from typing import List, Optional

class Inventory:
    def __init__(self):
        self.items: List[str] = []
        self.max_items = 10  # Maximum number of items in inventory
        
    def add_item(self, item_name: str) -> bool:
        """Add an item to the inventory if there's space"""
        if len(self.items) < self.max_items:
            self.items.append(item_name)
            return True
        return False
        
    def remove_item(self, item_name: str) -> bool:
        """Remove an item from the inventory"""
        if item_name in self.items:
            self.items.remove(item_name)
            return True
        return False
        
    def has_item(self, item_name: str) -> bool:
        """Check if an item is in the inventory"""
        return item_name in self.items
        
    def combine_items(self, item1: str, item2: str) -> Optional[str]:
        """Try to combine two items and return the result if successful"""
        combinations = {
            ("cloth_oil", "jar_of_oil"): "sacred_cleaning_cloth",
            ("jar_of_oil", "cloth_oil"): "sacred_cleaning_cloth",
            ("candle_unlit", "matches"): "candle_lit",
            ("matches", "candle_unlit"): "candle_lit"
        }
        
        # Check both possible orderings
        if (item1, item2) in combinations:
            result = combinations[(item1, item2)]
            if self.remove_item(item1) and self.remove_item(item2):
                self.add_item(result)
                return result
                
        elif (item2, item1) in combinations:
            result = combinations[(item2, item1)]
            if self.remove_item(item1) and self.remove_item(item2):
                self.add_item(result)
                return result
                
        return None 