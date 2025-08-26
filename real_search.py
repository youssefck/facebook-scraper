#!/usr/bin/env python3
"""
Real Facebook Post Search with Authentication
Uses provided cookies for authenticated search
"""

import json
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add the current directory to Python path
sys.path.insert(0, '/workspace')

# Your provided cookies for authentication
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

def search_with_cookies(keyword: str, pages: int = 10):
    """
    Search Facebook posts with authentication cookies
    """
    print(f"🔍 Starting REAL Facebook search for: '{keyword}'")
    print(f"📄 Searching {pages} pages")
    print(f"🔐 Using provided authentication cookies")
    print("=" * 60)
    
    try:
        # Try to import and use the real facebook_scraper
        from facebook_scraper import get_posts_by_search
        
        results = []
        post_count = 0
        
        print("🚀 Initiating search...")
        
        # Perform the search with cookies
        print("🔧 Configuring search parameters...")
        search_iterator = get_posts_by_search(
            word=keyword,
            cookies=COOKIES,
            pages=pages,
            timeout=60,  # Longer timeout
            options={
                "comments": False,  # Skip comments for faster processing
                "reactions": False,  # Disable reactions initially to avoid issues
                "allow_extra_requests": False,  # Disable extra requests
                "posts_per_page": 4  # Default page size
            }
        )
        
        for post in search_iterator:
            post_count += 1
            
            # Extract key information
            post_info = {
                "post_number": post_count,
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
                "reactions": post.get('reactions', {}),
                "has_image": bool(post.get('image') or post.get('images')),
                "has_video": bool(post.get('video')),
                "factcheck": post.get('factcheck'),
                "search_keyword": keyword
            }
            
            # Add image info
            if post.get('images'):
                post_info["images"] = post.get('images', [])
                post_info["image_count"] = len(post.get('images', []))
            elif post.get('image'):
                post_info["images"] = [post.get('image')]
                post_info["image_count"] = 1
            else:
                post_info["images"] = []
                post_info["image_count"] = 0
            
            # Truncate very long text for preview
            if len(post_info["text"]) > 500:
                post_info["text_preview"] = post_info["text"][:500] + "..."
                post_info["full_text_length"] = len(post_info["text"])
            
            results.append(post_info)
            
            print(f"✅ Post {post_count}: {post_info['author']} - {post_info['text'][:80]}...")
            
            # Show progress every 10 posts
            if post_count % 10 == 0:
                print(f"📊 Progress: {post_count} posts found so far...")
        
        # Final summary
        print("\n" + "=" * 60)
        print(f"🎯 SEARCH COMPLETED!")
        print(f"📝 Keyword: '{keyword}'")
        print(f"📄 Pages searched: {pages}")
        print(f"📊 Total posts found: {post_count}")
        
        if results:
            total_engagement = sum(r.get('likes', 0) + r.get('comments', 0) + r.get('shares', 0) for r in results)
            total_likes = sum(r.get('likes', 0) for r in results)
            total_comments = sum(r.get('comments', 0) for r in results)
            total_shares = sum(r.get('shares', 0) for r in results)
            posts_with_images = sum(1 for r in results if r.get('has_image'))
            posts_with_videos = sum(1 for r in results if r.get('has_video'))
            
            print(f"💬 Total engagement: {total_engagement}")
            print(f"   👍 Total likes: {total_likes}")
            print(f"   💬 Total comments: {total_comments}")
            print(f"   🔄 Total shares: {total_shares}")
            print(f"🖼️  Posts with images: {posts_with_images}")
            print(f"🎥 Posts with videos: {posts_with_videos}")
        
        # Create final output
        final_output = {
            "search_info": {
                "keyword": keyword,
                "pages_searched": pages,
                "total_posts_found": post_count,
                "search_timestamp": datetime.now().isoformat(),
                "authentication": "cookies_used"
            },
            "statistics": {
                "total_engagement": sum(r.get('likes', 0) + r.get('comments', 0) + r.get('shares', 0) for r in results),
                "total_likes": sum(r.get('likes', 0) for r in results),
                "total_comments": sum(r.get('comments', 0) for r in results),
                "total_shares": sum(r.get('shares', 0) for r in results),
                "posts_with_images": sum(1 for r in results if r.get('has_image')),
                "posts_with_videos": sum(1 for r in results if r.get('has_video')),
                "public_posts": sum(1 for r in results if r.get('is_public'))
            },
            "posts": results
        }
        
        return final_output
        
    except ImportError as e:
        print(f"❌ Error: Facebook scraper dependencies not available: {e}")
        print("📦 Required packages: requests-html, dateparser, demjson3, beautifulsoup4")
        return {
            "error": "Dependencies not available",
            "message": str(e),
            "keyword": keyword,
            "status": "failed"
        }
        
    except Exception as e:
        print(f"❌ Search failed with error: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        return {
            "error": "Search failed", 
            "message": str(e),
            "error_type": type(e).__name__,
            "keyword": keyword,
            "partial_results": len(results) if 'results' in locals() else 0
        }

def main():
    keyword = "inwi.ma"
    pages = 10
    
    print("🚀 Facebook Post Search - REAL EXECUTION")
    print("=" * 60)
    
    # Execute search
    results = search_with_cookies(keyword, pages)
    
    print("\n📋 COMPLETE JSON RESULTS:")
    print("=" * 60)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save results
    filename = f"real_search_inwi_ma_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    main()