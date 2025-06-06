from PriceTracker import PriceTracker
from datetime import datetime,timedelta

class MarketTracker(PriceTracker):
    """A class for tracking prices of multiple assets in a market.

    This class maintains a collection of  PriceTracker instances, one for each
    asset being tracked in the market.

    Attributes:
        _trackers (dict): Dictionary mapping asset names to PriceTracker instances.
    """
    def __init__(self):
        """Initilises a new MarketTracker.
        """
        self._trackers = {}

    
    def add_price(self, name: str, time: datetime, price: float):
        """Add price data for specified asset at given time.

        If asset does not exist in the tracker dictionary, a new PriceTracker is created.

        Args:
            name (str): The name of the asset being tracked.
            time (datetime): The time at which the price was recorded.
            price (float): The price value to be added.
        """
        if name not in self._trackers:
            self._trackers[name] = PriceTracker()
        
        self._trackers[name].add_price(time,price)
    

    def get_price_data(self, name: str, start: datetime, end: datetime):
        """Get price data for specified asset within given time frame.

        Args:
            name (str): The name of the asset being tracked.
            start (datetime): The start of the time interval.
            end (datetime): The end of the time interval.
        
        Returns:
            list: A list of tuples containing the price data over given time range.

        Raises:
            KeyError: If specified asset is not found in the tracker.
        """
        if name not in self._trackers:
            raise KeyError('Asset {name} not found in Market Tracker!')
        
        price_data = self._trackers[name].get_price_data(start,end)

        return price_data