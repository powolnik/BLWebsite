import trimesh
import json

class Scene3DService:
    @staticmethod
    def load_component_model(component):
        """Load 3D model file and return mesh data"""
        if component.model_3d:
            mesh = trimesh.load(component.model_3d.path)
            return {
                'vertices': mesh.vertices.tolist(),
                'faces': mesh.faces.tolist(),
                'bounds': mesh.bounds.tolist()
            }
        return None

    @staticmethod
    def compose_scene(order):
        """Build complete 3D scene from order components"""
        scene_data = {
            'components': [],
            'environment': {
                'lighting': 'default',
                'ground': True
            }
        }

        for item in order.items.all():
            model_data = Scene3DService.load_component_model(item.component)
            if model_data:
                scene_data['components'].append({
                    'id': item.component.id,
                    'name': item.component.name,
                    'model': model_data,
                    'quantity': item.quantity,
                    'color': item.component.color
                })

        return scene_data