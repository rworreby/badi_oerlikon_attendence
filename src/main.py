from scraper.fetcher import Fetcher
from scraper.parser import Parser
from db.repository import Repository
from db.session import create_session
from utils.logger import Logger


def main():
    logger = Logger()
    logger.log_info("Starting the historical data scraper...")

    # Initialize components
    fetcher = Fetcher()
    parser = Parser()
    repository = Repository(create_session())

    # Define the URL to scrape
    url = "https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder/oerlikon.html"

    try:
        # Fetch data from the URL
        html_data = fetcher.fetch_data(url)
        logger.log_info("Data fetched successfully.")

        # Parse the fetched HTML data
        parsed_data = parser.parse_html(html_data)
        logger.log_info("Data parsed successfully.")

        # Save the parsed data to the database
        repository.save_data(parsed_data)
        logger.log_info("Data saved to the database successfully.")

    except Exception as e:
        logger.log_error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()