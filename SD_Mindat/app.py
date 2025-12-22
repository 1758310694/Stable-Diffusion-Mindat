import gradio as gr
import numpy as np
import random
from diffusers import DiffusionPipeline
import torch
import re
from PIL import Image, ImageDraw, ImageFont

device = "cuda" if torch.cuda.is_available() else "cpu"
model_repo_id = "Quanli1/sd-1.5-FT"  # 替换为可用模型

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
pipe = DiffusionPipeline.from_pretrained(model_repo_id, torch_dtype=torch_dtype)
pipe = pipe.to(device)

MAX_SEED = np.iinfo(np.int32).max
MAX_IMAGE_SIZE = 1024

json_list = [
  {
    "elements": "Na, Pb, O, C, and H",
    "diapheny": "Transparent",
    "hmin": "",
    "hmax": "",
    "lustretype": "Vitreous",
    "streak": "White",
    "csystem": "Hexagonal",
    "cleavagetype": "",
    "fracturetype": "",
    "opticaltype": ""
  },
  {
    "elements": "Ca, Si, Ti, and O",
    "diapheny": "Transparent, Translucent",
    "hmin": "5.0",
    "hmax": "5.5",
    "lustretype": "Adamantine,Resinous",
    "streak": "White",
    "csystem": "Monoclinic",
    "cleavagetype": "Distinct/Good",
    "fracturetype": "",
    "opticaltype": "Biaxial"
  },
  {
    "elements": "Al, Fe, Mg, Si, B, and O",
    "diapheny": "Transparent,Translucent",
    "hmin": "7.5",
    "hmax": "7.5",
    "lustretype": "Vitreous,Pearly",
    "streak": "",
    "csystem": "Orthorhombic",
    "cleavagetype": "Perfect",
    "fracturetype": "",
    "opticaltype": "Biaxial"
  },
  {
    "elements": "Al, B, O, F, and H",
    "diapheny": "Transparent",
    "hmin": "7.0",
    "hmax": "7.0",
    "lustretype": "Vitreous",
    "streak": "white",
    "csystem": "Hexagonal",
    "cleavagetype": "None Observed",
    "fracturetype": "Conchoidal",
    "opticaltype": "Uniaxial"
  },
  {
    "elements": "Hg, and S",
    "diapheny": "Transparent,Translucent",
    "hmin": "2.0",
    "hmax": "2.5",
    "lustretype": "Metallic",
    "streak": "Red-brown to scarlet",
    "csystem": "Trigonal",
    "cleavagetype": "Perfect",
    "fracturetype": "Irregular/Uneven,Sub-Conchoidal",
    "opticaltype": "Uniaxial"
  }
]


def format_prompt_dynamic(
    elements="", diapheny="", hmin="", hmax="", lustretype="",
    streak="", csystem="", cleavagetype="", fracturetype="", opticaltype=""
):
    """预处理 trim"""
    elements = elements.strip()
    diapheny = diapheny.strip()
    hmin = hmin.strip() if hmin else ""
    hmax = hmax.strip() if hmax else ""
    lustretype = lustretype.strip()
    streak = streak.strip()
    csystem = csystem.strip()
    cleavagetype = cleavagetype.strip()
    fracturetype = fracturetype.strip()
    opticaltype = opticaltype.strip()    
    """生成规范化字符串，空字段跳过"""
    parts = []
    head_format = "A mineral "
    if diapheny:
        head_format = (f"A {diapheny} mineral ")
    if elements:
        parts.append(f"composed of {elements}")
    if hmin or hmax:
        h_str = f"{hmin or '?'}–{hmax or '?'}"
        parts.append(f"with Mohs hardness {h_str}")
    if lustretype:
        parts.append(f"{lustretype} lustre")
    if streak:
        parts.append(f"{streak} streak")
    if csystem:
        parts.append(f"{csystem} crystal system")
    if cleavagetype:
        parts.append(f"{cleavagetype} cleavage")
    if fracturetype:
        parts.append(f"{fracturetype} fracture")
    if opticaltype:
        parts.append(f"{opticaltype} optical type")
        
    body_format = ", ".join(parts)
    all_format = head_format + (body_format + "." if body_format else "")

    # 如果 all_format 和 head_format 相同，则返回空字符串
    return all_format if all_format != head_format else ""


