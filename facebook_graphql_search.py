#!/usr/bin/env python3
"""
Facebook GraphQL API Search
Uses Facebook's internal GraphQL API for search - much more reliable and complete data
"""

import requests
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

def facebook_graphql_search(keyword: str, pages: int = 5):
    """
    Search Facebook using internal GraphQL API
    Returns structured data from Facebook's real search endpoint
    """
    
    # Your provided cookies and headers
    cookies = {
        'datr': 'u4MOaBz8cANjLPfdxB-kyrow',
        'sb': 'u4MOaKiWNS00Ub_bVCu0Kc2f',
        'ps_l': '1',
        'ps_n': '1',
        'c_user': '100007570923188',
        'b_user': '61559962276051',
        'locale': 'en_US',
        'pas': '100007570923188%3A0tD7VC74XY',
        'fbl_st': '101628247%3BT%3A29267760',
        'wl_cbv': 'v2%3Bclient_version%3A2902%3Btimestamp%3A1756065637',
        'dpr': '1',
        'wd': '1920x919',
        'ar_debug': '1',
        'fr': '1yicHj3sck1c8Y88b.AWdt42sk1ovov4veHzQyixVUS8o9dqyBnabJiOABBR2kPrE5oJA.BorixF..AAA.0.0.BorixF.AWdDJriyAIAAmh6FjqiLVh-n-Zs',
        'xs': '39%3AHedndidVURnKpw%3A2%3A1746745261%3A-1%3A-1%3AhpgzruHmnkIPDA%3AAcXHkHSM908HEl3N5boOsl8UqwsKXWqiCBAXhf5hvfds',
        'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1756245102703%2C%22v%22%3A1%7D',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ar;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': f'https://www.facebook.com/search/posts?q={keyword}&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-full-version-list': '"Not;A=Brand";v="99.0.0.0", "Google Chrome";v="139.0.7258.139", "Chromium";v="139.0.7258.139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'x-asbd-id': '359341',
        'x-fb-friendly-name': 'SearchCometResultsPaginatedResultsQuery',
        'x-fb-lsd': 'vLhMaN7xuRiuDe_Nydjw6X',
    }

    # Base data for GraphQL request
    base_data = {
        'av': '100007570923188',
        '__aaid': '0',
        '__user': '100007570923188',
        '__a': '1',
        '__req': '8',
        '__hs': '20326.HYP:comet_pkg.2.1...0',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1026338653',
        '__s': 'nafkqu:gatg18:icuu5r',
        '__hsi': '7543015359938874891',
        '__dyn': '7xeUjGU5a5Q1ryaxG4Vp41twWwIxu13wFwhUngS3q2ibwNw9G2Saw8i2S1DwUx60GE3Qwb-q7oc81EEc87m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE4u9x-3m1mzXw8W58jwGzEaE5e3ym2SU4i5oe8464-5pUfEe88o4Wm7-2K0-obUG2-azqwaW223908O3216xi4UK2K2WEjxK2B08-269wkopg6C13xecwBwWwjHDzUiBG2OUqwjVqwLwHwa211wo83KwHwOyUqxG',
        '__csr': 'gP0CgiEnNsp3cG9b7ivbRqOQJ8yqZ9RR99NffqcHdRi_llHbkGaDkx6YzcBlJAi6aFl-mqgKKBnF9YxLqbJbhWZpWWy5-8QFFFe_DpaAzuJpt25UCiLyvmchFUGmSGoSuazmp3p8sgOUKufG9iG-ifglGqq9ye4eq2517GFoCmmjHAxyQ5UKujwwxSmcyo6a2vQbJa2-q4oGmbDDyEK4oswCU8oWbK9x658izo42224Ue84CimbG4opx22nxu58be5VUGcwmEowqU-m1dxOUizqwgUKu6UlwxwzwKwWwsEc8nyGxy3OucyEK2O9xe2-1bCwkUC78fEcE5KbwuUC17BwPU6SaCw52w9q2K4E1Fbw_xC6p8eWQ320P84a0CE11Q1wyE7W368xXw8m6oqXwBwcWeG8gsBDx2E05hOcw1kC0gm0yEy0afwdLg0pqw0ebNw5Hxam0oa0li09nyoC2N07Xw7Zw9Aw0Tq1ko1bA684C360jW09xg0gDyoB38C02lW4EB39C06E8C049E0afo0Ehwgo1ComG49dw0GIw1gm07j9U0wAw1oA0jl0wCG0na0bwx4w',
        '__hsdp': 'ga90Yy9psGh9atQAyCaguqhAInaGq4478qCJqQwwhIyi17GGVF5AIdF6Fbcx14a4eoWGsHsBdevclelkOmBx92dlix9Q8aWgDSuQHqBgSQ6yAzaKltim9xt2Kih4iyQ48B3F62ecUG2K9F2ozKawEgx17gsiDDBDzlFufxaaIwh9wg9pkbwmE-44bzokBjqh9AhLolsV8GayVOHyWgwEsgy66fBUHwxc7i1K5rDgcQcGt0Dy9WoV6zoOumHykec9URkcggAwAhm2y2K1dwjUG1iwg822Ukwg69x23y68syUN4F5YYTgjXwImcw8a2Gag3dy838wl80xK2y16w8F6agV83lpyra1Og41xy1tohwqU56a63NU3rw33U1P81w40kYE1so08to1ak2m-i',
        '__hblp': '08a6U2Fogw9K1qDwXw2hGwxwj8-0k61LwQzUpyofoaUaE5F0xwt9E8Ee83UwAwoobbwlu1OxK1dAwrE9E5W1-yEeVUoxSQ4E6S1wxa8hki1Fw4Rw861Qg9Xg2bwpU7-0H8C1gwt89oe204nwd-1cwr8c81e40mW0tyU4K5Edo-bwjU2Gws84e0G8S1YwSwfS8wpoco2FVFE1Q8bU2dw2UU6W7U2EwcC21aag2iDzQ6pE4y0haUaU2awpEvw4fw4gwaCi3edw_g7-10wo82YCwq8564EGu7EhyEuwAwXyU4i1zwtE6m7A4ESewOwgohwibw4Hw6dweC0g20sG6U9E520Qubw58wgU4-0HGAw96',
        '__sjsp': 'ga90Yy9psGh9atQAyCaguqhAInaGq4478qCJqQwwhIyi17GGVF5AIdF6Fbcx14a4eoWGsHsBdevclelkOmBx92dlix9Q8aWgDSuQHqBgSQ6yAzaKltim9xt2Kih4iyQ48B3F62ecUG2K9F2ozKawEgx17gsiDDBDzlFufxaaIwh9wg9pkbwmE-44bzokBjqh9AhLolsV8GayVOHyWgwEsgy66fBUHwxc7i1K5rDgcQcGt0Dy9WoV6zoOumHykec9URkcggAwAhm2y2K1dwjUG1iwg822Ukwg69x23y68syUN4F5YYTgjXwImcw8a2Gag3dy838wl80xK2y16w8F6agV83lpyra1Og41xy1tohwqU56a63NU3rw33U1P81w40kYE1so08to1ak2m-i',
        '__comet_req': '15',
        'fb_dtsg': 'NAfsC--IVdRQAbezpRZYxfOtlFELNplwlYHtscNqWlFd6oFCgX57w0g:39:1746745261',
        'jazoest': '25628',
        'lsd': 'vLhMaN7xuRiuDe_Nydjw6X',
        '__spin_r': '1026338653',
        '__spin_b': 'trunk',
        '__spin_t': '1756245121',
        '__crn': 'comet.fbweb.CometSearchGlobalSearchDefaultTabRoute',
        'qpl_active_flow_ids': '1056839232,1056842055,25305590',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'SearchCometResultsPaginatedResultsQuery',
        'server_timestamps': 'true',
        'doc_id': '24190416707327186',
    }

    print(f"🚀 Facebook GraphQL Search for: '{keyword}'")
    print(f"📄 Requesting {pages} pages of results")
    print("=" * 60)

    all_posts = []
    cursor = None
    page_count = 0

    try:
        for page_num in range(pages):
            page_count += 1
            print(f"\n📖 Requesting page {page_num + 1}...")

            # Build variables for this request
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
                        "bsid": "bb428b12-50ca-47b0-a3d7-ab3fab3189c5",
                        "tsid": None
                    },
                    "experience": {
                        "client_defined_experiences": ["ADS_PARALLEL_FETCH"],
                        "encoded_server_defined_params": None,
                        "fbid": None,
                        "type": "POSTS_TAB"
                    },
                    "filters": ["{\"name\":\"recent_posts\",\"args\":\"\"}"],
                    "text": keyword
                },
                "count": 10,  # Posts per page
                "feedLocation": "SEARCH",
                "feedbackSource": 23,
                "fetch_filters": True,
                "focusCommentID": None,
                "locale": None,
                "privacySelectorRenderLocation": "COMET_STREAM",
                "renderLocation": "search_results_page",
                "scale": 1,
                "stream_initial_count": 0,
                "useDefaultActor": False,
                # GraphQL feature flags
                "__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider": True,
                "__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider": True,
                "__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider": False,
                "__relay_internal__pv__IsWorkUserrelayprovider": False,
                "__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider": True,
                "__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider": False,
                "__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider": False,
                "__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider": False,
                "__relay_internal__pv__IsMergQAPollsrelayprovider": False,
                "__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider": True,
                "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False,
                "__relay_internal__pv__CometUFIShareActionMigrationrelayprovider": True,
                "__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider": False,
                "__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider": True,
                "__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider": True
            }

            # Add cursor for pagination (after first page)
            if cursor:
                variables["cursor"] = cursor

            # Prepare request data
            data = base_data.copy()
            data['variables'] = json.dumps(variables)

            # Make request
            response = requests.post(
                'https://www.facebook.com/api/graphql/',
                cookies=cookies,
                headers=headers,
                data=data,
                timeout=30
            )

            if response.status_code != 200:
                print(f"❌ Request failed with status {response.status_code}")
                break

            # Parse response
            try:
                json_response = response.json()
                
                # Navigate to the search results
                if 'data' in json_response and 'serpResponse' in json_response['data']:
                    results = json_response['data']['serpResponse']['results']
                    
                    if 'edges' in results:
                        edges = results['edges']
                        posts_found_this_page = 0
                        
                        for edge in edges:
                            if 'node' in edge:
                                post_data = extract_post_info(edge['node'], keyword)
                                if post_data:
                                    all_posts.append(post_data)
                                    posts_found_this_page += 1
                                    print(f"✅ Post {len(all_posts)}: {post_data['author']} - {post_data['text'][:60]}...")
                        
                        print(f"📊 Page {page_num + 1}: Found {posts_found_this_page} posts")
                        
                        # Get cursor for next page
                        if 'page_info' in results and results['page_info'].get('has_next_page'):
                            cursor = results['page_info'].get('end_cursor')
                            if not cursor:
                                print("🔚 No more pages available")
                                break
                        else:
                            print("🔚 Reached end of results")
                            break
                    else:
                        print("❌ No edges found in results")
                        break
                else:
                    print("❌ No search results found in response")
                    break

            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                break
            except Exception as e:
                print(f"❌ Error processing response: {e}")
                break

        # Create final summary
        summary = {
            "search_info": {
                "keyword": keyword,
                "pages_requested": pages,
                "pages_processed": page_count,
                "total_posts_found": len(all_posts),
                "search_timestamp": datetime.now().isoformat(),
                "method": "facebook_graphql_api"
            },
            "statistics": {
                "posts_with_text": sum(1 for p in all_posts if p.get('text')),
                "posts_with_authors": sum(1 for p in all_posts if p.get('author')),
                "posts_with_urls": sum(1 for p in all_posts if p.get('post_url')),
                "posts_with_dates": sum(1 for p in all_posts if p.get('publication_date'))
            },
            "posts": all_posts
        }

        return summary

    except Exception as e:
        return {
            "error": "GraphQL search failed",
            "message": str(e),
            "keyword": keyword,
            "partial_results": len(all_posts)
        }

