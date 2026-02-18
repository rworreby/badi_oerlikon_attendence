"""
Azure Function for crawling pool occupancy data on a schedule.
Triggered by timer every hour.
"""

import azure.functions as func
import logging
import sys
import os
import time

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scraper.fetcher import Fetcher
from scraper.parser import Parser
from azure_storage.repository import AzureBlobRepository
from utils.logger import Logger


def main(mytimer: func.TimerRequest) -> None:
    """
    Azure Function timer trigger that runs the crawler every hour.

    Azure Functions Timeout: 10 minutes max (Consumption Plan)
    Expected execution: ~2-4 seconds

    Args:
        mytimer: Timer trigger object with schedule and isPastDue info
    """
    logger = Logger()
    start_time = time.time()

    if mytimer.past_due:
        logger.log_info("Timer is past due!")

    logger.log_info(f"Crawler function triggered at {mytimer.trigger_time}")

    try:
        # Initialize components
        fetcher = Fetcher()
        parser = Parser()
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        repository = AzureBlobRepository(connection_string)

        # Get URL from environment
        url = os.getenv(
            "SCRAPE_URL",
            "https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/"
            "sport-und-badeanlagen/hallenbaeder/oerlikon.html",
        )

        logger.log_info(f"Starting scrape from: {url}")

        # Fetch data
        fetch_start = time.time()
        html_data = fetcher.fetch_data(url)
        fetch_time = time.time() - fetch_start
        logger.log_info(f"Data fetched successfully in {fetch_time:.2f}s")

        # Parse data
        parse_start = time.time()
        parsed_data = parser.parse_html(html_data)
        parse_time = time.time() - parse_start
        logger.log_info(f"Data parsed successfully in {parse_time:.2f}s")

        # Save to blob storage
        save_start = time.time()
        blob_name = repository.save_data(parsed_data)
        save_time = time.time() - save_start
        logger.log_info(f"Data saved to blob storage in {save_time:.2f}s: {blob_name}")

        total_time = time.time() - start_time
        logger.log_info(
            f"Crawler execution completed successfully in {total_time:.2f}s"
        )

    except Exception as e:
        total_time = time.time() - start_time
        logger.log_error(f"Error during crawler execution after {total_time:.2f}s: {e}")
        raise
