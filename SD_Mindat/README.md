# SD_Mindat Text-to-Image
一个基于 Mindat 矿物数据的 Stable Diffusion 文生图项目  

## 开始（Getting Started）

### 环境配置（Prerequisites）

请确保你的运行环境满足以下要求：

- **Docker**（推荐使用 Docker Desktop）
- **NVIDIA GPU**
- **CUDA 12.6**
- **NVIDIA Container Toolkit**（用于 Docker 调用 GPU）
- **Python 3.10 + pip**（用于下载模型）
- **cloudflared**（用于将本地服务暴露到公网）
 
### 检查环境（Verify Environment）

在命令行中执行以下命令，确认环境配置正确：

```cmd
# 查看 Docker 版本，确认 Docker 已正确安装
docker --version

# 查看 CUDA 版本（nvcc 编译器），确认 GPU 驱动和 CUDA 可用
nvcc -V

# 查看 Python 版本，确认已安装 Python 3.10+
python --version

# 查看 pip 版本，确认 pip 可用
pip --version
```

### 代码获取（Installation）

#### 方法一：直接下载源码

在 GitHub 项目页面点击 **Code → Download ZIP**，下载并解压源码。

#### 方法二：使用 Git 克隆（推荐）
```cmd
git clone [*.git]
```

### 详细配置（Setup）
```cmd
# 进入项目目录
cd ./test-mineral-df

# 拉取官方 Python 3.10 精简版基础镜像
docker pull python:3.10-slim

# 基于当前目录下的 Dockerfile 构建镜像（df-mineral-cu126）
docker build -t df-mineral-cu126 .

# 安装 Hugging Face Hub（用于模型下载与管理）
pip install huggingface_hub

# 执行自定义 python 脚本，从 Hugging Face 下载 Stable Diffusion 所需模型 Quanli1/sd-1.5-FT
# 默认下载路径为 C:/Users/Lenovo/hf_cache，可在脚本中修改
python download_model.py

```

### 运行docker容器（Run Container）
```cmd
# 运行 Docker 容器，使用 GPU 并映射端口 7860
# -v 将本地模型缓存目录映射到容器内，保证模型可用
# 如果修改了默认下载路径，请相应修改挂载路径
# 容器启动后执行 app.py 启动应用
docker run -it --gpus all -p 7860:7860 -v C:/Users/Lenovo/hf_cache:/root/.cache/huggingface/hub df-mineral-cu126  python app.py

# 将本地应用暴露到公网（可选）
# 执行后终端会输出一个随机生成的公网地址，例如：https://xxxx.trycloudflare.com
cloudflared tunnel --url http://localhost:7860
```

### 操作使用说明（Usage）

在完成 Docker 容器启动和模型下载后，你可以通过以下方式使用 SD_Mindat 文生图应用：

#### 1. 本地访问

打开浏览器，访问本地服务地址：http://localhost:7860

即可进入可视化界面，输入文本提示生成矿物图像。

#### 2. 公网访问（可选）

如果启用了 Cloudflare 隧道，将本地服务暴露到公网，可以通过终端输出的随机地址访问，例如：https://xxxx.trycloudflare.com

> ⚠️ 注意：
> - **禁止将本服务用于违法、违规或有害内容生成** 
> - 公网地址为临时生成，关闭隧道后会失效  
> - 若需要长期访问，可创建持久隧道并绑定自定义子域名  
> - 确保 Docker 容器正在运行且端口 7860 已暴露