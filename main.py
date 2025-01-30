import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        return response.text
    except requests.RequestException as e:
        print(f"Failed to retrieve content from {url}: {e}")
        return None

def parse_html(content):
    return BeautifulSoup(content, 'lxml')


def search_information(soup, query):
    # Поиск по тексту или заголовкам
    results = soup.find_all(string=lambda text: query.lower() in text.lower() if text else False)
    return results


def search_in_site(url, query):
    page_content = fetch_page_content(url)
    if not page_content:
        return []

    soup = parse_html(page_content)
    return search_information(soup, query)


def fetch_results_from_all_sites(query):
    sites = [
        "https://www.itmo.ru",
        "https://минобрнауки.рф",
        "https://news.itmo.ru/"
    ]
    overall_results = {}

    for site in sites:
        results = search_in_site(site, query)
        overall_results[site] = results

    return overall_results


# Пример использования:
query = "Университет ИТМО достижения"
results = fetch_results_from_all_sites(query)

for site, results in results.items():
    print(f"Results from {site}:")
    for result in results:
        print("-", result.strip())  # Вывод и очистка пробелов