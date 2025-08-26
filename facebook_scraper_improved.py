import requests
import json
import time
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone

try:
    from project.session_manager import SessionManager
    from project.rate_limit import with_backoff
    from project.progress import load_progress, save_progress
except ModuleNotFoundError:
    # Allow running from inside the project/ directory
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.dirname(__file__))
    from session_manager import SessionManager
    from rate_limit import with_backoff
    from progress import load_progress, save_progress

# Configuration
DEFAULT_FB_DTSG = ""

# Target endpoint and headers for www.facebook.com GraphQL
GRAPHQL_ENDPOINT = "https://www.facebook.com/api/graphql/"
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.facebook.com",
    "Referer": "https://www.facebook.com/",
}
    
DOC_ID_POSTS_SEARCH = "24197523603262205"  # Global search posts query

def _decode_possible_prefixed_json(text: str) -> Optional[Dict]:
    """Decode JSON that might have prefixes like 'for (;;);' or be JSONL.
    If multiple JSON objects present, prefer one with data.serpResponse.results.
    """
    text = text.strip()
    # Strip common anti-JSON prefixes
    for prefix in ('for (;;);', 'while(1);', 'for(;;);', 'while (1);'):
        if text.startswith(prefix):
            text = text[len(prefix):].lstrip()
            break
    # JSONL or chunked lines: scan and pick best candidate
    if '\n' in text and text.count('{') > 1:
        best = None
        for line in text.split('\n'):
            line = line.strip()
            if not line or not line.startswith('{'):
                continue
            try:
                obj = json.loads(line)
                # choose object that contains results edges or page_info
                data = obj.get('data') if isinstance(obj, dict) else None
                serp = data.get('serpResponse') if isinstance(data, dict) else None
                results = serp.get('results') if isinstance(serp, dict) else None
                if isinstance(results, dict) and (
                    isinstance(results.get('edges'), list) or isinstance(results.get('page_info'), dict)
                ):
                    return obj
                if best is None:
                    best = obj
            except Exception:
                continue
        return best
    # Single JSON object fallback
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

def _extract_message_from_story(story: Dict) -> Optional[str]:
    if not story:
        return None
    message_paths = [
        ['comet_sections', 'content', 'story', 'comet_sections', 'message', 'story', 'message', 'text'],
        ['comet_sections', 'content', 'story', 'comet_sections', 'message_container', 'story', 'message', 'text'],
        ['message', 'text'],
        ['message', 'message', 'text'],
        ['message_container', 'story', 'message', 'text'],
        ['message', 'message_container', 'story', 'message', 'text']
    ]
    for path in message_paths:
        current = story
        try:
            for key in path:
                current = current[key]
            if current and isinstance(current, str):
                return current
        except (KeyError, TypeError):
            continue
    return None

def _extract_created_time(story: Dict) -> Optional[str]:
    """Extract creation_time from Facebook story object. 
    Updated to target the correct JSON paths based on actual response structure."""
    if not story:
        return None
    
    # NEW: Primary paths based on actual Facebook response structure
    primary_paths = [
        ['creation_time'],  # Direct from story object
        ['story', 'creation_time'],  # If nested under story
    ]
    
    # NEW: Context layout paths (from metadata sections)
    context_paths = [
        ['comet_sections', 'context_layout', 'story', 'comet_sections', 'metadata', 0, 'story', 'creation_time'],
        ['comet_sections', 'metadata', 0, 'story', 'creation_time'],
    ]
    
    # Fallback paths (your original ones)
    fallback_paths = [
        ['created_time'],
        ['timestamp'],
        ['comet_sections', 'content', 'story', 'comet_sections', 'timestamp', 'story', 'creation_time']
    ]
    
    # Try all paths in order of priority
    all_paths = primary_paths + context_paths + fallback_paths
    
    for path in all_paths:
        current = story
        try:
            for key in path:
                current = current[key]
            if current:
                timestamp = str(current)
                # Convert Unix timestamp to ISO format
                if timestamp.isdigit():
                    ts = int(timestamp)
                    if ts > 10_000_000_000:  # milliseconds
                        ts = ts // 1000
                    return _format_iso_z(datetime.fromtimestamp(ts, tz=timezone.utc))
                return timestamp
        except (KeyError, TypeError, IndexError):
            continue
    return None

