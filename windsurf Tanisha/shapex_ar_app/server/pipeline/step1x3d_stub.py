import os
from .mesh_utils import create_placeholder_texture


def generate_texture_for_mesh(clean_mesh_path: str, prompt: str, out_texture_path: str) -> str:
    """
    Try to use Step1X-3D if available. If not, create a placeholder texture.
    Returns the path to the texture image.
    """
    # TODO: integrate real Step1X-3D texture gen here when installed
    os.makedirs(os.path.dirname(out_texture_path), exist_ok=True)
    return create_placeholder_texture(out_texture_path, text=prompt[:16] or "ShapeX")