def extract_post_info(node: Dict, keyword: str) -> Dict[str, Any]:
    """
    Extract important post information from Facebook GraphQL node
    Focuses on: content text, author, publication date, post URL
    """
    try:
        post_info = {
            "text": "",
            "author": "",
            "author_id": "",
            "publication_date": "",
            "post_url": "",
            "post_id": "",
            "search_keyword": keyword
        }

        # Extract text content
        if 'comet_sections' in node:
            # Try to find text in comet_sections
            sections = node['comet_sections']
            if 'content' in sections:
                content = sections['content']
                if 'story' in content:
                    story = content['story']
                    if 'message' in story and story['message']:
                        post_info['text'] = story['message'].get('text', '')

        # Alternative text extraction paths
        if not post_info['text']:
            # Try other common text locations
            if 'story' in node:
                story = node['story']
                if 'message' in story and story['message']:
                    post_info['text'] = story['message'].get('text', '')
                elif 'comet_sections' in story:
                    # Look in story's comet_sections
                    pass

        # Extract author information
        if 'comet_sections' in node:
            sections = node['comet_sections']
            if 'context_layout' in sections:
                context = sections['context_layout']
                if 'story' in context:
                    story_context = context['story']
                    if 'comet_sections' in story_context:
                        story_sections = story_context['comet_sections']
                        if 'actor_photo' in story_sections:
                            actor = story_sections['actor_photo']
                            if 'story' in actor:
                                actor_story = actor['story']
                                if 'actors' in actor_story and actor_story['actors']:
                                    first_actor = actor_story['actors'][0]
                                    post_info['author'] = first_actor.get('name', '')
                                    post_info['author_id'] = first_actor.get('id', '')

        # Extract post URL and ID
        if 'post_id' in node:
            post_info['post_id'] = node['post_id']
            # Construct URL from post ID
            post_info['post_url'] = f"https://www.facebook.com/story.php?story_fbid={node['post_id']}"

        # Extract publication date
        if 'comet_sections' in node:
            sections = node['comet_sections']
            if 'context_layout' in sections:
                context = sections['context_layout']
                if 'story' in context:
                    story_context = context['story']
                    if 'creation_time' in story_context:
                        post_info['publication_date'] = str(story_context['creation_time'])

        # Only return if we found some useful information
        if post_info['text'] or post_info['author'] or post_info['post_id']:
            return post_info
        else:
            return None

    except Exception as e:
        print(f"⚠️  Error extracting post info: {e}")
        return None

