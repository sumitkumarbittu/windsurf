# Shap-E + Step1X-3D Hybrid 3D Generation Server

This repo contains:
- **Server** (Python/FastAPI): Generates 3D models from a text prompt using a Shap-E → mesh clean → Step1X-3D texture pipeline (with graceful fallbacks if the heavy models aren't installed yet).

## Structure
```
shapex_ar_app/
  server/
    app.py
    requirements.txt
    pipeline/
      __init__.py
      shap_e_stub.py
      step1x3d_stub.py
      mesh_utils.py
```

## Quickstart (Server)
1) Python 3.10+
2) Create venv and install deps
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
```
3) Run
```
uvicorn server.app:app --reload --port 8000
```
4) Test in browser
- Open http://127.0.0.1:8000/docs
- Use POST /generate with a prompt (e.g., "A shiny red sports car").
- The response returns URLs for the generated OBJ and texture files under /static/.

Notes:
- If Shap-E or Step1X-3D are not installed, the pipeline uses light-weight fallbacks (procedural mesh + placeholder texture) so you can run end-to-end.
- To enable real Shap-E / Step1X-3D, install and configure those packages, then update `server/pipeline/shap_e_stub.py` and `server/pipeline/step1x3d_stub.py` accordingly.

## License
MIT (replace as needed)
