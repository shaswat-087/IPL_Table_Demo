import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask,render_template

app = Flask(__name__)

def team_details():
    scraper = cloudscraper.create_scraper()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action":"parse",
        "page":"2026_Indian_Premier_League",
        "format":"json",
        "prop":"text"
    }
    headers = {"User-Agent": "IPL Bot (educational project)"}

    response = scraper.get(url,params=params,headers=headers,timeout=10)
    data = response.json()
    html = data["parse"]["text"]["*"]

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="wikitable")
    results = []

    for table in tables:
        ths = [th.get_text(strip=True) for th in table.find_all("th")]
        if "Pts" in ths and "NRR" in ths:
            for row in table.find_all("tr")[1:]:
                cols = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                if len(cols) >= 9:
                    nrr = cols[8].replace("\u2212", "-")
                    results.append({
                        "team": cols[2],
                        "played": int(cols[3]),
                        "wins": int(cols[4]),
                        "losses": int(cols[5]),
                        "nr":int(cols[6]),
                        "points": int(cols[7]),
                        "nrr": float(nrr),
                    })
            break

    return results


results = team_details()

if not results:
    print("No data found")
else:
    sorted_results = sorted(results, key=lambda t: (t["points"], t["nrr"]), reverse=True)
    print(f"\n{'Team':<35} {'Pld':<5} {'W':<4} {'L':<4} {'NR':<4} {'Pts':<5} {'NRR'}")
    print("-" * 60)
    for t in sorted_results:
        nrr = f"+{t['nrr']:.3f}" if t['nrr'] >= 0 else f"{t['nrr']:.3f}"
        print(f"{t['team']:<35} {t['played']:<5} {t['wins']:<4} {t['losses']:<4} {t['nr']:<4}{t['points']:<5} {nrr}")

TEAM_COLORS = {
    "Chennai":   {"bg": "#FFCC00", "text": "black"},
    "Mumbai":    {"bg": "#004BA0", "text": "white"},
    "Bengaluru": {"bg": "#CC0000", "text": "white"},
    "Kolkata":   {"bg": "#3A225D", "text": "gold"},
    "Rajasthan": {"bg": "#EA1A85", "text": "white"},
    "Punjab":    {"bg": "#DC1431", "text": "white"},
    "Hyderabad": {"bg": "#FF822A", "text": "black"},
    "Gujarat":   {"bg": "#1C1C1C", "text": "#B8860B"},
    "Delhi":     {"bg": "#0078BC", "text": "white"},
    "Lucknow":   {"bg": "#A72056", "text": "white"},
}

def get_color(team_name):
    for key, colors in TEAM_COLORS.items():
        if key in team_name:
            return colors
    return {"bg": "white", "text": "black"}

@app.route("/")
def home():
    standings = team_details()
    for t in standings:
     t["color"] = get_color(t["team"])

    return render_template("Table.html", standings=standings)

if __name__ == "__main__":
    app.run(debug=True)
