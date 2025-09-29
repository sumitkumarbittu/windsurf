import os
import math
import numpy as np
import trimesh


def generate_rough_mesh(prompt: str, out_path: str) -> str:
    """
    Try to use Shap-E if available. If not, procedurally generate a placeholder mesh (UV-sphere).
    Returns the path to the rough mesh (OBJ).
    """
    # TODO: integrate real Shap-E here if installed
    # from shap_e.models import load_model
    # from shap_e.diffusion.utils import sample_latents, decode_latents

    # Placeholder: procedural UV sphere with basic UVs
    sphere = trimesh.primitives.Sphere(radius=0.5)
    mesh = sphere.to_mesh()

    # Ensure it has UVs; create simple spherical UVs
    # Trimesh may not have UVs for primitives; compute a naive projection
    vertices = mesh.vertices
    normals = mesh.vertex_normals
    u = 0.5 + (np.arctan2(normals[:, 2], normals[:, 0]) / (2 * math.pi))
    v = 0.5 - (np.arcsin(normals[:, 1]) / math.pi)
    uv = np.column_stack([u, v])

    mesh.visual.uv = uv

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    mesh.export(out_path)
    return out_path
