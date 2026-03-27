import requests
from bs4 import BeautifulSoup

def scrape_job_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.6 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        og_title = soup.find("meta", property="og:title")
        raw_title = og_title["content"] if og_title else ""

        if not raw_title:
            raw_title = soup.title.string if soup.title else ""

        if not raw_title:
            return "Unknown Company", "Unknown Role (Could not parse)"
        
        company = "Unknown Company"
        job_title = raw_title.strip()[:100]

        delimiters = [' | ', ' - ', ' at ', ' @ ']
        for delimiter in delimiters:
            if delimiter in raw_title:
                parts = raw_title.split(delimiter, 1)
                if len(parts) == 2:
                    job_title = parts[0].strip()
                    company = parts[1].strip()
                    break

        return company, job_title
    except requests.exceptions.RequestException as e:
        print(f"Scraping Error: {e}")
        return "Manual Entry Required", f"Protected Website: {url}"
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return "Error", "Error parsing website"