import os
import uuid
import math
import numpy as np
import trimesh
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from PIL import Image, ImageDraw

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Directory setup
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")
PIPE_OUT_DIR = os.path.join(DATA_DIR, "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(PIPE_OUT_DIR, exist_ok=True)


# Shap-E stub functions
def generate_rough_mesh(prompt: str, out_path: str) -> str:
    """
    Generate 3D mesh from text prompt using improved shape generation.
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Improved shape generation based on prompt keywords with variations
    prompt_lower = prompt.lower()
    
    # Vehicle variations
    if any(word in prompt_lower for word in ['sports car', 'race car', 'racing car']):
        mesh = create_sports_car_mesh()
    elif any(word in prompt_lower for word in ['truck', 'pickup']):
        mesh = create_truck_mesh()
    elif any(word in prompt_lower for word in ['bus', 'van']):
        mesh = create_bus_mesh()
    elif any(word in prompt_lower for word in ['car', 'vehicle', 'sedan']):
        mesh = create_regular_car_mesh()
    
    # Building variations
    elif any(word in prompt_lower for word in ['tall building', 'skyscraper', 'tower']):
        mesh = create_tall_building_mesh()
    elif any(word in prompt_lower for word in ['small house', 'cottage']):
        mesh = create_small_house_mesh()
    elif any(word in prompt_lower for word in ['house', 'building', 'home']):
        mesh = create_house_like_mesh()
    
    # Nature variations
    elif any(word in prompt_lower for word in ['tall tree', 'big tree', 'oak tree']):
        mesh = create_tall_tree_mesh()
    elif any(word in prompt_lower for word in ['small tree', 'bush', 'shrub']):
        mesh = create_small_tree_mesh()
    elif any(word in prompt_lower for word in ['tree', 'plant']):
        mesh = create_tree_like_mesh()
    
    # Container variations
    elif any(word in prompt_lower for word in ['coffee cup', 'mug']):
        mesh = create_mug_mesh()
    elif any(word in prompt_lower for word in ['wine glass', 'glass']):
        mesh = create_wine_glass_mesh()
    elif any(word in prompt_lower for word in ['cup', 'container']):
        mesh = create_cup_like_mesh()
    
    # Furniture variations
    elif any(word in prompt_lower for word in ['office chair', 'desk chair']):
        mesh = create_office_chair_mesh()
    elif any(word in prompt_lower for word in ['wooden chair', 'dining chair']):
        mesh = create_wooden_chair_mesh()
    elif any(word in prompt_lower for word in ['chair', 'seat']):
        mesh = create_chair_like_mesh()
    
    # Shape variations
    elif any(word in prompt_lower for word in ['long box', 'rectangular box']):
        mesh = create_long_box_mesh()
    elif any(word in prompt_lower for word in ['small box', 'cube']):
        mesh = create_small_box_mesh()
    elif any(word in prompt_lower for word in ['box', 'container']):
        mesh = create_box_like_mesh()
    
    else:
        # Generate different default shapes based on prompt hash for variety
        import hashlib
        prompt_hash = int(hashlib.md5(prompt.encode()).hexdigest()[:8], 16)
        shape_type = prompt_hash % 4
        
        if shape_type == 0:
            mesh = trimesh.primitives.Sphere(radius=0.5).to_mesh()
        elif shape_type == 1:
            mesh = trimesh.primitives.Box(extents=[1.0, 1.0, 1.0])
        elif shape_type == 2:
            mesh = trimesh.primitives.Cylinder(radius=0.4, height=1.0)
        else:
            mesh = trimesh.primitives.Capsule(radius=0.3, height=1.0).to_mesh()
    
    # Add UV coordinates
    vertices = mesh.vertices
    if len(vertices) > 0:
        # Compute spherical UV mapping
        normals = mesh.vertex_normals
        u = 0.5 + (np.arctan2(normals[:, 2], normals[:, 0]) / (2 * math.pi))
        v = 0.5 - (np.arcsin(normals[:, 1]) / math.pi)
        mesh.visual.uv = np.column_stack([u, v])
    
    mesh.export(out_path)
    return out_path

def create_sports_car_mesh():
    """Create a low, sleek sports car"""
    # Lower, wider body
    body = trimesh.primitives.Box(extents=[2.2, 0.9, 0.7])
    
    # Very low, sleek roof
    roof = trimesh.primitives.Box(extents=[1.0, 0.8, 0.4])
    roof.apply_translation([0, 0, 0.55])
    
    # Lower wheels
    wheel_positions = [[-0.8, -0.6, -0.25], [0.8, -0.6, -0.25], [-0.8, 0.6, -0.25], [0.8, 0.6, -0.25]]
    wheels = []
    for pos in wheel_positions:
        wheel = trimesh.primitives.Cylinder(radius=0.25, height=0.15)
        wheel.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        wheel.apply_translation(pos)
        wheels.append(wheel)
    
    return trimesh.util.concatenate([body, roof] + wheels)

def create_regular_car_mesh():
    """Create a regular sedan car"""
    # Standard car body
    body = trimesh.primitives.Box(extents=[2.0, 0.8, 1.0])
    
    # Standard roof
    roof = trimesh.primitives.Box(extents=[1.2, 0.7, 0.6])
    roof.apply_translation([0, 0, 0.8])
    
    # Standard wheels
    wheel_positions = [[-0.7, -0.5, -0.3], [0.7, -0.5, -0.3], [-0.7, 0.5, -0.3], [0.7, 0.5, -0.3]]
    wheels = []
    for pos in wheel_positions:
        wheel = trimesh.primitives.Cylinder(radius=0.3, height=0.2)
        wheel.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        wheel.apply_translation(pos)
        wheels.append(wheel)
    
    return trimesh.util.concatenate([body, roof] + wheels)

def create_truck_mesh():
    """Create a pickup truck"""
    # Truck cab
    cab = trimesh.primitives.Box(extents=[1.2, 0.8, 1.2])
    cab.apply_translation([-0.4, 0, 0])
    
    # Truck bed
    bed = trimesh.primitives.Box(extents=[1.6, 0.8, 0.6])
    bed.apply_translation([0.8, 0, -0.3])
    
    # Larger wheels
    wheel_positions = [[-0.8, -0.5, -0.4], [0.4, -0.5, -0.4], [1.2, -0.5, -0.4], 
                      [-0.8, 0.5, -0.4], [0.4, 0.5, -0.4], [1.2, 0.5, -0.4]]
    wheels = []
    for pos in wheel_positions:
        wheel = trimesh.primitives.Cylinder(radius=0.35, height=0.25)
        wheel.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        wheel.apply_translation(pos)
        wheels.append(wheel)
    
    return trimesh.util.concatenate([cab, bed] + wheels)

def create_bus_mesh():
    """Create a bus"""
    # Long, tall body
    body = trimesh.primitives.Box(extents=[3.0, 0.9, 1.8])
    
    # Many wheels
    wheel_positions = [[-1.2, -0.6, -0.6], [-0.4, -0.6, -0.6], [0.4, -0.6, -0.6], [1.2, -0.6, -0.6],
                      [-1.2, 0.6, -0.6], [-0.4, 0.6, -0.6], [0.4, 0.6, -0.6], [1.2, 0.6, -0.6]]
    wheels = []
    for pos in wheel_positions:
        wheel = trimesh.primitives.Cylinder(radius=0.4, height=0.2)
        wheel.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        wheel.apply_translation(pos)
        wheels.append(wheel)
    
    return trimesh.util.concatenate([body] + wheels)

# Keep the original for backward compatibility
def create_car_like_mesh():
    return create_regular_car_mesh()

def create_house_like_mesh():
    """Create a basic house-shaped mesh"""
    # House base
    base = trimesh.primitives.Box(extents=[2.0, 2.0, 1.5])
    
    # Roof (pyramid)
    roof_vertices = np.array([
        [-1.2, -1.2, 0.75], [1.2, -1.2, 0.75], [1.2, 1.2, 0.75], [-1.2, 1.2, 0.75],  # base
        [0, 0, 2.0]  # apex
    ])
    roof_faces = np.array([
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # triangular faces
        [0, 3, 2], [0, 2, 1]  # base (split into triangles)
    ])
    roof = trimesh.Trimesh(vertices=roof_vertices, faces=roof_faces)
    
    return trimesh.util.concatenate([base, roof])

def create_tree_like_mesh():
    """Create a basic tree-shaped mesh"""
    # Trunk (cylinder)
    trunk = trimesh.primitives.Cylinder(radius=0.2, height=1.5)
    
    # Leaves (sphere on top)
    leaves = trimesh.primitives.Sphere(radius=0.8)
    leaves.apply_translation([0, 0, 1.2])
    
    return trimesh.util.concatenate([trunk, leaves])

def create_cup_like_mesh():
    """Create a basic cup-shaped mesh"""
    # Outer cylinder
    outer = trimesh.primitives.Cylinder(radius=0.5, height=1.0)
    # Inner cylinder (to make it hollow)
    inner = trimesh.primitives.Cylinder(radius=0.4, height=0.9)
    inner.apply_translation([0, 0, 0.05])
    
    # Subtract inner from outer to create hollow cup
    try:
        cup = outer.difference(inner)
        return cup
    except:
        return outer  # Fallback if boolean operation fails

def create_box_like_mesh():
    """Create a basic box-shaped mesh"""
    return trimesh.primitives.Box(extents=[1.0, 1.0, 1.0])

def create_chair_like_mesh():
    """Create a basic chair-shaped mesh"""
    # Seat
    seat = trimesh.primitives.Box(extents=[1.0, 1.0, 0.1])
    seat.apply_translation([0, 0, 0.5])
    
    # Backrest
    back = trimesh.primitives.Box(extents=[1.0, 0.1, 1.0])
    back.apply_translation([0, 0.45, 1.0])
    
    # Legs (4 cylinders)
    leg_positions = [[-0.4, -0.4, 0.25], [0.4, -0.4, 0.25], [-0.4, 0.4, 0.25], [0.4, 0.4, 0.25]]
    legs = []
    for pos in leg_positions:
        leg = trimesh.primitives.Cylinder(radius=0.05, height=0.5)
        leg.apply_translation(pos)
        legs.append(leg)
    
    return trimesh.util.concatenate([seat, back] + legs)

# Additional mesh variations
def create_tall_building_mesh():
    """Create a tall building/skyscraper"""
    base = trimesh.primitives.Box(extents=[1.5, 1.5, 4.0])
    return base

def create_small_house_mesh():
    """Create a small cottage"""
    base = trimesh.primitives.Box(extents=[1.5, 1.5, 1.0])
    roof_vertices = np.array([
        [-0.9, -0.9, 0.5], [0.9, -0.9, 0.5], [0.9, 0.9, 0.5], [-0.9, 0.9, 0.5],
        [0, 0, 1.2]
    ])
    roof_faces = np.array([
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
        [0, 3, 2], [0, 2, 1]
    ])
    roof = trimesh.Trimesh(vertices=roof_vertices, faces=roof_faces)
    return trimesh.util.concatenate([base, roof])

def create_tall_tree_mesh():
    """Create a tall tree"""
    trunk = trimesh.primitives.Cylinder(radius=0.15, height=2.5)
    leaves = trimesh.primitives.Sphere(radius=1.0)
    leaves.apply_translation([0, 0, 2.0])
    return trimesh.util.concatenate([trunk, leaves])

def create_small_tree_mesh():
    """Create a small tree/bush"""
    trunk = trimesh.primitives.Cylinder(radius=0.1, height=0.8)
    leaves = trimesh.primitives.Sphere(radius=0.5)
    leaves.apply_translation([0, 0, 0.8])
    return trimesh.util.concatenate([trunk, leaves])

def create_mug_mesh():
    """Create a coffee mug with handle"""
    outer = trimesh.primitives.Cylinder(radius=0.4, height=0.8)
    inner = trimesh.primitives.Cylinder(radius=0.35, height=0.75)
    inner.apply_translation([0, 0, 0.025])
    
    # Simple handle (torus section)
    handle = trimesh.primitives.Cylinder(radius=0.05, height=0.3)
    handle.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    handle.apply_translation([0.45, 0, 0.2])
    
    try:
        mug = outer.difference(inner)
        return trimesh.util.concatenate([mug, handle])
    except:
        return trimesh.util.concatenate([outer, handle])

def create_wine_glass_mesh():
    """Create a wine glass"""
    # Bowl
    bowl = trimesh.primitives.Sphere(radius=0.4)
    bowl.apply_translation([0, 0, 0.8])
    
    # Stem
    stem = trimesh.primitives.Cylinder(radius=0.05, height=0.6)
    stem.apply_translation([0, 0, 0.3])
    
    # Base
    base = trimesh.primitives.Cylinder(radius=0.3, height=0.05)
    
    return trimesh.util.concatenate([bowl, stem, base])

def create_office_chair_mesh():
    """Create an office chair with wheels"""
    # Seat
    seat = trimesh.primitives.Cylinder(radius=0.4, height=0.1)
    seat.apply_translation([0, 0, 0.5])
    
    # Backrest
    back = trimesh.primitives.Box(extents=[0.8, 0.1, 0.8])
    back.apply_translation([0, 0.35, 0.9])
    
    # Central post
    post = trimesh.primitives.Cylinder(radius=0.05, height=0.5)
    post.apply_translation([0, 0, 0.25])
    
    # Base with wheels
    base_positions = [[0.3, 0, 0], [-0.3, 0, 0], [0, 0.3, 0], [0, -0.3, 0], [0.2, 0.2, 0]]
    wheels = []
    for pos in base_positions:
        wheel = trimesh.primitives.Sphere(radius=0.08)
        wheel.apply_translation(pos)
        wheels.append(wheel)
    
    return trimesh.util.concatenate([seat, back, post] + wheels)

def create_wooden_chair_mesh():
    """Create a traditional wooden chair"""
    # Seat
    seat = trimesh.primitives.Box(extents=[0.9, 0.9, 0.08])
    seat.apply_translation([0, 0, 0.45])
    
    # Backrest with slats
    back1 = trimesh.primitives.Box(extents=[0.08, 0.08, 0.8])
    back1.apply_translation([-0.3, 0.4, 0.85])
    back2 = trimesh.primitives.Box(extents=[0.08, 0.08, 0.8])
    back2.apply_translation([0, 0.4, 0.85])
    back3 = trimesh.primitives.Box(extents=[0.08, 0.08, 0.8])
    back3.apply_translation([0.3, 0.4, 0.85])
    
    # Legs
    leg_positions = [[-0.35, -0.35, 0.225], [0.35, -0.35, 0.225], [-0.35, 0.35, 0.225], [0.35, 0.35, 0.225]]
    legs = []
    for pos in leg_positions:
        leg = trimesh.primitives.Box(extents=[0.08, 0.08, 0.45])
        leg.apply_translation(pos)
        legs.append(leg)
    
    return trimesh.util.concatenate([seat, back1, back2, back3] + legs)

def create_long_box_mesh():
    """Create a long rectangular box"""
    return trimesh.primitives.Box(extents=[2.5, 0.8, 0.6])

def create_small_box_mesh():
    """Create a small cube"""
    return trimesh.primitives.Box(extents=[0.6, 0.6, 0.6])


# Mesh utility functions
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


def create_placeholder_texture(out_path: str, text: str = "ShapX") -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", (1024, 1024), color=(200, 40, 40))
    draw = ImageDraw.Draw(img)
    draw.text((40, 40), text, fill=(255, 255, 255))
    img.save(out_path)
    return out_path

def create_smart_texture(out_path: str, prompt: str) -> str:
    """Create context-aware texture based on prompt keywords"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    prompt_lower = prompt.lower()
    
    # Determine base color and pattern based on prompt
    if any(word in prompt_lower for word in ['red', 'crimson', 'scarlet']):
        base_color = (220, 20, 20)
    elif any(word in prompt_lower for word in ['blue', 'azure', 'navy']):
        base_color = (20, 20, 220)
    elif any(word in prompt_lower for word in ['green', 'emerald', 'forest']):
        base_color = (20, 180, 20)
    elif any(word in prompt_lower for word in ['yellow', 'gold', 'golden']):
        base_color = (255, 215, 0)
    elif any(word in prompt_lower for word in ['purple', 'violet', 'magenta']):
        base_color = (128, 0, 128)
    elif any(word in prompt_lower for word in ['orange', 'amber']):
        base_color = (255, 165, 0)
    elif any(word in prompt_lower for word in ['white', 'snow', 'ivory']):
        base_color = (240, 240, 240)
    elif any(word in prompt_lower for word in ['black', 'dark', 'shadow']):
        base_color = (40, 40, 40)
    elif any(word in prompt_lower for word in ['brown', 'wood', 'wooden', 'oak']):
        base_color = (139, 69, 19)
    elif any(word in prompt_lower for word in ['metal', 'metallic', 'steel', 'iron']):
        base_color = (169, 169, 169)
    elif any(word in prompt_lower for word in ['shiny', 'glossy', 'chrome']):
        base_color = (192, 192, 192)
    else:
        base_color = (128, 128, 128)  # Default gray
    
    # Create texture with patterns
    img = Image.new("RGB", (512, 512), color=base_color)
    draw = ImageDraw.Draw(img)
    
    # Add material-specific patterns
    if any(word in prompt_lower for word in ['brick', 'wall']):
        create_brick_pattern(draw, base_color)
    elif any(word in prompt_lower for word in ['wood', 'wooden', 'tree']):
        create_wood_pattern(draw, base_color)
    elif any(word in prompt_lower for word in ['metal', 'metallic']):
        create_metal_pattern(draw, base_color)
    elif any(word in prompt_lower for word in ['fabric', 'cloth', 'textile']):
        create_fabric_pattern(draw, base_color)
    elif any(word in prompt_lower for word in ['stone', 'rock', 'marble']):
        create_stone_pattern(draw, base_color)
    elif any(word in prompt_lower for word in ['car', 'vehicle']):
        create_car_paint_pattern(draw, base_color)
    
    # Add text label
    try:
        draw.text((20, 20), prompt[:20], fill=(255, 255, 255) if sum(base_color) < 400 else (0, 0, 0))
    except:
        pass
    
    img.save(out_path)
    return out_path

def create_brick_pattern(draw, base_color):
    """Add brick-like pattern"""
    brick_color = tuple(max(0, c - 30) for c in base_color)
    for y in range(0, 512, 40):
        offset = 20 if (y // 40) % 2 else 0
        for x in range(offset, 512, 80):
            draw.rectangle([x, y, x + 60, y + 30], outline=brick_color, width=2)

def create_wood_pattern(draw, base_color):
    """Add wood grain pattern"""
    grain_color = tuple(max(0, c - 40) for c in base_color)
    for y in range(0, 512, 8):
        draw.line([(0, y), (512, y + 20)], fill=grain_color, width=1)

def create_metal_pattern(draw, base_color):
    """Add metallic pattern"""
    highlight = tuple(min(255, c + 50) for c in base_color)
    shadow = tuple(max(0, c - 50) for c in base_color)
    for y in range(0, 512, 4):
        color = highlight if y % 8 < 4 else shadow
        draw.line([(0, y), (512, y)], fill=color, width=1)

def create_fabric_pattern(draw, base_color):
    """Add fabric weave pattern"""
    weave_color = tuple(max(0, c - 20) for c in base_color)
    for x in range(0, 512, 8):
        for y in range(0, 512, 8):
            if (x + y) % 16 < 8:
                draw.rectangle([x, y, x + 4, y + 4], fill=weave_color)

def create_stone_pattern(draw, base_color):
    """Add stone texture pattern"""
    import random
    random.seed(42)  # Consistent pattern
    for _ in range(100):
        x, y = random.randint(0, 512), random.randint(0, 512)
        size = random.randint(2, 8)
        shade = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in base_color)
        draw.ellipse([x, y, x + size, y + size], fill=shade)

def create_car_paint_pattern(draw, base_color):
    """Add car paint shine pattern"""
    highlight = tuple(min(255, c + 80) for c in base_color)
    for y in range(0, 512, 20):
        draw.line([(0, y), (512, y + 10)], fill=highlight, width=2)


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


# Step1X-3D stub functions
def generate_texture_for_mesh(clean_mesh_path: str, prompt: str, out_texture_path: str) -> str:
    """
    Generate context-aware texture based on prompt.
    """
    os.makedirs(os.path.dirname(out_texture_path), exist_ok=True)
    return create_smart_texture(out_texture_path, prompt)


# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return jsonify({
        "message": "ShapeX 3D Generator API",
        "endpoints": {
            "GET /": "Web interface",
            "POST /generate": "Generate 3D model from text prompt",
            "GET /static/<filename>": "Download generated assets"
        }
    })


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400
    
    prompt = data['prompt']
    job_id = str(uuid.uuid4())
    work_dir = os.path.join(PIPE_OUT_DIR, job_id)
    os.makedirs(work_dir, exist_ok=True)

    rough_obj = os.path.join(work_dir, "rough.obj")
    clean_obj = os.path.join(work_dir, "clean.obj")
    tex_png = os.path.join(work_dir, "texture.png")

    try:
        # 1) Rough mesh (Shap-E stub)
        generate_rough_mesh(prompt, rough_obj)

        # 2) Clean mesh
        clean_mesh(rough_obj, clean_obj)

        # 3) Texture (Step1X-3D stub)
        generate_texture_for_mesh(clean_obj, prompt, tex_png)

        # 4) Export to static dir with a public name
        export_name = f"asset_{job_id}"
        obj_path, mtl_path, tex_path = export_mesh_with_texture(
            mesh_path=clean_obj,
            texture_image_path=tex_png,
            export_dir=STATIC_DIR,
            name=export_name,
        )

        base_url = "/static"
        return jsonify({
            "id": job_id,
            "obj_url": f"{base_url}/{os.path.basename(obj_path)}",
            "mtl_url": f"{base_url}/{os.path.basename(mtl_path)}",
            "texture_url": f"{base_url}/{os.path.basename(tex_path)}",
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/static/<filename>')
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route('/debug')
def debug():
    """Debug endpoint to check generated files"""
    import glob
    static_files = glob.glob(os.path.join(STATIC_DIR, "*"))
    file_info = []
    for file_path in static_files[-6:]:  # Last 6 files
        filename = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        file_info.append({"filename": filename, "size": size})
    
    return jsonify({
        "static_dir": STATIC_DIR,
        "recent_files": file_info,
        "total_files": len(static_files)
    })


if __name__ == '__main__':
    print("Starting ShapeX 3D Generator...")
    print("Available endpoints:")
    print("  GET  /           - Web interface")
    print("  GET  /api        - API info")
    print("  POST /generate   - Generate 3D model")
    print("  GET  /static/*   - Download assets")
    print(f"Open http://127.0.0.1:5001 in your browser!")
    app.run(host='0.0.0.0', port=5001, debug=True)
