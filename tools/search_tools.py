import json
import os
import requests
from langchain.tools import tool


class SearchTools:

    @tool("Search internet")
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant results."""
        # Ensure the query is a string
        if not isinstance(query, str):
            query = str(query)  # Convert to string if not already
        return SearchTools.search(query)

    @tool("Search instagram")
    def search_instagram(query):
        """Useful to search for Instagram posts about a given topic and return relevant results."""
        # Ensure the query is a string
        if not isinstance(query, str):
            query = str(query)  # Convert to string if not already
        # Modify the query to focus on Instagram by adding "site:instagram.com"
        instagram_query = f"site:instagram.com {query}"
        return SearchTools.search(instagram_query)

    @staticmethod
    def search(query, n_results=5):
        """Executes a search query using the Serper API and returns formatted results."""
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'Content-Type': 'application/json'
        }

        try:
            # Send the request to the Serper API
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.exceptions.RequestException as e:
            return f"Error fetching search results: {e}"

        try:
            # Parse the JSON response
            results = response.json().get('organic', [])
        except json.JSONDecodeError:
            return "Error parsing JSON response."

        # Build the result string from the obtained search results
        result_strings = []
        for result in results[:n_results]:
            title = result.get('title', 'No Title')
            link = result.get('link', 'No Link')
            snippet = result.get('snippet', 'No Snippet')
            result_strings.append('\n'.join([
                f"Title: {title}", f"Link: {link}", f"Snippet: {snippet}", "\n-----------------"
            ]))

        content = '\n'.join(result_strings)
        return f"\nSearch result: {content}\n"