def _extract_author(story: Dict) -> Optional[Dict]:
    if not story:
        return None
    author_paths = [
        ['comet_sections', 'context_layout', 'story', 'comet_sections', 'actor_photo', 'story', 'actor'],
        ['comet_sections', 'actor_photo', 'story', 'actor'],
        ['actor'],
        ['story', 'actor']
    ]
    for path in author_paths:
        current = story
        try:
            for key in path:
                current = current[key]
            if current and isinstance(current, dict):
                return {
                    "id": current.get("id"),
                    "name": current.get("name", "Unknown")
                }
        except (KeyError, TypeError):
            continue
    actors = story.get('actors')
    if isinstance(actors, list) and actors:
        first = actors[0] or {}
        return {"id": first.get("id"), "name": first.get("name", "Unknown")}
    return None

def _extract_permalink(story: Dict) -> Optional[str]:
    if not story:
        return None
    permalink_paths = [
        ['www_permalink'],
        ['permalink'],
        ['url'],
        ['story', 'permalink'],
        ['story', 'url']
    ]
    for path in permalink_paths:
        current = story
        try:
            for key in path:
                current = current[key]
            if current and isinstance(current, str):
                return current
        except (KeyError, TypeError):
            continue
    post_id = story.get('post_id') or story.get('id')
    if post_id:
        return f"https://www.facebook.com/{post_id}"
    return None

def _format_iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def _fallback_fetch_created_time(session: requests.Session, url: Optional[str]) -> Optional[str]:
    """Fallback method to extract timestamp from HTML page"""
    if not url:
        return None
    try:
        headers = session.headers.copy()
        headers.pop('Content-Type', None)
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        
        candidate_urls = [url]
        try:
            if 'web.facebook.com' in url:
                candidate_urls.append(url.replace('web.facebook.com', 'www.facebook.com'))
                candidate_urls.append(url.replace('web.facebook.com', 'm.facebook.com'))
            elif 'www.facebook.com' in url:
                candidate_urls.append(url.replace('www.facebook.com', 'm.facebook.com'))
            elif 'm.facebook.com' in url:
                candidate_urls.append(url.replace('m.facebook.com', 'www.facebook.com'))
        except Exception:
            pass

        html = ''
        for test_url in candidate_urls:
            try:
                resp = session.get(test_url, headers=headers, timeout=20)
                if not resp.encoding:
                    resp.encoding = 'utf-8'
                html = resp.text or ''
                if html:
                    break
            except Exception:
                continue
        if not html:
            return None
            
        # 1) data-utime (unix seconds)
        m = re.search(r'data-utime="(\d{10,13})"', html)
        if m:
            ts = int(m.group(1))
            if ts > 10_000_000_000:  # milliseconds
                ts = ts // 1000
            return _format_iso_z(datetime.fromtimestamp(ts, tz=timezone.utc))
            
        # 2) ISO in meta tags
        m = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)', html)
        if m:
            try:
                dt = datetime.fromisoformat(m.group(1).replace('Z', '+00:00'))
                return _format_iso_z(dt)
            except Exception:
                pass
                
        # 3) publish_time in JSON blobs
        m = re.search(r'"publish_time"\s*:\s*(\d{10,13})', html)
        if m:
            ts = int(m.group(1))
            if ts > 10_000_000_000:
                ts = ts // 1000
            return _format_iso_z(datetime.fromtimestamp(ts, tz=timezone.utc))
            
    except Exception:
        return None
    return None

def _extract_post_from_edge(edge: Dict) -> Optional[Dict]:
    """Extract post information from search result edge"""
    try:
        story = None
        # Try different story extraction paths
        try:
            story = edge.get('rendering_strategy', {}).get('view_model', {}).get('click_model', {}).get('story')
        except (KeyError, TypeError):
            pass
        if not story:
            story_paths = [
                ['node', 'rendering_strategy', 'view_model', 'click_model', 'story'],
                ['rendering_strategy', 'view_model', 'click_model', 'story'],
                ['node', 'story'],
                ['story']
            ]
            for path in story_paths:
                current = edge
                try:
                    for key in path:
                        current = current[key]
                    if current and isinstance(current, dict):
                        story = current
                        break
                except (KeyError, TypeError):
                    continue
        if not story:
            return None
            
        post_id = story.get("post_id") or story.get("id")
        if not post_id:
            return None
            
        message = _extract_message_from_story(story)
        if not message:
            return None
            
        # IMPROVED: Better creation_time extraction
        created_time = _extract_created_time(story)
        author = _extract_author(story)
        permalink = _extract_permalink(story)
        
        return {
            "id": post_id,
            "message": message,
            "created_time": created_time,
            "author_name": author["name"] if author else "Unknown",
            "author_id": author["id"] if author else None,
            "permalink": permalink,
        }
    except Exception as e:
        return None

