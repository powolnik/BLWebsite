from decimal import Decimal
from .models import Order, OrderItem, Component


class ConfiguratorService:
    """Logika biznesowa konfiguratora scen."""

    @staticmethod
    def add_item(order: Order, component_id: int, quantity: int = 1,
                 position_data: dict = None) -> OrderItem:
        """Dodaj komponent do zamowienia."""
        component = Component.objects.get(pk=component_id, is_available=True)
        item, created = OrderItem.objects.get_or_create(
            order=order, component=component,
            defaults={
                'quantity': quantity,
                'unit_price': component.price,
                'subtotal': component.price * quantity,
                'position_data': position_data or {},
            }
        )
        if not created:
            item.quantity += quantity
            item.subtotal = item.unit_price * item.quantity
            item.save()
        order.recalculate_total()
        return item

    @staticmethod
    def remove_item(order: Order, item_id: int) -> None:
        """Usun komponent z zamowienia."""
        OrderItem.objects.filter(pk=item_id, order=order).delete()
        order.recalculate_total()

    @staticmethod
    def update_item_quantity(order: Order, item_id: int, quantity: int) -> OrderItem:
        """Zmien ilosc komponentu."""
        item = OrderItem.objects.get(pk=item_id, order=order)
        if quantity <= 0:
            item.delete()
            order.recalculate_total()
            return None
        item.quantity = quantity
        item.save()
        order.recalculate_total()
        return item

    @staticmethod
    def submit_order(order: Order) -> Order:
        """Zloze zamowienie do recenzji."""
        if order.status != 'draft':
            raise ValueError('Tylko szkic moze byc zlozony.')
        if not order.items.exists():
            raise ValueError('Zamowienie musi zawierac min. 1 element.')
        order.status = 'submitted'
        order.save(update_fields=['status'])
        return order

    @staticmethod
    def calculate_power_summary(order: Order) -> dict:
        """Podsumowanie zuzycia mocy."""
        items = order.items.select_related('component').all()
        total_power = sum(
            item.component.power_consumption * item.quantity for item in items
        )
        total_weight = sum(
            float(item.component.weight_kg) * item.quantity for item in items
        )
        return {
            'total_power_watts': total_power,
            'total_weight_kg': round(total_weight, 2),
            'item_count': sum(item.quantity for item in items),
        }
from django.conf import settings
from .models import Order, Component, Scene3D, ComponentPlacement
import json
import os


class ConfiguratorService:
    """Service for configurator business logic."""
    
    @staticmethod
    def add_item(order, component_id, quantity=1, position_data=None):
        """Add component to order."""
        from .models import Component, OrderItem
        
        component = Component.objects.get(id=component_id)
        if quantity > component.max_quantity:
            raise ValueError(f"Maximum quantity for {component.name} is {component.max_quantity}")
        
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            component=component,
            defaults={
                'quantity': quantity,
                'position_data': position_data or {}
            }
        )
        
        if not created:
            order_item.quantity += quantity
            if order_item.quantity > component.max_quantity:
                raise ValueError(f"Maximum quantity for {component.name} is {component.max_quantity}")
            order_item.save()
        
        order.recalculate_total()
        return order_item
    
    @staticmethod
    def remove_item(order, item_id):
        """Remove item from order."""
        from .models import OrderItem
        
        OrderItem.objects.filter(order=order, id=item_id).delete()
        order.recalculate_total()
    
    @staticmethod
    def submit_order(order):
        """Submit order for review."""
        if not order.items.exists():
            raise ValueError("Cannot submit empty order")
        
        order.status = 'submitted'
        order.save()
    
    @staticmethod
    def calculate_power_summary(order):
        """Calculate power consumption and weight summary."""
        total_power = 0
        total_weight = 0
        
        for item in order.items.all():
            total_power += item.component.power_consumption * item.quantity
            total_weight += float(item.component.weight_kg) * item.quantity
        
        return {
            'total_power_w': total_power,
            'total_weight_kg': total_weight,
            'estimated_power_cost_per_hour': total_power * 0.15 / 1000,  # Rough estimate
        }


class Scene3DService:
    """Service for 3D scene composition and export."""
    
    @staticmethod
    def compose_scene(order):
        """Compose 3D scene data from order."""
        scene_data = {
            'scene': {
                'background': '#000000',
                'fog': {'near': 1, 'far': 1000, 'color': '#000000'},
                'environment': 'studio'
            },
            'camera': {
                'position': {'x': 0, 'y': 10, 'z': 20},
                'target': {'x': 0, 'y': 0, 'z': 0},
                'fov': 75
            },
            'lighting': [
                {
                    'type': 'ambient',
                    'color': '#404040',
                    'intensity': 0.4
                },
                {
                    'type': 'directional',
                    'color': '#ffffff',
                    'intensity': 1,
                    'position': {'x': 10, 'y': 10, 'z': 5}
                }
            ],
            'objects': []
        }
        
        # Add template base if exists
        if order.template:
            scene_data['objects'].append({
                'type': 'stage',
                'geometry': {
                    'type': 'box',
                    'width': float(order.template.width),
                    'height': 0.5,
                    'depth': float(order.template.depth)
                },
                'material': {
                    'color': '#333333',
                    'metalness': 0.1,
                    'roughness': 0.8
                },
                'position': {'x': 0, 'y': 0, 'z': 0}
            })
        
        # Add components
        for item in order.items.all():
            component = item.component
            position_data = item.position_data or {}
            
            for i in range(item.quantity):
                obj_data = {
                    'id': f"{component.slug}_{item.id}_{i}",
                    'name': component.name,
                    'type': 'component',
                    'category': component.category.slug,
                    'geometry': {
                        'type': 'box',  # Default, can be overridden by component data
                        'width': float(component.width_m),
                        'height': 2.0,  # Default height
                        'depth': float(component.depth_m)
                    },
                    'material': {
                        'color': component.color or component.category.color,
                        'metalness': 0.5,
                        'roughness': 0.5
                    },
                    'position': {
                        'x': position_data.get('x', i * 3),  # Spread components if no position
                        'y': position_data.get('y', 1),
                        'z': position_data.get('z', 0)
                    }
                }
                
                # Add 3D model if available
                if component.model_3d:
                    obj_data['model'] = {
                        'url': component.model_3d.url,
                        'format': component.model_format,
                        'scale': component.scale_factor
                    }
                
                scene_data['objects'].append(obj_data)
        
        return scene_data
    
    @staticmethod
    def export_scene(order, format_type='gltf'):
        """Export 3D scene in specified format."""
        scene_data = Scene3DService.compose_scene(order)
        
        # Create or update Scene3D record
        scene_3d, created = Scene3D.objects.get_or_create(
            order=order,
            defaults={
                'scene_data': scene_data,
                'export_format': format_type
            }
        )
        
        if not created:
            scene_3d.scene_data = scene_data
            scene_3d.export_format = format_type
            scene_3d.save()
        
        # In a real implementation, you would generate the actual 3D file here
        # For now, return metadata
        return {
            'scene_id': scene_3d.id,
            'format': format_type,
            'download_url': f'/api/configurator/orders/{order.id}/download_3d/',
            'preview_url': f'/api/configurator/orders/{order.id}/scene_3d/',
            'objects_count': len(scene_data['objects']),
            'estimated_file_size': '2.5MB'  # Placeholder
        }
