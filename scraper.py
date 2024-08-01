import requests
from bs4 import BeautifulSoup

URL = 'https://pratham.org/'

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        if href.startswith("/"):
            section_url = f"{url}{href}"
        elif href.startswith('http'):
            section_url = href
        else:
            continue
        all_links.append(section_url)
    return set(all_links)


def extract_single_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        content = {
            'headers': [header.get_text(strip=True) for header in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraphs': [para.get_text(strip=True) for para in soup.find_all('p')],
        }
        
        return content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {'headers': [], 'paragraphs': []}
    

def extract_all_links(links):
    all_content = []
    
    for link in links:
        content = extract_single_link(link)
        all_content.append(content)
    
    return all_content


def clean_and_combine(all_content):
    all_paragraphs = []

    for data in all_content:
        data['paragraphs'] = [para for para in data['paragraphs'] if len(para) >= 40]
        all_paragraphs.extend(para_list for para_list in data['paragraphs'])

        
    return all_paragraphs


def run_scraper():
    links = get_links(URL)

    content = extract_all_links(links)

    all_paragraphs = clean_and_combine(content)

    return all_paragraphs