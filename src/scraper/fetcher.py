class Fetcher:
    def fetch_data(self, url):
        import requests
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text