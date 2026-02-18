import sys
from src.scraper.fetcher import Fetcher
from src.scraper.parser import Parser
# from src.db.repository import Repository
# from src.db.session import create_session
from src.utils.logger import Logger


def main():
    logger = Logger()
    logger.log_info("Starting the scraping process.")

    # Create a database session
    # session = create_session()
    # repository = Repository(session)

    # Define the URL to scrape
    url = "https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder/oerlikon.html"  # Replace with the actual URL

    # Fetch data from the URL
    fetcher = Fetcher()
    html_data = fetcher.fetch_data(url)

    print(html_data)
    open("fetched_page.html", "w").write(html_data)

    # Parse the fetched HTML data
    parser = Parser()
    parsed_data = parser.parse_html(html_data)

    open("scraped_data.csv", "a").write(f"{parsed_data['timestamp']},{parsed_data['occupancy']}\n")
    logger.log_info("Scraping process completed.")

    # Save the parsed data to the database
    # repository.save_data(parsed_data)
    # logger.log_info("Data has been successfully scraped and stored in the database.")

if __name__ == "__main__":
    main()