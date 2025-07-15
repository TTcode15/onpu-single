#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import random
from PIL import Image, ImageDraw, ImageEnhance

# 出力ディレクトリ
output_dir = "note_dataset/images"
label_dir = "note_dataset/labels"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(label_dir, exist_ok=True)

# クラスマップ
class_map = {"C4": 0, "C5": 1}

# データ数
train_count = 100
val_count = 50
image_size = 128

# 音符位置（Y軸）
staff_top = 50
line_spacing = 6
staff_lines_y = [staff_top + i * line_spacing for i in range(5)]
note_positions = {
    "C4": staff_lines_y[4] + line_spacing,  # 第1加線（下）
    "C5": (staff_lines_y[1] + staff_lines_y[2]) // 2  # 第3間（上から2と3の間）
}

# データ生成
def generate_note_image(note_name, index, split="train"):
    img = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(img)

    # 音符サイズ・位置
    y_center = note_positions[note_name]
    x_center = random.randint(50, 78)
    note_w = random.randint(10, 13)
    note_h = random.randint(6, 8)
    outline_width = random.randint(1, 2)

    # 五線譜（音符幅の約1.5倍）
    staff_x1 = x_center - int(note_w * 0.75)
    staff_x2 = x_center + int(note_w * 0.75)
    line_thickness = random.randint(1, 2)
    for y in staff_lines_y:
        draw.line((staff_x1, y, staff_x2, y), fill="black", width=line_thickness)

    # 音符（白抜きの楕円）
    note_box = (
        x_center - note_w // 2,
        y_center - note_h // 2,
        x_center + note_w // 2,
        y_center + note_h // 2
    )
    draw.ellipse(note_box, fill="white", outline="black", width=outline_width)

    # 横棒（線の上にある音符）
    for y in staff_lines_y:
        if abs(y_center - y) <= 1:
            draw.line((x_center - note_w // 2, y_center, x_center + note_w // 2, y_center), fill="black", width=1)

    # 加線（五線譜外）
    if y_center < staff_lines_y[0]:
        for y in range(staff_lines_y[0] - line_spacing, y_center - 1, -line_spacing):
            draw.line((x_center - note_w, y, x_center + note_w, y), fill="black", width=1)
    elif y_center > staff_lines_y[-1]:
        for y in range(staff_lines_y[-1] + line_spacing, y_center + 1, line_spacing):
            draw.line((x_center - note_w, y, x_center + note_w, y), fill="black", width=1)

    # 画像変換（回転・平行移動・色調整）
    angle = random.uniform(-5, 5)
    dx = random.randint(-3, 3)
    dy = random.randint(-3, 3)
    img = img.rotate(angle, resample=Image.Resampling.BICUBIC, center=(image_size // 2, image_size // 2), fillcolor="white")
    img = img.transform((image_size, image_size), Image.Transform.AFFINE, (1, 0, dx, 0, 1, dy), fillcolor="white")

    img = ImageEnhance.Brightness(img).enhance(random.uniform(0.9, 1.1))
    img = ImageEnhance.Contrast(img).enhance(random.uniform(0.9, 1.1))

    # 保存
    fname = f"{note_name}_{index}.png"
    save_img_path = os.path.join(output_dir, split, fname)
    save_lbl_path = os.path.join(label_dir, split, fname.replace(".png", ".txt"))
    os.makedirs(os.path.dirname(save_img_path), exist_ok=True)
    os.makedirs(os.path.dirname(save_lbl_path), exist_ok=True)
    img.save(save_img_path)

    # バウンディングボックス（音符＋五線譜）
    min_x = min(staff_x1, note_box[0])
    max_x = max(staff_x2, note_box[2])
    min_y = min(min(staff_lines_y), note_box[1])
    max_y = max(max(staff_lines_y), note_box[3])

    xc = (min_x + max_x) / 2 / image_size
    yc = (min_y + max_y) / 2 / image_size
    w = (max_x - min_x) / image_size
    h = (max_y - min_y) / image_size
    class_id = class_map[note_name]

    with open(save_lbl_path, "w") as f:
        f.write(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")

# 実行：C4/C5 各100枚（train）、50枚（val）
for note in ["C4", "C5"]:
    for i in range(train_count):
        generate_note_image(note, i, "train")
    for i in range(val_count):
        generate_note_image(note, i, "val")


# In[ ]:




