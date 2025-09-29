from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uuid

from .pipeline import (
    generate_rough_mesh,
    clean_mesh,
    generate_texture_for_mesh,
    export_mesh_with_texture,
)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")
PIPE_OUT_DIR = os.path.join(DATA_DIR, "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(PIPE_OUT_DIR, exist_ok=True)

app = FastAPI(title="ShapeX 3D Generator")

# Allow local dev from iOS simulator / web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class GenerateRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate(req: GenerateRequest):
    job_id = str(uuid.uuid4())
    work_dir = os.path.join(PIPE_OUT_DIR, job_id)
    os.makedirs(work_dir, exist_ok=True)

    rough_obj = os.path.join(work_dir, "rough.obj")
    clean_obj = os.path.join(work_dir, "clean.obj")
    tex_png = os.path.join(work_dir, "texture.png")

    # 1) Rough mesh (Shap-E stub)
    generate_rough_mesh(req.prompt, rough_obj)

    # 2) Clean mesh
    clean_mesh(rough_obj, clean_obj)

    # 3) Texture (Step1X-3D stub)
    generate_texture_for_mesh(clean_obj, req.prompt, tex_png)

    # 4) Export to static dir with a public name
    export_name = f"asset_{job_id}"
    obj_path, mtl_path, tex_path = export_mesh_with_texture(
        mesh_path=clean_obj,
        texture_image_path=tex_png,
        export_dir=STATIC_DIR,
        name=export_name,
    )

    base_url = "/static"
    return {
        "id": job_id,
        "obj_url": f"{base_url}/{os.path.basename(obj_path)}",
        "mtl_url": f"{base_url}/{os.path.basename(mtl_path)}",
        "texture_url": f"{base_url}/{os.path.basename(tex_path)}",
    }
