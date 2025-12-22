FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --upgrade pip \
 && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

RUN pip install -r requirements.txt gradio

EXPOSE 7860