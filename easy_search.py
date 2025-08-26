#!/usr/bin/env python3
"""
Easy Facebook Post Search Interface
Simple script to search Facebook posts and get JSON results
"""

import json
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, '/workspace')

def quick_search(keyword: str, num_results: int = 10):
    """
    Quick search function that returns JSON results
    """
    print(f"🔍 Searching Facebook for: '{keyword}'")
    print(f"📊 Requesting {num_results} results")
    print("=" * 60)
    
    # Import the search function
    from search_posts import search_facebook_posts, format_results_summary
    
    # Perform search
    raw_results = search_facebook_posts(keyword, num_results)
    formatted_results = format_results_summary(raw_results, keyword)
    
    # Display summary
    print(f"✅ Search completed!")
    print(f"📈 Found: {formatted_results['total_found']} posts")
    
    if formatted_results.get('engagement_stats'):
        stats = formatted_results['engagement_stats'] 
        print(f"💬 Total engagement: {stats['total_engagement']}")
        print(f"   👍 Likes: {stats['total_likes']}")
        print(f"   💬 Comments: {stats['total_comments']}")
        print(f"   🔄 Shares: {stats['total_shares']}")
    
    print("\n📋 JSON RESULTS:")
    print("=" * 60)
    
    # Return clean JSON
    return formatted_results

# Interactive mode
if __name__ == "__main__":
    print("🚀 Facebook Post Search Tool")
    print("=" * 60)
    
    # Get keyword from user
    if len(sys.argv) >= 2:
        keyword = sys.argv[1]
        num_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    else:
        keyword = input("Enter search keyword: ").strip()
        try:
            num_results = int(input("How many results do you want? (default 10): ").strip() or "10")
        except ValueError:
            num_results = 10
    
    if not keyword:
        print("❌ No keyword provided!")
        sys.exit(1)
    
    # Perform search
    results = quick_search(keyword, num_results)
    
    # Pretty print JSON
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save to file
    filename = f"facebook_search_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")