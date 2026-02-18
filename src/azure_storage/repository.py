"""Repository layer for Azure Blob Storage integration."""

import os
from datetime import datetime
from azure_storage.blob_adapter import AzureBlobStorageAdapter
from utils.logger import Logger


class AzureBlobRepository:
    """Repository for persisting scraped data to Azure Blob Storage."""

    def __init__(self, connection_string: str = None):
        """
        Initialize the Azure Blob repository.

        Args:
            connection_string: Azure Storage connection string
        """
        self.adapter = AzureBlobStorageAdapter(connection_string)
        self.logger = Logger()

    def save_data(self, data: dict) -> str:
        """
        Save scraped data to Azure Blob Storage.

        Args:
            data: Dictionary containing scraped data

        Returns:
            Blob name/path where data was saved
        """
        try:
            # Enhance data with metadata
            enhanced_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "source": data.get("url", "unknown"),
                "data": data,
            }

            blob_name = self.adapter.save_data(enhanced_data)
            self.logger.log_info(f"Data persisted to Azure Blob Storage: {blob_name}")
            return blob_name

        except Exception as e:
            self.logger.log_error(f"Error saving data: {e}")
            raise

    def get_latest_data(self):
        """
        Retrieve the most recently scraped data.

        Returns:
            Dictionary with latest data or None
        """
        try:
            data = self.adapter.get_latest_data()
            if data:
                self.logger.log_info("Latest data retrieved successfully")
            return data

        except Exception as e:
            self.logger.log_error(f"Error retrieving latest data: {e}")
            return None

    def get_all_blobs(self):
        """
        Retrieve list of all scraped data blobs.

        Returns:
            List of blob names
        """
        try:
            blobs = self.adapter.list_blobs(prefix="scraped_data_")
            self.logger.log_info(f"Retrieved {len(blobs)} blobs")
            return blobs

        except Exception as e:
            self.logger.log_error(f"Error listing blobs: {e}")
            return []

    def get_data_by_blob_name(self, blob_name: str):
        """
        Retrieve data by specific blob name.

        Args:
            blob_name: Name of the blob to retrieve

        Returns:
            Dictionary with blob data
        """
        try:
            data = self.adapter.retrieve_data(blob_name)
            return data

        except Exception as e:
            self.logger.log_error(f"Error retrieving data for blob {blob_name}: {e}")
            return None
