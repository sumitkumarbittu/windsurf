import os
import trimesh
from PIL import Image, ImageDraw


def clean_mesh(in_path: str, out_path: str) -> str:
    mesh = trimesh.load(in_path)
    mesh.remove_degenerate_faces()
    mesh.remove_duplicate_faces()
    mesh.remove_unreferenced_vertices()
    mesh.fill_holes()
    mesh.merge_vertices()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    mesh.export(out_path)
    return out_path


def export_mesh_with_texture(mesh_path: str, texture_image_path: str, export_dir: str, name: str):
    """
    Exports OBJ + MTL + PNG into export_dir using the provided mesh and texture.
    Returns tuple of file paths: (obj, mtl, png)
    """
    os.makedirs(export_dir, exist_ok=True)

    # Load mesh and attach texture reference via material name
    mesh = trimesh.load(mesh_path)

    # Prepare paths
    obj_path = os.path.join(export_dir, f"{name}.obj")
    mtl_path = os.path.join(export_dir, f"{name}.mtl")
    tex_rel = f"{name}.png"
    tex_path = os.path.join(export_dir, tex_rel)

    # Copy/Save texture to export directory if needed
    if os.path.abspath(texture_image_path) != os.path.abspath(tex_path):
        Image.open(texture_image_path).save(tex_path)

    # Write minimal MTL
    material_name = f"{name}_mat"
    with open(mtl_path, "w") as f:
        f.write(f"newmtl {material_name}\n")
        f.write("Ka 1.000 1.000 1.000\n")
        f.write("Kd 1.000 1.000 1.000\n")
        f.write("Ks 0.000 0.000 0.000\n")
        f.write(f"map_Kd {tex_rel}\n")

    # Export OBJ that references the MTL and material
    # Trimesh exporter doesn't automatically write the MTL ref for us in some cases,
    # so we write OBJ manually using Trimesh's export to wavefront data.
    obj_data = mesh.export(file_type='obj')
    header = f"mtllib {os.path.basename(mtl_path)}\nusemtl {material_name}\n"

    with open(obj_path, "w") as f:
        f.write(header + obj_data)

    return obj_path, mtl_path, tex_path


def create_placeholder_texture(out_path: str, text: str = "ShapX") -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", (1024, 1024), color=(200, 40, 40))
    draw = ImageDraw.Draw(img)
    draw.text((40, 40), text, fill=(255, 255, 255))
    img.save(out_path)
    return out_path
