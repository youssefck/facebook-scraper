#!/usr/bin/env python3
"""
Alternative Facebook Search - Using page scraping instead of global search
"""

import json
import sys
from datetime import datetime
sys.path.insert(0, '/workspace')

# Your cookies
COOKIES = {
    'datr': 'T5AiZ8l6hbmh1Qh3OTE-_vSf',
    'sb': 'T5AiZ5UyDKV9wbgl_mBw6y2R', 
    'ps_l': '1',
    'ps_n': '1',
    'dpr': '1.5',
    'c_user': '100003651255170',
    'xs': '23%3Akb3jl3EgjW-ZgQ%3A2%3A1756137972%3A-1%3A-1',
    'fr': '1cGoymFMkpiDiRWmt.AWeCaO07KIrhu3-_A6UMmA0ayiK7iA62oRnN00-QKovpGuJy8Uc.Boqfzc..AAA.0.0.BorIn2.AWdH_UghHdnTh16TQ4il46lpePE',
    'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1756138038008%2C%22v%22%3A1%7D',
    'wd': '1920x326',
}

def search_in_pages(keyword: str, pages_to_search: list, posts_per_page: int = 10):
    """
    Search for keyword in specific Facebook pages
    """
    print(f"🔍 Searching for '{keyword}' in Facebook pages")
    print(f"📄 Pages to search: {pages_to_search}")
    print("🔐 Using authentication cookies")
    print("=" * 60)
    
    try:
        from facebook_scraper import get_posts
        
        all_results = []
        total_posts_found = 0
        
        for page_name in pages_to_search:
            print(f"\n📖 Searching in page: {page_name}")
            page_results = []
            page_post_count = 0
            
            try:
                # Get posts from this page
                for post in get_posts(page_name, cookies=COOKIES, pages=3):
                    page_post_count += 1
                    
                    # Check if keyword appears in post text
                    post_text = post.get('text', '').lower()
                    if keyword.lower() in post_text:
                        total_posts_found += 1
                        
                        post_info = {
                            "match_number": total_posts_found,
                            "source_page": page_name,
                            "post_id": post.get('post_id', 'N/A'),
                            "text": post.get('text', '').strip(),
                            "author": post.get('username', 'Unknown'),
                            "author_id": post.get('user_id', 'N/A'),
                            "post_url": post.get('post_url', 'N/A'),
                            "timestamp": post.get('time', '').isoformat() if post.get('time') else 'N/A',
                            "likes": post.get('likes', 0),
                            "comments": post.get('comments', 0),
                            "shares": post.get('shares', 0),
                            "is_public": post.get('available', False),
                            "has_image": bool(post.get('image') or post.get('images')),
                            "has_video": bool(post.get('video')),
                            "search_keyword": keyword,
                            "keyword_positions": [i for i, word in enumerate(post_text.split()) if keyword.lower() in word.lower()]
                        }
                        
                        page_results.append(post_info)
                        print(f"✅ Match {total_posts_found}: {post_info['text'][:80]}...")
                    
                    # Limit posts per page to avoid hitting limits
                    if page_post_count >= posts_per_page:
                        break
                
                print(f"📊 Page '{page_name}': {len(page_results)} matches from {page_post_count} posts")
                all_results.extend(page_results)
                
            except Exception as page_error:
                print(f"❌ Error searching page '{page_name}': {page_error}")
                continue
        
        # Create summary
        summary = {
            "search_info": {
                "keyword": keyword,
                "pages_searched": pages_to_search,
                "total_matches": total_posts_found,
                "search_timestamp": datetime.now().isoformat(),
                "method": "page_scraping"
            },
            "statistics": {
                "total_engagement": sum(r.get('likes', 0) + r.get('comments', 0) + r.get('shares', 0) for r in all_results),
                "total_likes": sum(r.get('likes', 0) for r in all_results),
                "total_comments": sum(r.get('comments', 0) for r in all_results),
                "total_shares": sum(r.get('shares', 0) for r in all_results),
                "posts_with_images": sum(1 for r in all_results if r.get('has_image')),
                "posts_with_videos": sum(1 for r in all_results if r.get('has_video'))
            },
            "matches": all_results
        }
        
        return summary
        
    except Exception as e:
        return {
            "error": "Page search failed",
            "message": str(e),
            "keyword": keyword
        }

def search_specific_pages_for_inwi():
    """
    Search for 'inwi.ma' in relevant Moroccan/telecom pages
    """
    
    # Pages that might mention inwi.ma
    relevant_pages = [
        "inwi",  # Official Inwi page
        "Maroc",  # Morocco general page
        "TelecomMorocco",  # If exists
        "Morocco.Travel",  # Tourism page
        "MoroccoToday",  # News page
    ]
    
    print("🚀 ALTERNATIVE SEARCH APPROACH")
    print("=" * 60)
    print("🎯 Instead of global search, searching specific pages")
    print("🔍 This method is more reliable and bypasses search restrictions")
    
    results = search_in_pages("inwi.ma", relevant_pages, posts_per_page=15)
    
    print("\n" + "=" * 60)
    print("🎯 SEARCH RESULTS")
    print("=" * 60)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        print(f"💬 Message: {results['message']}")
    else:
        print(f"📝 Keyword: {results['search_info']['keyword']}")
        print(f"📊 Total matches: {results['search_info']['total_matches']}")
        print(f"📄 Pages searched: {len(results['search_info']['pages_searched'])}")
        
        if results['statistics']['total_engagement'] > 0:
            stats = results['statistics']
            print(f"💬 Total engagement: {stats['total_engagement']}")
            print(f"   👍 Likes: {stats['total_likes']}")
            print(f"   💬 Comments: {stats['total_comments']}")
            print(f"   🔄 Shares: {stats['total_shares']}")
    
    print("\n📋 JSON RESULTS:")
    print("=" * 60)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save results
    filename = f"page_search_inwi_ma_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    search_specific_pages_for_inwi()