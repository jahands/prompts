#!/usr/bin/env python3
"""
Simple Inventory Management System
Python 3.11 compatible

Features:
- Add items to inventory
- Search for items
- Generate reports
- Update item quantities
- Remove items
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Item:
    """Represents an inventory item"""
    id: str
    name: str
    description: str
    quantity: int
    price: float
    category: str
    date_added: str
    last_updated: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert item to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """Create item from dictionary"""
        return cls(**data)


class InventoryManager:
    """Main inventory management class"""
    
    def __init__(self, storage_file: str = "inventory.json"):
        self.storage_file = storage_file
        self.items: Dict[str, Item] = {}
        self.load_inventory()
    
    def load_inventory(self) -> None:
        """Load inventory from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.items = {
                        item_id: Item.from_dict(item_data)
                        for item_id, item_data in data.items()
                    }
                print(f"Loaded {len(self.items)} items from {self.storage_file}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading inventory: {e}")
                self.items = {}
        else:
            print("No existing inventory file found. Starting with empty inventory.")
    
    def save_inventory(self) -> None:
        """Save inventory to JSON file"""
        try:
            data = {
                item_id: item.to_dict()
                for item_id, item in self.items.items()
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Inventory saved to {self.storage_file}")
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    def add_item(self, name: str, description: str, quantity: int, 
                 price: float, category: str) -> str:
        """Add a new item to inventory"""
        # Generate unique ID
        item_id = f"{name.lower().replace(' ', '_')}_{len(self.items) + 1}"
        
        # Ensure unique ID
        while item_id in self.items:
            item_id = f"{name.lower().replace(' ', '_')}_{len(self.items) + 1}"
        
        current_time = datetime.now().isoformat()
        
        item = Item(
            id=item_id,
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category=category,
            date_added=current_time,
            last_updated=current_time
        )
        
        self.items[item_id] = item
        self.save_inventory()
        print(f"Added item: {name} (ID: {item_id})")
        return item_id
    
    def search_items(self, query: str, search_by: str = "name") -> List[Item]:
        """Search for items by name, description, or category"""
        results = []
        query_lower = query.lower()
        
        for item in self.items.values():
            if search_by == "name" and query_lower in item.name.lower():
                results.append(item)
            elif search_by == "description" and query_lower in item.description.lower():
                results.append(item)
            elif search_by == "category" and query_lower in item.category.lower():
                results.append(item)
            elif search_by == "all":
                if (query_lower in item.name.lower() or 
                    query_lower in item.description.lower() or 
                    query_lower in item.category.lower()):
                    results.append(item)
        
        return results
    
    def get_item_by_id(self, item_id: str) -> Optional[Item]:
        """Get item by ID"""
        return self.items.get(item_id)
    
    def update_quantity(self, item_id: str, new_quantity: int) -> bool:
        """Update item quantity"""
        if item_id in self.items:
            self.items[item_id].quantity = new_quantity
            self.items[item_id].last_updated = datetime.now().isoformat()
            self.save_inventory()
            print(f"Updated quantity for {self.items[item_id].name} to {new_quantity}")
            return True
        else:
            print(f"Item with ID {item_id} not found")
            return False
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from inventory"""
        if item_id in self.items:
            item_name = self.items[item_id].name
            del self.items[item_id]
            self.save_inventory()
            print(f"Removed item: {item_name} (ID: {item_id})")
            return True
        else:
            print(f"Item with ID {item_id} not found")
            return False
    
    def generate_inventory_report(self) -> str:
        """Generate comprehensive inventory report"""
        if not self.items:
            return "No items in inventory"
        
        report = ["=" * 50]
        report.append("INVENTORY REPORT")
        report.append("=" * 50)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total items: {len(self.items)}")
        report.append("")
        
        # Summary by category
        categories = {}
        total_value = 0
        
        for item in self.items.values():
            if item.category not in categories:
                categories[item.category] = {"count": 0, "total_quantity": 0, "total_value": 0}
            
            categories[item.category]["count"] += 1
            categories[item.category]["total_quantity"] += item.quantity
            categories[item.category]["total_value"] += item.quantity * item.price
            total_value += item.quantity * item.price
        
        report.append("SUMMARY BY CATEGORY:")
        report.append("-" * 30)
        for category, data in categories.items():
            report.append(f"{category}:")
            report.append(f"  Items: {data['count']}")
            report.append(f"  Total Quantity: {data['total_quantity']}")
            report.append(f"  Total Value: ${data['total_value']:.2f}")
            report.append("")
        
        report.append(f"TOTAL INVENTORY VALUE: ${total_value:.2f}")
        report.append("")
        
        # Detailed item list
        report.append("DETAILED ITEM LIST:")
        report.append("-" * 30)
        
        for item in sorted(self.items.values(), key=lambda x: x.name):
            report.append(f"ID: {item.id}")
            report.append(f"Name: {item.name}")
            report.append(f"Description: {item.description}")
            report.append(f"Category: {item.category}")
            report.append(f"Quantity: {item.quantity}")
            report.append(f"Price: ${item.price:.2f}")
            report.append(f"Total Value: ${item.quantity * item.price:.2f}")
            report.append(f"Date Added: {item.date_added}")
            report.append(f"Last Updated: {item.last_updated}")
            report.append("-" * 30)
        
        return "\n".join(report)
    
    def generate_low_stock_report(self, threshold: int = 10) -> str:
        """Generate report of items with low stock"""
        low_stock_items = [
            item for item in self.items.values()
            if item.quantity <= threshold
        ]
        
        if not low_stock_items:
            return f"No items with stock below {threshold}"
        
        report = ["=" * 50]
        report.append("LOW STOCK REPORT")
        report.append("=" * 50)
        report.append(f"Items with stock <= {threshold}:")
        report.append("")
        
        for item in sorted(low_stock_items, key=lambda x: x.quantity):
            report.append(f"⚠️  {item.name} (ID: {item.id})")
            report.append(f"    Current Stock: {item.quantity}")
            report.append(f"    Category: {item.category}")
            report.append(f"    Price: ${item.price:.2f}")
            report.append("")
        
        return "\n".join(report)


def main():
    """Main function to demonstrate the inventory system"""
    print("Simple Inventory Management System")
    print("=" * 40)
    
    # Create inventory manager
    inventory = InventoryManager()
    
    while True:
        print("\nOptions:")
        print("1. Add item")
        print("2. Search items")
        print("3. Update quantity")
        print("4. Remove item")
        print("5. Generate inventory report")
        print("6. Generate low stock report")
        print("7. List all items")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            # Add item
            name = input("Item name: ").strip()
            description = input("Description: ").strip()
            try:
                quantity = int(input("Quantity: "))
                price = float(input("Price: "))
            except ValueError:
                print("Invalid quantity or price")
                continue
            category = input("Category: ").strip()
            
            inventory.add_item(name, description, quantity, price, category)
        
        elif choice == "2":
            # Search items
            query = input("Search query: ").strip()
            search_by = input("Search by (name/description/category/all): ").strip().lower()
            
            if search_by not in ["name", "description", "category", "all"]:
                search_by = "name"
            
            results = inventory.search_items(query, search_by)
            
            if results:
                print(f"\nFound {len(results)} item(s):")
                for item in results:
                    print(f"- {item.name} (ID: {item.id}, Qty: {item.quantity})")
            else:
                print("No items found")
        
        elif choice == "3":
            # Update quantity
            item_id = input("Item ID: ").strip()
            try:
                new_quantity = int(input("New quantity: "))
                inventory.update_quantity(item_id, new_quantity)
            except ValueError:
                print("Invalid quantity")
        
        elif choice == "4":
            # Remove item
            item_id = input("Item ID: ").strip()
            inventory.remove_item(item_id)
        
        elif choice == "5":
            # Generate inventory report
            report = inventory.generate_inventory_report()
            print("\n" + report)
            
            # Optionally save to file
            save_file = input("\nSave report to file? (y/n): ").strip().lower()
            if save_file == 'y':
                filename = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(report)
                print(f"Report saved to {filename}")
        
        elif choice == "6":
            # Generate low stock report
            try:
                threshold = int(input("Low stock threshold (default 10): ") or "10")
            except ValueError:
                threshold = 10
            
            report = inventory.generate_low_stock_report(threshold)
            print("\n" + report)
        
        elif choice == "7":
            # List all items
            if not inventory.items:
                print("No items in inventory")
            else:
                print("\nAll items:")
                for item in sorted(inventory.items.values(), key=lambda x: x.name):
                    print(f"- {item.name} (ID: {item.id}, Qty: {item.quantity}, "
                          f"Price: ${item.price:.2f}, Category: {item.category})")
        
        elif choice == "8":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()