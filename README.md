# Stable-Diffusion-Mindat
本项目旨在基于Mindat文本属性组合来生成矿物图像。通过使用Mindat数据来微调Stable Diffusion，且过程不依赖于矿物种类信息。

以下是项目结构：
```
├── Stable_Diffusion×Mindat.ipynb      // 数据集构建、模型微调、推理及评估流程
├── SD_Mindat
│   ├── app.py               // 工具主程序
│   ├── requirements.txt     // 其他依赖
│   ├── download_model.py    // 权重模型下载
│   ├── README.md         // 工具构建说明
│   └── Dockerfile         // Docker配置文件
└── README.md           // 总说明
```

Stable_Diffusion×Mindat.ipynb包含Mindat图像文本对数据集的创建流程、模型微调的具体参数值、微调后模型的推理与评估工作流程，可在 Colab 上方便运行和查看结果。
SD_Mindat是将微调模型开发成为一个供用户直接便捷可使用的交互式工具，其使用流程如下：
