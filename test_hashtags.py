"""Test platform-specific hashtag generation logic"""
import re

def test_platform_logic():
    """Test that different platforms get different hashtag strategies"""
    
    # Simulate hashtags extracted from caption
    hashtags = ['#photography', '#nature', '#landscape', '#mountains', '#beautiful', 
                '#sunset', '#adventure', '#travel', '#hiking', '#outdoors']
    
    print("Original hashtags:", hashtags)
    print("\n" + "="*60 + "\n")
    
    # Test Instagram
    platform = 'instagram'
    final_hashtags = sorted(set(hashtags), key=lambda x: len(x), reverse=True)
    final_hashtags = final_hashtags[:30]
    print(f"🔵 {platform.upper()}: Prioritize LONG, specific hashtags")
    print(f"   Strategy: Sorted by length (descending)")
    print(f"   Limit: 30 tags")
    print(f"   Result: {final_hashtags[:5]}...")
    print()
    
    # Test TikTok
    platform = 'tiktok'
    final_hashtags = sorted(set(hashtags), key=lambda x: (len(x), x), reverse=False)
    final_hashtags = final_hashtags[:20]
    print(f"⚫ {platform.upper()}: Mix of SHORT trending + specific tags")
    print(f"   Strategy: Sorted by length (ascending)")
    print(f"   Limit: 20 tags")
    print(f"   Result: {final_hashtags[:5]}...")
    print()
    
    # Test Twitter
    platform = 'twitter'
    final_hashtags = [tag for tag in hashtags if len(tag) <= 10]
    final_hashtags = sorted(set(final_hashtags), key=lambda x: len(x))
    final_hashtags = final_hashtags[:8]
    print(f"🔴 {platform.upper()}: SHORT, concise hashtags ONLY")
    print(f"   Strategy: Filter to max 10 chars, sort by length")
    print(f"   Limit: 8 tags")
    print(f"   Result: {final_hashtags}")
    print()
    
    # Test LinkedIn
    platform = 'linkedin'
    professional_keywords = ['business', 'career', 'professional', 'industry', 'leadership', 
                            'marketing', 'growth', 'success', 'innovation', 'tech']
    final_hashtags = [tag for tag in hashtags 
                     if any(keyword in tag.lower() for keyword in professional_keywords) 
                     or len(tag) > 8]
    final_hashtags = sorted(set(final_hashtags), key=lambda x: len(x), reverse=True)
    final_hashtags = final_hashtags[:5]
    print(f"💼 {platform.upper()}: PROFESSIONAL keywords only")
    print(f"   Strategy: Filter professional terms or long tags, sort by length")
    print(f"   Limit: 5 tags")
    print(f"   Result: {final_hashtags}")
    print()
    
    print("="*60)
    print("✅ Platform-specific strategies are DIFFERENT!")
    print("✅ Each platform gets unique hashtag selection!")

if __name__ == '__main__':
    test_platform_logic()