def _find_cursor_any(obj):
    """Find pagination cursor in nested response object"""
    try:
        if isinstance(obj, dict):
            for k in ("end_cursor", "endCursor"):
                if k in obj and isinstance(obj[k], str) and len(obj[k]) > 8:
                    return obj[k]
            if "cursor" in obj and isinstance(obj["cursor"], str) and len(obj["cursor"]) > 8:
                return obj["cursor"]
            for value in obj.values():
                result = _find_cursor_any(value)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = _find_cursor_any(item)
                if result:
                    return result
    except:
        pass
    return None

def fetch_posts(keyword, max_pages=30, page_size=5, delay_seconds=1.0, target_posts=100):
    """Main function to fetch posts from Facebook search API"""
    posts = []
    seen_post_ids = set()
    state = load_progress(keyword)
    cursor = state.get("last_cursor")
    page = 0

    sm = SessionManager()
    account = sm.next_account()
    if not account:
        raise Exception("No valid cookie sessions found in project/settings/cookies")
    session, session_headers, session_data = account
    tokens = SessionManager.extract_tokens(session_data)
    proxies = {}

    consecutive_empty_pages = 0
    retry_cleared_cursor = True
    
    while page < max_pages:
        print(f"\n📄 Page {page + 1}")

        variables = {
            "allow_streaming": False,
            "args": {
                "callsite": "COMET_GLOBAL_SEARCH",
                "config": {
                    "exact_match": False,
                    "high_confidence_config": None,
                    "intercept_config": None,
                    "sts_disambiguation": None,
                    "watch_config": None
                },
                "context": {
                    "bsid": f"{int(time.time() * 1000)}-{int(time.time() * 1000)}-{int(time.time() * 1000)}-{int(time.time() * 1000)}-{int(time.time() * 1000000)}",
                    "tsid": None
                },
                "experience": {
                    "client_defined_experiences": ["ADS_PARALLEL_FETCH"],
                    "encoded_server_defined_params": None,
                    "fbid": None,
                    "type": "GLOBAL_SEARCH"
                },
                "filters": [],
                "text": keyword
            },
            "count": page_size,
            "cursor": cursor,
            "feedLocation": "SEARCH",
            "feedbackSource": 23,
            "fetch_filters": True,
            "focusCommentID": None,
            "locale": None,
            "privacySelectorRenderLocation": "COMET_STREAM",
            "renderLocation": "search_results_page",
            "scale": 1,
            "stream_initial_count": 0,
            "useDefaultActor": False
        }

        current_time = int(time.time())
        fb_dtsg = tokens.get('fb_dtsg') or DEFAULT_FB_DTSG
        data = {
            'fb_dtsg': fb_dtsg,
            'doc_id': DOC_ID_POSTS_SEARCH,
            'variables': json.dumps(variables),
            '__spin_t': str(current_time)
        }

        try:
            def _send():
                return session.post(
                    GRAPHQL_ENDPOINT,
                    headers=session.headers,
                    data=data,
                    timeout=30,
                    proxies=proxies,
                )
            resp, need_rotate = with_backoff(_send, max_attempts=4, base_delay=2.0)

            # Rotate account if needed
            if resp is None or need_rotate or (resp is not None and resp.status_code in (429, 403)):
                print("🔁 Rotating account...")
                account = sm.next_account()
                if not account:
                    print("No more accounts available.")
                    break
                session, session_headers, session_data = account
                tokens = SessionManager.extract_tokens(session_data)
                fb_dtsg = tokens.get('fb_dtsg') or DEFAULT_FB_DTSG
                resp, _ = with_backoff(_send, max_attempts=3, base_delay=2.0)
                if resp is None:
                    print("Rate limit persists after rotation.")
                    break

            if not resp.encoding:
                resp.encoding = "utf-8"
                
            print(f"Status: {resp.status_code}, Response Length: {len(resp.text)} chars")
            
            if resp.status_code != 200:
                print(f"Error: HTTP {resp.status_code}")
                break

            obj = _decode_possible_prefixed_json(resp.text)
            if not isinstance(obj, dict):
                print("No valid JSON object found")
                break

            # Save first page for debugging if needed
            if page == 0:
                with open(f"response_page_{page + 1}.json", "w", encoding="utf-8") as f:
                    json.dump(obj, f, indent=2, ensure_ascii=False)

            if isinstance(obj, dict) and isinstance(obj.get('errors'), list) and obj['errors']:
                print(f"GraphQL errors: {[str(err.get('message', '')) for err in obj['errors'][:3]]}")

            data_root = obj.get("data", {})
            serp = data_root.get("serpResponse", {})
            results = serp.get("results", {})
            edges = results.get("edges", [])

            print(f"Found {len(edges)} edges")

            page_posts = []
            for edge in edges:
                post = _extract_post_from_edge(edge)
                if post and post.get("message"):
                    # Fallback for missing created_time
                    if not post.get("created_time"):
                        post["created_time"] = _fallback_fetch_created_time(session, post.get("permalink"))
                    
                    # Ensure proper format
                    if post.get("created_time") and isinstance(post["created_time"], (int, float, str)):
                        try:
                            val = str(post["created_time"]).strip()
                            if val.isdigit():
                                ts = int(val)
                                if ts > 10_000_000_000:
                                    ts = ts // 1000
                                post["created_time"] = _format_iso_z(datetime.fromtimestamp(ts, tz=timezone.utc))
                        except Exception:
                            pass
                    
                    if post["id"] not in seen_post_ids:
                        seen_post_ids.add(post["id"])
                        post["search_keyword"] = keyword
                        post["page"] = page + 1
                        page_posts.append(post)

            if page_posts:
                posts.extend(page_posts)
                
                # Save page results
                with open(f"posts_page_{page + 1}.jsonl", "w", encoding="utf-8") as f:
                    for post in page_posts:
                        f.write(json.dumps(post, ensure_ascii=False) + "\n")
                        
                with open("posts.jsonl", "a", encoding="utf-8") as f:
                    for post in page_posts:
                        f.write(json.dumps(post, ensure_ascii=False) + "\n")
                
                print(f"✅ Saved {len(page_posts)} posts (Total: {len(posts)})")
                
                if len(posts) >= target_posts:
                    print(f"🎯 Reached target of {target_posts} posts!")
                    break
            else:
                print("No new posts found")
                if page == 0 and state.get("last_cursor") and retry_cleared_cursor:
                    print("Clearing saved cursor and retrying...")
                    cursor = None
                    save_progress(keyword, None, len(posts))
                    retry_cleared_cursor = False
                    consecutive_empty_pages = 0
                    continue

            # Check pagination
            page_info = results.get("page_info") or results.get("pageInfo") or {}
            has_next = (
                page_info.get("has_next_page")
                if isinstance(page_info, dict) and "has_next_page" in page_info
                else page_info.get("hasNextPage") if isinstance(page_info, dict) else None
            )
            next_cursor = None
            if isinstance(page_info, dict):
                next_cursor = page_info.get("end_cursor") or page_info.get("endCursor")
                
            if not next_cursor and edges:
                for edge in edges:
                    edge_cursor = edge.get("cursor")
                    if edge_cursor and isinstance(edge_cursor, str) and len(edge_cursor) > 8:
                        next_cursor = edge_cursor
                        break
                        
            if not next_cursor and edges:
                next_cursor = _find_cursor_any(obj)

            if not has_next and not next_cursor:
                print("✅ Reached end of results")
                break
            if not next_cursor:
                print("⚠️ No cursor for next page")
                break

            cursor = next_cursor
            page += 1
            save_progress(keyword, cursor, len(posts))
            time.sleep(delay_seconds)

        except Exception as e:
            print(f"Error: {e}")
            break

    return posts, cursor

if __name__ == "__main__":
    try:
        keyword = "credit agricole"
        posts, last_cursor = fetch_posts(keyword, max_pages=10, page_size=5, delay_seconds=1.0, target_posts=50)
        
        # Final save
        with open("posts.jsonl", "w", encoding="utf-8") as f:
            for post in posts:
                f.write(json.dumps(post, ensure_ascii=False) + "\n")
                
        print(f"\n🎉 FINAL RESULTS:")
        print(f"📊 Total posts collected: {len(posts)}")
        print(f"🔗 Unique post IDs: {len(set(post['id'] for post in posts))}")
        
        # Check creation_time coverage
        posts_with_time = sum(1 for p in posts if p.get('created_time'))
        print(f"📅 Posts with creation_time: {posts_with_time}/{len(posts)} ({posts_with_time/len(posts)*100:.1f}%)")
        
    except Exception as e:
        print(f"Error: {e}")