def main():
    keyword = "inwi.ma"
    pages = 3  # Start with fewer pages for testing
    
    print("🚀 Facebook GraphQL API Search - REAL EXECUTION")
    print("=" * 60)
    
    # Execute search
    results = facebook_graphql_search(keyword, pages)
    
    print("\n" + "=" * 60)
    print("🎯 FINAL RESULTS")
    print("=" * 60)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        print(f"💬 Message: {results['message']}")
    else:
        info = results['search_info']
        stats = results['statistics']
        
        print(f"📝 Keyword: {info['keyword']}")
        print(f"📊 Total posts found: {info['total_posts_found']}")
        print(f"📄 Pages processed: {info['pages_processed']}/{info['pages_requested']}")
        print(f"📊 Posts with text: {stats['posts_with_text']}")
        print(f"👤 Posts with authors: {stats['posts_with_authors']}")
        print(f"🔗 Posts with URLs: {stats['posts_with_urls']}")
        
        if results['posts']:
            print(f"\n📋 SAMPLE POSTS:")
            for i, post in enumerate(results['posts'][:3], 1):
                print(f"\n🔸 Post {i}:")
                print(f"   Author: {post.get('author', 'Unknown')}")
                print(f"   Text: {post.get('text', 'No text')[:100]}...")
                print(f"   URL: {post.get('post_url', 'No URL')}")
                print(f"   Date: {post.get('publication_date', 'No date')}")

    print(f"\n📋 COMPLETE JSON RESULTS:")
    print("=" * 60)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save results
    filename = f"facebook_graphql_search_{keyword.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    main()