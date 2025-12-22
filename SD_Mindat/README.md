---
title: Test Mineral Df
emoji: 🖼
colorFrom: purple
colorTo: red
sdk: gradio
sdk_version: 5.44.0
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

>cmd
cd C:/Users/Lenovo/Desktop/test-mineral-df
nvcc -V
docker pull python:3.10-slim
docker build -t df-mineral-cu126 .
python download_model.py
docker run -it --gpus all -p 7860:7860 -v C:/Users/Lenovo/Desktop/test-mineral-df:/app -v C:/Users/Lenovo/hf_cache:/root/.cache/huggingface/hub df-mineral-cu126 python /app/app.py
cloudflared tunnel --url http://localhost:7860