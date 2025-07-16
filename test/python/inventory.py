"""
Simple Inventory Management System

A basic inventory management system that can add items, search for them,
and generate reports. Uses modern Python type annotations (PEP 585).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol, Any
import json


@dataclass
class Item:
    """Represents an inventory item."""
    id: int
    name: str
    description: str
    quantity: int
    price: float
    category: str
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert item to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Item':
        """Create item from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            quantity=data['quantity'],
            price=data['price'],
            category=data['category'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )


class SearchCriteria(Protocol):
    """Protocol for search criteria."""
    def matches(self, item: Item) -> bool:
        """Check if item matches the search criteria."""
        ...


@dataclass
class NameSearch:
    """Search by item name."""
    name: str
    case_sensitive: bool = False

    def matches(self, item: Item) -> bool:
        if self.case_sensitive:
            return self.name in item.name
        return self.name.lower() in item.name.lower()


@dataclass
class CategorySearch:
    """Search by item category."""
    category: str
    case_sensitive: bool = False

    def matches(self, item: Item) -> bool:
        if self.case_sensitive:
            return self.category == item.category
        return self.category.lower() == item.category.lower()


@dataclass
class PriceRangeSearch:
    """Search by price range."""
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    def matches(self, item: Item) -> bool:
        if self.min_price is not None and item.price < self.min_price:
            return False
        if self.max_price is not None and item.price > self.max_price:
            return False
        return True


@dataclass
class QuantitySearch:
    """Search by quantity threshold."""
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None

    def matches(self, item: Item) -> bool:
        if self.min_quantity is not None and item.quantity < self.min_quantity:
            return False
        if self.max_quantity is not None and item.quantity > self.max_quantity:
            return False
        return True


class InventoryManager:
    """Manages inventory items with add, search, and reporting capabilities."""

    def __init__(self) -> None:
        self.items: dict[int, Item] = {}
        self.next_id: int = 1

    def add_item(self, name: str, description: str, quantity: int, 
                 price: float, category: str) -> Item:
        """Add a new item to inventory."""
        now = datetime.now()
        item = Item(
            id=self.next_id,
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category=category,
            created_at=now,
            updated_at=now
        )
        self.items[self.next_id] = item
        self.next_id += 1
        return item

    def update_item(self, item_id: int, **kwargs) -> Optional[Item]:
        """Update an existing item."""
        if item_id not in self.items:
            return None
        
        item = self.items[item_id]
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        item.updated_at = datetime.now()
        return item

    def remove_item(self, item_id: int) -> bool:
        """Remove an item from inventory."""
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

    def get_item(self, item_id: int) -> Optional[Item]:
        """Get an item by ID."""
        return self.items.get(item_id)

    def search_items(self, criteria: SearchCriteria) -> list[Item]:
        """Search for items matching given criteria."""
        return [item for item in self.items.values() if criteria.matches(item)]

    def get_all_items(self) -> list[Item]:
        """Get all items in inventory."""
        return list(self.items.values())

    def get_categories(self) -> set[str]:
        """Get all unique categories."""
        return {item.category for item in self.items.values()}

    def get_low_stock_items(self, threshold: int = 10) -> list[Item]:
        """Get items with quantity below threshold."""
        return [item for item in self.items.values() if item.quantity < threshold]

    def generate_inventory_report(self) -> dict[str, Any]:
        """Generate a comprehensive inventory report."""
        items = list(self.items.values())
        
        if not items:
            return {
                'total_items': 0,
                'total_value': 0.0,
                'categories': {},
                'low_stock_items': [],
                'average_price': 0.0,
                'generated_at': datetime.now().isoformat()
            }

        total_value = sum(item.price * item.quantity for item in items)
        categories = {}
        
        for item in items:
            if item.category not in categories:
                categories[item.category] = {
                    'count': 0,
                    'total_quantity': 0,
                    'total_value': 0.0
                }
            
            categories[item.category]['count'] += 1
            categories[item.category]['total_quantity'] += item.quantity
            categories[item.category]['total_value'] += item.price * item.quantity

        return {
            'total_items': len(items),
            'total_value': total_value,
            'categories': categories,
            'low_stock_items': [item.to_dict() for item in self.get_low_stock_items()],
            'average_price': sum(item.price for item in items) / len(items),
            'generated_at': datetime.now().isoformat()
        }

    def export_to_json(self, filename: str) -> bool:
        """Export inventory to JSON file."""
        try:
            data = {
                'items': [item.to_dict() for item in self.items.values()],
                'next_id': self.next_id,
                'exported_at': datetime.now().isoformat()
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def import_from_json(self, filename: str) -> bool:
        """Import inventory from JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.items = {}
            for item_data in data['items']:
                item = Item.from_dict(item_data)
                self.items[item.id] = item
            
            self.next_id = data['next_id']
            return True
        except Exception:
            return False


def main():
    """Demo function showing inventory system usage."""
    inventory = InventoryManager()
    
    # Add sample items
    inventory.add_item("Laptop", "Dell XPS 13", 10, 999.99, "Electronics")
    inventory.add_item("Mouse", "Wireless optical mouse", 50, 29.99, "Electronics")
    inventory.add_item("Desk", "Standing desk", 5, 299.99, "Furniture")
    inventory.add_item("Chair", "Ergonomic office chair", 8, 199.99, "Furniture")
    inventory.add_item("Notebook", "Spiral notebook", 100, 2.99, "Stationery")
    
    # Search examples
    print("=== Search Examples ===")
    
    # Search by name
    name_results = inventory.search_items(NameSearch("Laptop"))
    print(f"Items with 'Laptop' in name: {len(name_results)}")
    
    # Search by category
    electronics = inventory.search_items(CategorySearch("Electronics"))
    print(f"Electronics items: {len(electronics)}")
    
    # Search by price range
    expensive_items = inventory.search_items(PriceRangeSearch(min_price=100.0))
    print(f"Items over $100: {len(expensive_items)}")
    
    # Search by low stock
    low_stock = inventory.search_items(QuantitySearch(max_quantity=10))
    print(f"Low stock items (≤10): {len(low_stock)}")
    
    # Generate report
    print("\n=== Inventory Report ===")
    report = inventory.generate_inventory_report()
    print(f"Total items: {report['total_items']}")
    print(f"Total value: ${report['total_value']:.2f}")
    print(f"Average price: ${report['average_price']:.2f}")
    print(f"Categories: {list(report['categories'].keys())}")
    print(f"Low stock items: {len(report['low_stock_items'])}")


if __name__ == "__main__":
    main()