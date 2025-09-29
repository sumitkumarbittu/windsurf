#!/usr/bin/env python3
"""
Text-to-3D mesh sampling using Shap-E (exemplary CLI).

Grounded on:
- shap_e/examples/sample_text_to_3d.ipynb
- shap_e/models/download.py (load_model, load_config)
- shap_e/diffusion/sample.py (sample_latents)
- shap_e/diffusion/gaussian_diffusion.py (diffusion_from_config)
- shap_e/util/notebooks.py (decode_latent_mesh)
- shap_e/rendering/ply_util.py (for PLY writing via tri_mesh().write_ply)

Usage:
  python scripts/text_to_mesh.py --prompt "a chair that looks like an avocado" \
    --batch-size 2 --guidance-scale 15 --outdir outputs

Outputs:
  - outputs/example_mesh_0.ply / .obj
  - outputs/example_mesh_1.ply / .obj
"""

import argparse
import os
from pathlib import Path

import torch

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh


def main():
    parser = argparse.ArgumentParser(description="Shap-E text-to-mesh generator")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt")
    parser.add_argument("--batch-size", type=int, default=1, help="Number of meshes to sample")
    parser.add_argument("--guidance-scale", type=float, default=15.0, help="Classifier-free guidance scale")
    parser.add_argument("--karras-steps", type=int, default=64, help="Karras sampling steps")
    parser.add_argument("--sigma-min", type=float, default=1e-3, help="Min sigma for Karras sampler")
    parser.add_argument("--sigma-max", type=float, default=160.0, help="Max sigma for Karras sampler")
    parser.add_argument("--s-churn", type=float, default=0.0, help="Stochasticity for Karras sampler")
    parser.add_argument("--outdir", type=str, default="outputs", help="Output directory")
    parser.add_argument("--device", type=str, default=None, help="Override device e.g. 'cuda' or 'cpu'")
    args = parser.parse_args()

    device = torch.device(
        args.device if args.device else ("cuda" if torch.cuda.is_available() else "cpu")
    )

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Load transmitter (renderer+decoder), text-conditional diffusion model, and diffusion config
    xm = load_model("transmitter", device=device)
    model = load_model("text300M", device=device)
    diffusion = diffusion_from_config(load_config("diffusion"))

    # Sample latents following the notebook defaults
    latents = sample_latents(
        batch_size=args.batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=args.guidance_scale,
        model_kwargs=dict(texts=[args.prompt] * args.batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=args.karras_steps,
        sigma_min=args.sigma_min,
        sigma_max=args.sigma_max,
        s_churn=args.s_churn,
    )

    # Decode and save meshes
    for i, latent in enumerate(latents):
        tri = decode_latent_mesh(xm, latent).tri_mesh()
        ply_path = outdir / f"example_mesh_{i}.ply"
        obj_path = outdir / f"example_mesh_{i}.obj"
        with open(ply_path, "wb") as f:
            tri.write_ply(f)
        with open(obj_path, "w") as f:
            tri.write_obj(f)
        print(f"Saved: {ply_path} and {obj_path}")

    print("Done.")


if __name__ == "__main__":
    main()
