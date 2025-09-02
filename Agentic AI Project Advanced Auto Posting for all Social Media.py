from google.generativeai import configure as genai_configure
from google.generativeai import GenerativeModel
from mastodon import Mastodon
from googlesearch import search
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import os
import random
import requests

GOOGLE_API_KEY = 'write your api'
ACCESS_TOKEN = 'yourapi'
CLIENT_KEY = 'if necessary'
CLIENT_SECRET = 'if necessary'
API_BASE_URL = 'https://mastodon.social'
UNSPLASH_ACCESS_KEY = 'your api' 

genai_configure(api_key=GOOGLE_API_KEY)
try:
    model = GenerativeModel('gemini-2.0-flash')
except Exception as e:
    raise RuntimeError(f"Failed to load gemini-2.0-flash: {e}") from e

mastodon = Mastodon(
    client_id=CLIENT_KEY,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
    api_base_url=API_BASE_URL.strip()
)

query = "latest technology trends 2025 software engineering"
print("🔎 Searching online for fresh content...")
try:
    search_results = list(search(query, num_results=3, lang='en', advanced=False))
    context_urls = "\n".join([f"- {url}" for url in search_results])
except Exception as e:
    context_urls = "(Could not fetch live results, fallback to internal knowledge)"
    print("⚠️ Search warning:", str(e))

prompt = f"""
You are a helpful agent named AutoPulse AI.
My name is Jawad Naseer.

Based on the following sources:
{context_urls}

Choose the best and unique, most recent topic related to software engineering. Then generate 3 variations. For each:
1. A compelling clean title (no word 'title').
2. Write a professional, human-like short article of about 50 words.
3. Suggest 3-5 relevant hashtags.

Output format:
---
Title: ...
Article: ...
Hashtags: ...
---
"""

print("✨ Generating article variations with Gemini...")
response = model.generate_content(prompt)
article_text = response.text.strip()

variations = [block.strip() for block in article_text.split("---") if block.strip()]
chosen = random.choice(variations)

title, content, hashtags = "", "", ""
for line in chosen.split("\n"):
    if line.startswith("Title:"):
        title = line.replace("Title:", "").strip()
    elif line.startswith("Article:"):
        content = line.replace("Article:", "").strip()
    elif line.startswith("Hashtags:"):
        hashtags = line.replace("Hashtags:", "").strip()

print("✅ Content ready:")
print("Title:", title)
print("Article:", content)
print("Hashtags:", hashtags)

def fetch_unsplash_image(query, filename="news_post.png"):
    url = f'https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}'
    try:
        response = requests.get(url).json()
        img_url = response['urls']['regular']
        img_data = requests.get(img_url).content
        with open(filename, 'wb') as f:
            f.write(img_data)
        return filename
    except Exception as e:
        print("⚠️ Could not fetch Unsplash image, fallback to gradient.", str(e))
        return None

image_file = fetch_unsplash_image(title)

def overlay_text_on_image(title, content, image_file):
    W, H = 1200, 628
    text_color = (255, 255, 255)

    if image_file and os.path.exists(image_file):
        base = Image.open(image_file).convert("RGBA")
    else:
        base = Image.new("RGBA", (W, H), (25, 118, 210))

    draw = ImageDraw.Draw(base)

    overlay = Image.new('RGBA', base.size, (0,0,0,0))
    draw_overlay = ImageDraw.Draw(overlay)

    title_box = (0, 60, W, 220)
    draw_overlay.rectangle(title_box, fill=(0,0,0,120))

    article_box = (0, 240, W, 550)
    draw_overlay.rectangle(article_box, fill=(0,0,0,100))

    overlay = overlay.filter(ImageFilter.GaussianBlur(3))
    base = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(base)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 60)
        font_body = ImageFont.truetype("arial.ttf", 36)
    except:
        font_title = font_body = ImageFont.load_default()

    wrapped_title = textwrap.fill(title, width=26)
    title_bbox = draw.multiline_textbbox((50, 60), wrapped_title, font=font_title)
    draw.multiline_text(
        ((W - (title_bbox[2]-title_bbox[0])) / 2, 80),
        wrapped_title,
        font=font_title,
        fill=text_color,
        align="center"
    )

    wrapped_body = textwrap.fill(content, width=45)
    draw.multiline_text(
        (60, 260),
        wrapped_body,
        font=font_body,
        fill=text_color,
        align="left"
    )

    output_file = "final_news_post.png"
    base.convert('RGB').save(output_file)
    return output_file

image_file = overlay_text_on_image(title, content, image_file)

status_text = f"{title}\n\n{hashtags}"

print("🚀 Posting to Mastodon...")
try:
    media = mastodon.media_post(image_file, description=title)
    print("✅ Media uploaded:", media)
    mastodon.status_post(status=status_text, media_ids=[media['id']])
    print("✅ Posted successfully with full-width blurred semi-transparent overlay and relevant Unsplash image!")
except Exception as e:
    print("❌ Failed to post:", str(e))
finally:
    if os.path.exists(image_file):
        os.remove(image_file)  
