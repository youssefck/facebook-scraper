#!/usr/bin/env python3
"""
Facebook Post Search Script
Searches for posts by keyword and returns results in JSON format
"""

import sys
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the current directory to Python path to import facebook_scraper
sys.path.insert(0, '/workspace')

try:
    from facebook_scraper import get_posts_by_search
    SCRAPER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Facebook scraper not available: {e}")
    SCRAPER_AVAILABLE = False

def search_facebook_posts(keyword: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for Facebook posts by keyword and return structured results
    
    Args:
        keyword: Search term/keyword
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries containing post information
    """
    if not SCRAPER_AVAILABLE:
        # Return demo data showing the expected format
        demo_results = []
        for i in range(min(max_results, 3)):
            demo_results.append({
                "post_id": f"demo_post_{i+1}",
                "text": f"This is a demo post about {keyword}. This shows the format of results you would get when the scraper is fully functional.",
                "author": f"DemoUser{i+1}",
                "author_id": f"demo_user_{i+1}",
                "post_url": f"https://facebook.com/demo_post_{i+1}",
                "timestamp": datetime.now().isoformat(),
                "likes": 10 + i * 5,
                "comments": 2 + i,
                "shares": i,
                "is_public": True,
                "has_image": i % 2 == 0,
                "has_video": i % 3 == 0,
                "factcheck": None,
                "reactions": {"like": 10 + i * 5, "love": i, "haha": 0},
                "search_keyword": keyword,
                "image_count": 1 if i % 2 == 0 else 0,
                "first_image": f"https://demo.com/image_{i+1}.jpg" if i % 2 == 0 else None,
                "_note": "This is demo data - real scraper would return actual Facebook posts"
            })
        return demo_results
    
    results = []
    try:
        # Calculate pages needed (assuming ~4 posts per page)
        pages_needed = max(1, (max_results + 3) // 4)
        
        print(f"🔍 Searching for '{keyword}' (up to {max_results} results, {pages_needed} pages)...")
        
        post_count = 0
        for post in get_posts_by_search(keyword, pages=pages_needed):
            if post_count >= max_results:
                break
                
            # Extract key information from the post
            post_info = {
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
                "factcheck": post.get('factcheck'),
                "reactions": post.get('reactions', {}),
                "search_keyword": keyword
            }
            
            # Add image info if available
            if post.get('images'):
                post_info["image_count"] = len(post.get('images', []))
                post_info["first_image"] = post.get('images', [None])[0]
            elif post.get('image'):
                post_info["image_count"] = 1
                post_info["first_image"] = post.get('image')
            else:
                post_info["image_count"] = 0
                post_info["first_image"] = None
            
            # Truncate long text for better readability
            if len(post_info["text"]) > 300:
                post_info["text_preview"] = post_info["text"][:300] + "..."
                post_info["text_full"] = post_info["text"]
                post_info["text"] = post_info["text_preview"]
            
            results.append(post_info)
            post_count += 1
            
            print(f"✓ Found post {post_count}: {post_info['text'][:50]}...")
            
    except Exception as e:
        error_result = {
            "error": "Search failed",
            "error_message": str(e),
            "keyword": keyword,
            "partial_results": len(results),
            "suggestion": "Try using authentication cookies for better results"
        }
        results.append(error_result)
    
    return results

def format_results_summary(results: List[Dict[str, Any]], keyword: str) -> Dict[str, Any]:
    """Format a summary of search results"""
    
    if not results:
        return {
            "keyword": keyword,
            "total_found": 0,
            "message": "No posts found for this keyword",
            "results": []
        }
    
    # Check if we have an error result
    if len(results) == 1 and "error" in results[0]:
        return {
            "keyword": keyword,
            "status": "error",
            "total_found": 0,
            "error": results[0],
            "results": []
        }
    
    # Filter out any error entries for the summary
    valid_results = [r for r in results if "error" not in r]
    
    total_engagement = sum(r.get('likes', 0) + r.get('comments', 0) + r.get('shares', 0) 
                          for r in valid_results)
    
    summary = {
        "keyword": keyword,
        "total_found": len(valid_results),
        "search_timestamp": datetime.now().isoformat(),
        "engagement_stats": {
            "total_likes": sum(r.get('likes', 0) for r in valid_results),
            "total_comments": sum(r.get('comments', 0) for r in valid_results),
            "total_shares": sum(r.get('shares', 0) for r in valid_results),
            "total_engagement": total_engagement
        },
        "content_stats": {
            "posts_with_images": sum(1 for r in valid_results if r.get('has_image')),
            "posts_with_videos": sum(1 for r in valid_results if r.get('has_video')),
            "public_posts": sum(1 for r in valid_results if r.get('is_public'))
        },
        "results": valid_results
    }
    
    return summary

def main():
    """Main function to run the search"""
    
    # Get parameters from command line or use defaults
    if len(sys.argv) < 2:
        print("Usage: python search_posts.py <keyword> [max_results]")
        print("Example: python search_posts.py 'artificial intelligence' 10")
        return
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"🚀 Facebook Post Search Starting...")
    print(f"📝 Keyword: '{keyword}'")
    print(f"📊 Max Results: {max_results}")
    print("=" * 50)
    
    # Perform the search
    results = search_facebook_posts(keyword, max_results)
    
    # Format the final output
    final_output = format_results_summary(results, keyword)
    
    # Print results
    print("\n" + "=" * 50)
    print("🎯 SEARCH RESULTS SUMMARY")
    print("=" * 50)
    print(f"Keyword: {final_output['keyword']}")
    print(f"Posts Found: {final_output['total_found']}")
    
    if final_output.get('engagement_stats'):
        stats = final_output['engagement_stats']
        print(f"Total Engagement: {stats['total_engagement']} (👍 {stats['total_likes']} | 💬 {stats['total_comments']} | 🔄 {stats['total_shares']})")
    
    print("\n📋 DETAILED RESULTS (JSON):")
    print(json.dumps(final_output, indent=2, ensure_ascii=False))
    
    # Also save to file
    output_file = f"search_results_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()