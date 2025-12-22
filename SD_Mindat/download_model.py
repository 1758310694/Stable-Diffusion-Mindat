from huggingface_hub import snapshot_download
import os

# 设置缓存目录
os.environ["HF_HOME"] = r"C:/Users/Lenovo/hf_cache"

snapshot_download(
    repo_id="Quanli1/sd-1.5-FT",
    cache_dir=r"C:/Users/Lenovo/hf_cache",
    resume_download=True  # 自动断点续传
)
