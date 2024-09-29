import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# for loading a page by URL
def download_page(url):
    try:
        # get request
        response = requests.get(url)
        response.raise_for_status()  # Checking for the success
        return response.text  # return HTML
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


# search for all links on the page
def find_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set() # to store unique links

    # soup.find_all - search (<a> and href)
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)  # relative links to absolute ones
        links.add(full_url) # add to set

    return links


# page loading and link search
def crawl(url, visited=set(), depth=2):
    if depth == 0 or url in visited:
        return

    print(f"Webpage is loading: {url}")
    html = download_page(url)

    if html: # check
        links = find_links(html, url)
        visited.add(url) # to visited url
        print(f"{len(links)} links found on the webpage {url}:")
        for link in links:
            print(link)

        # searched
        for link in links:
            crawl(link, visited, depth - 1)


if __name__ == "__main__":
    start_url = "https://books.toscrape.com/"  # start url
    crawl(start_url)
