from AVLTree import AVLTree
from datetime import datetime, timedelta
from Heap import MinHeap
from BST import range_query

class PriceTracker:
    """A class for tracking price data over time with 10-day metrics:

    This class maintains a rolling window of price data, calculating the minimum, maximum
    and average prices over most recent 10 day window.

    Attributes:
        _price_tree (AVLTree): AVL Tree storing price data by datetime.
        _price_heap (MinHeap): Min heap for quick access to minimum price.
        _max_heap (MinHeap): Min heap (with negated values) for quick access to maximum price.
        _node_dict (dict): Dictionary mapping datetime to min heap nodes.
        _max_dict (dict): Dictionary mapping datetime to max heap nodes.
        _latest_time (datetime): The most recent time a price was added.
        _sum (float): Running sum of all prices in the current window.
        _count (int): Count of prices in the current window.

    
    """
    def __init__(self):
        """Initialises a new PriceTracker.
        """
        self._price_tree = AVLTree()
        self._price_heap = MinHeap()
        self._max_heap = MinHeap()
        self._node_dict = {}
        self._max_dict = {}
        self._times_list = []
        self._latest_time = None

        self._sum = 0.0
        self._count = 0
    
    def add_price(self, time: datetime, price: float):
        """Add a new price at specified time.

        This method keeps track and adds the price of the newly given 10-day window
        to the tracker. It also removes any price data that falls outside of this window.
        
        Args:
            time (datetime): The time at which the price was recorded.
            price (float): The price value to be added.
        """
        if self._latest_time is None:
            min_heap_node = self._price_heap.insert(price)
            self._node_dict[time] = min_heap_node

            max_heap_node = self._max_heap.insert(-price)
            self._max_dict[time] = max_heap_node

            self._sum += price
            self._count += 1

            
            self._price_tree.insert(time,(price,price,price,price))
            self._latest_time = time
            return
         
        new_window = time - timedelta(days=10)
        old_window = self._latest_time - timedelta(days=10)

    
        outdated_entries = range_query(self._price_tree,old_window,new_window)
        for outdated,_ in outdated_entries:
            if outdated in self._node_dict:
                min_node = self._node_dict[outdated]
            
                del self._node_dict[outdated]

                self._price_heap.delete_node(min_node)

            if outdated in self._max_dict:
                max_node = self._max_dict[outdated]
                del self._max_dict[outdated]
                self._max_heap.delete_node(max_node)
            
            self._sum -= price
            self._count -= 1
        
        min_heap_node = self._price_heap.insert(price)
        self._node_dict[time] = min_heap_node

        max_heap_node = self._max_heap.insert(-price)
        self._max_dict[time] = max_heap_node

        self._sum += price
        self._count += 1

    
        if self._price_heap.root is not None:
            ten_day_min = self._price_heap.root.key
        
        
        if self._max_heap.root is not None:
            ten_day_max = -self._max_heap.root.key
        
        if self._count > 0:
            ten_day_average = self._sum / self._count



        self._price_tree.insert(time,(price,ten_day_min,ten_day_max,ten_day_average))

        self._latest_time = time
        
    

    def get_price_data(self, start: datetime, end: datetime):
        """Get price data within specified time range.

        Args:
            start (datetime): The start of the time interval
            end (datetime): The end of the time interval.

        Returns:
            list: A list of tuples containing price data over given range.
        """
        result = range_query(self._price_tree,start,end)

        return result

            


        