"""Azure Storage module for BADI Oerlikon scraper."""

from .blob_adapter import AzureBlobStorageAdapter
from .repository import AzureBlobRepository

__all__ = ['AzureBlobStorageAdapter', 'AzureBlobRepository']
