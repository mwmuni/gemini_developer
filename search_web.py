# search_web.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def search_web(query, num_results=10):
    """
    Searches the web using Bing.

    Args:
        query: The search query.
        num_results: The maximum number of results to return.

    Returns:
        A list of search results as dictionaries with keys 'title', 'url', and 'snippet'.
    """

    response = make_request(query)

    search_results = []
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the search results as a list of dicts
    results = soup.find_all("div", class_="result__body")
    for i, result in enumerate(results):
        if i == num_results:
            break

        title_tag = result.find("a", class_="result__a")
        title = title_tag.get_text()
        url = title_tag["href"]
        snippet_tag = result.find("a", class_="result__snippet")
        snippet = snippet_tag.get_text() if snippet_tag else ""

        search_results.append({"title": title, "url": url, "snippet": snippet})
    
    return search_results

def make_request(query):
    search_url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    print(search_url)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(search_url, headers=headers, allow_redirects=True)
    response.raise_for_status()
    return response

def dump_page_text(urls: list[str]):
  results = ""
  for url in urls:
    response = make_request(url)

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    results += f"{url}\n{text}\n\n"
  return results

if __name__ == "__main__":
  import argparse
  # We want to allow the user to specify the number of search results
  parser = argparse.ArgumentParser(description="Search the web using Bing.")
  parser.add_argument("query", help="The search query.")
  parser.add_argument("--num-results", type=int, default=10, help="The number of search results to return.")
  # Add flag for getting the text from the pages
  parser.add_argument("--text", action="store_true", help="Get the text from the search results.")
  args = parser.parse_args()
  
  search_results = search_web(args.query, args.num_results)
  print(search_results)
  urls = [result["url"] for result in search_results]
  if args.text:
    page_text = dump_page_text(urls)
    print(page_text)
