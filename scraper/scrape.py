import requests
from bs4 import BeautifulSoup
import json

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

assessment_links = []

for link in links:
    text = link.text.strip()
    href = link.get("href")

    if href and "/products/product-catalog/view/" in href:

        full_url = "https://www.shl.com" + href

        assessment_links.append({
            "name": text,
            "url": full_url
        })

# Remove duplicates
unique_links = []
seen = set()

for item in assessment_links:
    if item["url"] not in seen:
        seen.add(item["url"])
        unique_links.append(item)

print("Total Assessments Found:", len(unique_links))

# Save JSON file
with open("data/shl_catalog.json", "w", encoding="utf-8") as f:
    json.dump(unique_links, f, indent=4)

print("Data saved to data/shl_catalog.json")