# AI-Powered iOS AR App: Shap-E + Step1X-3D Hybrid Pipeline

## Overview
This project implements a hybrid AI pipeline to generate high-fidelity 3D assets for an iOS AR application. It combines **Shap-E** for fast geometry generation and **Step1X-3D** for high-quality textures and refinements. The final output is AR-ready 3D models that can be loaded into ARKit / RealityKit / SceneKit.

---

## Architecture

### 1. Client (iOS App)
- **Frameworks:** ARKit, RealityKit / SceneKit, SwiftUI
- **Function:**
  - User inputs a text prompt or image.
  - Sends prompt to the server API.
  - Downloads processed 3D mesh and texture.
  - Loads model into AR scene.

### 2. Server (AI Heavy)
- **Requirements:** GPU machine (≥24 GB VRAM recommended)
- **Tools:**
  - Python 3.10+
  - PyTorch with CUDA
  - Shap-E (OpenAI)
  - Step1X-3D
  - Trimesh / PyMesh for mesh cleaning

- **Workflow:**
  1. Receive prompt from iOS app.
  2. **Shap-E**: Generate rough 3D mesh from prompt.
  3. **Mesh Cleaning**: Remove degenerate faces, fill holes, merge vertices.
  4. **Step1X-3D Texture Pipeline**: Apply high-quality textures and refinements to cleaned mesh.
  5. Send final textured 3D asset back to iOS app.

---

## Step-by-Step Implementation

### Step 1: User Input
- User enters a prompt (text or image) in the iOS app.
- App sends request to server API.

### Step 2: Generate Rough Geometry (Shap-E)
```python
from shap_e.models import load_model
from shap_e.diffusion.utils import sample_latents, decode_latents

model = load_model("shap-e/model")
prompt = "Red sports car with black rims"
latents = sample_latents(prompt)
rough_mesh = decode_latents(latents)
rough_mesh.save("rough_car.obj")
```

### Step 3: Mesh Cleaning / Conversion
```python
import trimesh

mesh = trimesh.load("rough_car.obj")
mesh.remove_degenerate_faces()
mesh.fill_holes()
mesh.merge_vertices()
mesh.export("clean_car.obj")
```

### Step 4: Texture Generation (Step1X-3D)
```python
from step1x3d.texture_pipeline import generate_texture

textured_mesh = generate_texture(mesh_path="clean_car.obj",
                                 prompt="Shiny red sports car with black rims")

textured_mesh.save("final_car_textured.obj")
textured_mesh.save_texture("final_car_texture.png")
```

### Step 5: Client Rendering (iOS)
```swift
let url = URL(string: "https://server.com/final_car_textured.obj")!
let task = URLSession.shared.downloadTask(with: url) { localURL, _, _ in
    guard let localURL = localURL else { return }
    let mesh = try! Entity.loadModel(contentsOf: localURL)
    arScene.addChild(mesh)
}
task.resume()
```

---

## Pros of Hybrid Pipeline
- Faster than full Step1X-3D geometry stage.
- High-quality textures better than Shap-E alone.
- Server-side processing allows mobile-friendly AR experience.

## Cons / Considerations
- Requires mesh cleaning/conversion step.
- GPU-heavy server needed for Step1X-3D texture generation.
- Some latency (~2–3 min for high-res assets) unless caching or batch processing is used.

---

## Optional Enhancements
- Cache generated 3D models for reuse.
- LoRA fine-tuning on Step1X-3D for custom style control.
- Low-bandwidth fallback: send Shap-E mesh only if Step1X-3D takes too long.
- Batch generation for multiple prompts.

---

## References
- [Shap-E (OpenAI)](https://github.com/openai/shap-e)
- [Step1X-3D](https://arxiv.org/abs/XXXX.XXXXX)
- [Trimesh Python Library](https://trimsh.org/)
- [ARKit / RealityKit](https://developer.apple.com/augmented-reality/)

---

## Summary
This hybrid pipeline combines the speed of Shap-E with the high-fidelity textures of Step1X-3D to deliver realistic 3D assets for AR applications on iOS. The server handles AI-heavy tasks while the mobile app focuses on interactive AR visualization.

