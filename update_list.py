import requests
import re

def get_coi_data():
    url = "https://www.coi.cz/pro-spotrebitele/rizikove-e-shopy/"
    domains = set()
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=30)
        r.encoding = 'utf-8'
        
        # Tato část najde domény v textu stránky ČOI spolehlivěji
        # Hledáme text mezi tagy, které ČOI používá pro názvy e-shopů
        found = re.findall(r'<span>([a-z0-9.-]+\.[a-z]{2,10})</span>', r.text.lower())
        
        for d in found:
            clean = d.strip()
            if '.' in clean and len(clean) > 3:
                domains.add(clean)
    except Exception as e:
        print(f"Chyba při stahování: {e}")
    return domains

if __name__ == "__main__":
    domains = get_coi_data()
    # Seřadíme a přidáme formát pro AdGuard ||...^
    final_list = sorted([f"||{d}^" for d in domains])

    if final_list:
        with open("blocklist.txt", "w", encoding="utf-8") as f:
            f.write("! Title: Rizikove e-shopy COI.cz\n")
            f.write(f"! Total items: {len(final_list)}\n")
            f.write("! Last update: 2026\n\n")
            f.write("\n".join(final_list))
        print(f"Hotovo! Nalezeno {len(final_list)} domén.")
    else:
        print("Chyba: Seznam je prázdný!")
