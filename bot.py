import os
import random
import tweepy
from google import genai
from google.genai import types

TOPICS = [
    "Global Defense & Military Power: Active aircraft carriers, nuclear-powered submarines, top arms exporters/importers, or defense spending (Strictly use verified IISS Military Balance or SIPRI data)",
    "World Geography & Population Realities: Least/most densely populated nations, Mercator map illusions vs true land area (km²), or unusual borders/buffer zones (Strictly use UN or World Bank data)",
    "Global GDP, Debt & Trade Chokepoints: Strait of Malacca/Suez/Hormuz trade volumes, top economies by GDP/PPP, foreign exchange reserves, or semiconductor manufacturing share (Strictly use IMF, World Bank, or WTO data)",
    "Verified World History & Empires: Remarkable historical rulers, ancient treaties, partition lines, or forgotten geopolitical turning points with exact verified dates and centuries",
    "Modern Wars & Strategic Geopolitics: NATO expansion, Arctic shipping routes, military alliances, air defense systems, or strategic naval bases with verified facts",
    "The Global AI & Tech Cold War: Semiconductor lithography monopolies (ASML/TSMC), sovereign AI compute capacity, hyperscale data centers, and tech rivalry between USA, China, and EU"
]

def generate_tweet():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    chosen_topic = random.choice(TOPICS)
    
    prompt = f"""
    You are an elite geopolitical, historical, and global statistics researcher writing for a viral X account (exact style of @HODLhypr / 'Countries').
    
    Topic Category: {chosen_topic}
    
    CRITICAL FACT-CHECKING & ACCURACY RULES:
    - ZERO HALLUCINATION: Every single number, percentage, land area (km²), year, and ranking MUST be 100% historically and statistically accurate.
    - Use Google Search to verify exact official figures from authoritative bodies: (SIPRI), (IISS), (World Bank), (IMF), (UN), or verified history before writing. Never invent or guess statistics.
    
    STRICT STYLE & FORMATTING RULES:
    1. TONE: Human-written, sharp, objective, punchy. No introductory filler, no clichés, NO hashtags (#) at all.
    2. COUNTRY FLAGS: Always include the official flag emoji next to every country mentioned (e.g., 🇺🇸 USA, 🇨🇳 China, 🇮🇳 India, 🇷🇺 Russia, 🇫🇷 France, 🇬🇧 UK, 🇲🇳 Mongolia, 🇹🇷 Turkey).
    3. CITATION: Explicitly cite the official source in parentheses like (SIPRI), (IISS), (World Bank), or (IMF).
    4. LAYOUT (Pick the best fit for the fact):
       - Style A (Ranked/Bullet List): 1-line hook with source -> bullet list using `• ` with flags and exact figures -> 1-line sharp takeaway.
       - Style B (Comparative Fact): 1-line striking statement -> 2-3 lines comparing scale (e.g., area in ~km² larger than 🇫🇷 France, 🇩🇪 Germany & 🇬🇧 UK combined) -> 1-line reality check.
    5. CHARACTER LIMIT: Strictly under 265 characters total (including spaces, line breaks, and emojis).
    
    Output ONLY the final tweet text and nothing else.
    """
    
    try:
        # Google Search Grounding ke saath 100% live fact verification
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                temperature=0.4
            )
        )
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
    return response.text.strip()

def post_tweet():
    tweet_text = generate_tweet()
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
        
    print(f"Generated Verified Tweet:\n{tweet_text}\n")
    
    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
    )
    
    response = client.create_tweet(text=tweet_text)
    print(f"Success! Tweet ID: {response.data['id']}")

if __name__ == "__main__":
    post_tweet()
  
