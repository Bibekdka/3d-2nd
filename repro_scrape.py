from scraper import scrape_model_page
import json

url = "https://makerworld.com/en/models/2265463-year-of-the-horse-string-art#profileId-2468909"

print(f"Testing URL: {url}")
data = scrape_model_page(url)

if "error" in data:
    print(f"ERROR: {data['error']}")
else:
    print("SUCCESS")
    print(f"Text length: {len(data['text'])}")
    print(f"Images found: {len(data['images'])}")
    print("First 3 images:")
    for img in data['images'][:3]:
        print(img)
