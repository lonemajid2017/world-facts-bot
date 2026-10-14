import os
import random
import sys
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
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY secret nahi mila!")

    client = genai.Client(api_key=api_key)
    chosen_topic = random.choice(TOPICS)

    prompt = f"""You are an elite geopolitical, historical, and global statistics researcher writing for a viral X account (exact style of @HODLhypr / 'Countries').

Topic Category: {chosen_topic}

CRITICAL FACT-CHECKING & ACCURACY RULES:
- ZERO HALLUCINATION: Every single number, percentage, land area (km²), year, and ranking MUST be 100% historically and statistically accurate.
- Verify exact official figures from authoritative bodies: (SIPRI), (IISS), (World Bank), (IMF), (UN), or verified history before writing. Never invent or guess statistics.

STRICT STYLE & FORMATTING RULES:
1. TONE: Human-written, sharp, objective, punchy. No introductory filler, no clichés, NO hashtags (#) at all.
2. COUNTRY FLAGS: Always include the official flag emoji next to every country mentioned (e.g., 🇺🇸 USA, 🇨🇳 China, 🇮🇳 India, 🇷🇺 Russia, 🇫🇷 France, 🇬🇧 UK, 🇲🇳 Mongolia, 🇹🇷 Turkey).
3. CITATION: Explicitly cite the official source in parentheses like (SIPRI), (IISS), (World Bank), or (IMF).
4. LAYOUT (Pick the best fit for the fact):
   - Style A (Ranked/Bullet List): 1-line hook with source -> bullet list using `• ` with flags and exact figures -> 1-line sharp takeaway.
   - Style B (Comparative Fact): 1-line striking statement -> 2-3 lines comparing scale (e.g., area in ~km² larger than 🇫🇷 France, 🇩🇪 Germany & 🇬🇧 UK combined) -> 1-line reality check.
5. CHARACTER LIMIT: Strictly under 250 characters total (including spaces, line breaks, and emojis).

Output ONLY the final tweet text and nothing else."""

    # Sahi models ki list (Sabse pehle gemini-3.0-flash jo Google API ne manga hai)
    candidate_models = [
        "gemini-3.0-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash"
    ]

    # Agar koi naya model ho toh khud list se dhoondh kar jodna
    try:
        for m in client.models.list():
            name = m.name.replace("models/", "")
            if ("flash" in name or "pro" in name) and all(x not in name for x in ["tts", "image", "embedding", "vision", "audio"]):
                if name not in candidate_models:
                    candidate_models.append(name)
    except Exception as e:
        print(f"Model list check note: {e}")

    last_error = None
    for model_name in candidate_models:
        # Pehle Google Search Fact-Check ke saath try karega
        try:
            print(f"Trying model: {model_name} (with Google Search verification)...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[{"google_search": {}}],
                    temperature=0.4
                )
            )
            if response and response.text:
                print(f"Success with {model_name} (Search Verified)!")
                return response.text.strip()
        except Exception as e1:
            print(f"Search mode note on {model_name}: {e1}")
            # Agar search tool us model par na chale toh normal mode mein try karega
            try:
                print(f"Trying model: {model_name} (standard mode)...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4
                    )
                )
                if response and response.text:
                    print(f"Success with {model_name}!")
                    return response.text.strip()
            except Exception as e2:
                print(f"Model {model_name} failed: {e2}")
                last_error = e2
                continue

    raise RuntimeError(f"Saare models fail hue. Last error: {last_error}")

def post_tweet():
    tweet_text = generate_tweet()
    tweet_text = tweet_text.strip().strip('"').strip("'")

    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."

    print(f"\nGenerated Verified Tweet ({len(tweet_text)} chars):\n{tweet_text}\n")

    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"].strip(),
        consumer_secret=os.environ["TWITTER_API_SECRET"].strip(),
        access_token=os.environ["TWITTER_ACCESS_TOKEN"].strip(),
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"].strip()
    )

    try:
        response = client.create_tweet(text=tweet_text)
        print(f"Success! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Twitter API Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    post_tweet()
    