def add_watermark(img, text="Generate image"):
    """在右下角添加水印（兼容新 Pillow，没有 textsize）"""
    watermark_img = img.copy()
    draw = ImageDraw.Draw(watermark_img)

    # 字体大小自动缩放
    font_size = max(16, img.width // 32)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 使用 textbbox 获取文本范围
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 右下位置
    x = img.width - text_w - 10
    y = img.height - text_h - 10

    # 半透明背景
    draw.rectangle(
        [(x - 5, y - 5), (x + text_w + 5, y + text_h + 5)],
        fill=(0, 0, 0, 120)
    )

    # 白色文字
    draw.text((x, y), text, fill="white", font=font)

    return watermark_img



def infer_from_prompt(
    prompt_text, seed, randomize_seed, width, height, guidance_scale, num_inference_steps
):
    if randomize_seed:
        seed = random.randint(0, MAX_SEED)
    generator = torch.Generator().manual_seed(seed)

    image = pipe(
        prompt=prompt_text,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        width=width,
        height=height,
        generator=generator,
    ).images[0]

    # 添加水印
    watermarked = add_watermark(image, "Generate image")

    return watermarked, seed
    
with gr.Blocks() as demo:
    gr.Markdown("# Mineral Text-to-Image Generator")

    with gr.Row():
        # 左侧列：输入表单 + 高级参数分组
        with gr.Column():
            gr.Markdown("### Mineral Properties")
            elements = gr.Text(label="Elements", info="elements in the geomaterial, Available values:H, Li, Be, B, C, N, O, F, Na, Mg, Al, Si, P, S, Cl, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Br, Rb, Sr, Y, Zr, Nb, Mo, Ru, Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Cs, Ba, La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf, Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Ra, Th, U, [], OH, H2O, H3O, BO3, NH4, NH2, NO3, CO3, PO4, SO4, SO3, AsO4, AsO3, VO4, CrO4, SeO4, SeO3, MoO4, SnOH, SbO4, SbO3, TeO4, TeO3, IO3, WO4, UO2, SiO4, SiO3, Si3O9, CH3COO, HCOO, C2O4, e.g., 'Hg, and S'")
            diapheny = gr.Text(label="Diapheny", info="the diaphany of the mineral, Available values : Opaque, Translucent, Transparent, e.g., 'Transparent', 'Translucent'")
            hmin = gr.Text(label="Min Mohs hardness", info="minimum Moh's hardness of the mineral, the range is 1-10, e.g., '2.0'")
            hmax = gr.Text(label="Max Mohs hardness", info="maximum Moh's hardness of the mineral, the range is 1-10, e.g., '2.5'")
            lustretype = gr.Text(label="Lustre", info="the lustre type of the mineral, Available values : Adamantine, Dull, Earthy, Greasy, Metallic, Pearly, Resinous, Silky, Sub-Adamantine, Sub-Metallic, Sub-Vitreous, Vitreous, Waxy, e.g., 'Metallic'")
            streak = gr.Text(label="Streak", info="the color of the streak, e.g., 'Red-brown to scarlet'")
            csystem = gr.Text(label="Crystal system", info="the crystal system of the mineral, Available values : Amorphous, Hexagonal, Icosahedral, Isometric, Monoclinic, Orthorhombic, Tetragonal, Triclinic, Trigonal, e.g., 'Trigonal'")
            cleavagetype = gr.Text(label="Cleavage", info="the cleavage type of the mineral, Available values : Distinct/Good, Imperfect/Fair, None Observed, Perfect, Poor/Indistinct, Very Good, e.g., 'Perfect'")
            fracturetype = gr.Text(label="Fracture", info="the fracture type of the mineral, Available values : Conchoidal, Fibrous, Hackly, Irregular/Uneven, Micaceous, None observed, Splintery, Step-Like, Sub-Conchoidal, e.g., 'Irregular/Uneven, Sub-Conchoidal'")
            opticaltype = gr.Text(label="Optical type", info="the optical type of the mineral, Available values : Biaxial, Isotropic, Uniaxial, e.g., 'Uniaxial'")

            gr.Markdown("### Advanced Parameters")
            seed = gr.Slider(label="Seed", minimum=0, maximum=MAX_SEED, step=1, value=0)
            randomize_seed = gr.Checkbox(label="Randomize seed", value=True)
            width = gr.Slider(label="Width", minimum=256, maximum=MAX_IMAGE_SIZE, step=32, value=512)
            height = gr.Slider(label="Height", minimum=256, maximum=MAX_IMAGE_SIZE, step=32, value=512)
            guidance_scale = gr.Slider(label="Guidance scale", minimum=0, maximum=10, step=0.1, value=7.5)
            num_inference_steps = gr.Slider(label="Inference steps", minimum=1, maximum=50, step=1, value=25)

        # 右侧列：动态 prompt + 按钮 + 图像
        with gr.Column():
            dynamic_prompt = gr.Textbox(label="Generated Prompt", lines=3)
            run_button = gr.Button("Generate Image")
            result_image = gr.Image(label="Result")
            gr.Markdown("### Examples")
            example_buttons = []
            for example in json_list:
                # 按钮显示文本可以直接用 format_prompt_dynamic 生成，也可以只用元素摘要
                btn_text = format_prompt_dynamic(**example) or "Example"
            
                btn = gr.Button(btn_text, elem_classes="example-btn")
                example_buttons.append(btn)
            
                # 点击按钮直接填充表单和动态 prompt
                btn.click(
                    fn=lambda e=example: (
                        e["elements"], e["diapheny"], e["hmin"], e["hmax"], e["lustretype"], 
                        e["streak"], e["csystem"], e["cleavagetype"], e["fracturetype"], 
                        e["opticaltype"], format_prompt_dynamic(**e)
                    ),
                    inputs=None,
                    outputs=[
                        elements, diapheny, hmin, hmax, lustretype, streak, csystem,
                        cleavagetype, fracturetype, opticaltype, dynamic_prompt
                    ]
                )
                
    # 绑定动态更新 prompt
    for input_field in [
        elements, diapheny, hmin, hmax, lustretype,
        streak, csystem, cleavagetype, fracturetype, opticaltype
    ]:
        input_field.change(
            fn=format_prompt_dynamic,
            inputs=[elements, diapheny, hmin, hmax, lustretype,
                    streak, csystem, cleavagetype, fracturetype, opticaltype],
            outputs=dynamic_prompt
        )


    # 点击按钮生成图像，直接使用 dynamic_prompt 的文本
    run_button.click(
        fn=infer_from_prompt,
        inputs=[dynamic_prompt, seed, randomize_seed, width, height, guidance_scale, num_inference_steps],
        outputs=[result_image, seed]
    )

if __name__ == "__main__":
    demo.launch()
