from abc import ABC, abstractmethod

class SteamDataSource(ABC):
    """
    Abstract base class for all Steam data sources.
    Defines the interface for fetching and parsing Steam-related data.
    """
    @abstractmethod
    def get_data(self, identifier: str | int, **kwargs):
        """
        Abstract method to fetch and parse data from a specific source.
        
        Args:
            identifier: The primary identifier for the data (e.g., game URL, AppID, API method name).
            **kwargs: Additional keyword arguments specific to the data source (e.g., language).

        Returns:
            A dictionary containing the parsed data, or None if data could not be fetched/parsed.
        """
        pass

    def parse_static_content(self, content: str, **kwargs):
        raise NotImplementedError("This data source does not support parsing HTML content directly.")
