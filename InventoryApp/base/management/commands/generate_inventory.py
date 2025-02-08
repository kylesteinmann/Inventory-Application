from django.core.management.base import BaseCommand
from base.models import InventoryItem
from django.utils import timezone
from decimal import Decimal
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generates 100 random inventory items'

    def handle(self, *args, **kwargs):
        categories = ['Electronics', 'Furniture', 'Office Supplies', 'Tools', 'Equipment']
        sub_categories = {
            'Electronics': ['Laptops', 'Phones', 'Tablets', 'Monitors', 'Accessories'],
            'Furniture': ['Chairs', 'Desks', 'Cabinets', 'Tables', 'Shelves'],
            'Office Supplies': ['Paper', 'Writing Tools', 'Organizers', 'Binders', 'Labels'],
            'Tools': ['Hand Tools', 'Power Tools', 'Measuring Tools', 'Safety Equipment', 'Storage'],
            'Equipment': ['Printers', 'Projectors', 'Cameras', 'Audio Equipment', 'Network Equipment']
        }
        brands = ['Dell', 'HP', 'Lenovo', 'Apple', 'Samsung', 'Sony', 'LG', 'Cisco', 'Herman Miller', 'Steelcase']
        colors = ['Black', 'White', 'Silver', 'Gray', 'Blue', 'Red']
        locations = ['Room 101', 'Room 102', 'Room 103', 'Storage A', 'Storage B', 'Office 1', 'Office 2', 'Lab 1', 'Lab 2']

        for i in range(100):
            category = random.choice(categories)
            sub_category = random.choice(sub_categories[category])
            
            item = InventoryItem(
                name=f"{category} - {sub_category}",
                value=Decimal(random.uniform(100.0, 5000.0)).quantize(Decimal('0.01')),
                status=random.choice([status[0] for status in InventoryItem.ITEM_STATUS]),
                category=category,
                sub_category=sub_category,
                brand=random.choice(brands),
                model=f"Model-{random.randint(1000, 9999)}",
                color=random.choice(colors),
                reorder=random.choice([True, False]),
                location=random.choice(locations),
                last_maintained=timezone.now().date() - timedelta(days=random.randint(0, 365))
            )
            item.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created item "{item.name}"')
            ) 