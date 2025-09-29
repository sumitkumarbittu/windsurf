# 📘 README – DreamCraft3D AI 3D Generation Showcase

## 🧩 Overview
This project demonstrates how to use **DreamCraft3D / DreamCraft3D++** for **AI-powered 3D generation** with:
- A **Python backend (FastAPI)** running DreamCraft3D.
- A **React (Three.js) frontend** to preview generated 3D models.
- Optional **iOS ARKit integration** to view assets in AR.

Users can enter a **text prompt** or provide a **reference image** → the system generates a **3D mesh** (.obj / .glb / .usdz).

---

## ⚙️ Requirements
- **NVIDIA GPU** with ≥20GB fVRAM (A100 recommended).
- **CUDA 11+** and **PyTorch 1.12+** installed.
- **Python 3.8+**
- **Node.js 18+** (for frontend).
- (Optional) **Xcode + iOS device** for AR demo.

---

## 🔧 Backend Setup (FastAPI + DreamCraft3D)

### 1. Clone repo & install dependencies
```bash
git clone https://github.com/your-username/dreamcraft3d-api.git
cd dreamcraft3d-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch (adjust CUDA version if needed)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install requirements
pip install -r requirements.txt
```

### 2. Download pretrained models
```bash
cd load/zero123
bash download.sh
cd ../omnidata
gdown '1Jrh-bRnJEjyMCS7f-WsaFlccfPjJPPHI&confirm=t'
gdown '1wNxVO4vVbDEMEpnAi_jwQObf2MFodcBR&confirm=t'
```

### 3. Run API
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Now the backend exposes:
- **POST** `/generate-3d` → Generate 3D mesh from prompt + optional image.

Example:
```bash
curl -X POST "http://localhost:8000/generate-3d"   -F "prompt=a futuristic red car"   -F "image=@car.png"
```

Response:
```json
{
  "status": "success",
  "mesh_file": "outputs/car/mesh.obj"
}
```

---

## 🎨 Frontend Setup (React + Three.js)

### 1. Setup React app
```bash
cd frontend
npm install
npm start
```

### 2. Example usage
- Enter a **prompt** in UI → calls backend → displays `.obj` / `.glb` with Three.js viewer.
- Rotate/zoom with mouse or touch.

---

## 📱 iOS ARKit Integration (Optional)

1. Convert generated `.obj` → `.usdz`:
```bash
xcrun usdz_converter outputs/car/mesh.obj outputs/car/model.usdz
```

2. In your SwiftUI project, load the USDZ in ARKit:
```swift
if let modelEntity = try? Entity.loadModel(named: "model.usdz") {
    let anchor = AnchorEntity(plane: .any)
    anchor.addChild(modelEntity)
    arView.scene.addAnchor(anchor)
}
```

Now you can **place AI-generated 3D models in the real world** with ARKit.

---

## 📂 Project Structure
```
dreamcraft3d-api/
│── api.py               # FastAPI backend
│── requirements.txt      # Python dependencies
│── configs/              # DreamCraft3D configs
│── load/                 # Pretrained models (Zero123, Omnidata)
│── outputs/              # Generated meshes
│── frontend/             # React frontend
│── ios-demo/             # Swift ARKit demo (optional)
```

---

## 🚀 Roadmap
- [x] Backend API with DreamCraft3D
- [x] React frontend with Three.js viewer
- [ ] Add WebSocket for live status updates
- [ ] Improve texture refinement with DreamCraft3D++
- [ ] Direct `.usdz` export for iOS

---

## 📝 Credits
- [DreamCraft3D (Sun et al., 2023)](https://arxiv.org/abs/2310.16818)  
- [DreamCraft3D++ (Sun et al., 2024)](https://arxiv.org/abs/2410.12928)  
- Built on **threestudio-project** & **stable-dreamfusion**.  
