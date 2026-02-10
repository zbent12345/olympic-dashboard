import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_olympics():
    # Target URLs (ESPN's Winter Games structure)
    MEDAL_URL = "https://www.espn.com/olympics/winter/2026/medals"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 1. SCRAPE MEDALS
    response = requests.get(MEDAL_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    standings = []
    # ESPN table parsing logic
    rows = soup.select('tr.Table__TR')
    for row in rows[1:]: # Skip header
        cols = row.find_all('td')
        if len(cols) >= 5:
            country_name = cols[0].text.strip()
            standings.append({
                "rank": len(standings) + 1,
                "name": country_name,
                "g": int(cols[1].text or 0),
                "s": int(cols[2].text or 0),
                "b": int(cols[3].text or 0),
                "total": int(cols[4].text or 0)
            })

    # 2. FIND TODAY'S FINALS (MOCK/SIMULATED FOR THIS EXAMPLE)
    # Note: Real scraping of schedules varies by day, so we look for "Gold" or "Final"
    events = [
        {"sport": "Alpine Skiing", "event": "Men's Downhill", "winner": "Beat Feuz (SUI)", "usa": True},
        {"sport": "Figure Skating", "event": "Men's Short Program", "winner": "Nathan Chen (USA)", "usa": True},
        {"sport": "Short Track", "event": "Women's 500m", "winner": "Arianna Fontana (ITA)", "usa": False}
    ]

    final_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "standings": standings,
        "events": events
    }

    with open('data.json', 'w') as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    scrape_olympics()
