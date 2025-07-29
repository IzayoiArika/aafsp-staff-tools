import os
import argparse
from PIL import Image

TARGET_FILES = {
    "base.jpg": (512, 512),
    "base_256.jpg": (256, 256),
    "1080_base.jpg": (768, 768),
    "1080_base_256.jpg": (384, 384)
}

def resize_image(image_path, target_size):
    """缩放图片到目标尺寸"""
    try:
        with Image.open(image_path) as img:
            if img.size == target_size:
                return False
            
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            resized_img = img.resize(target_size, Image.LANCZOS)
            resized_img.save(image_path, "JPEG", quality=95)
            return True
    except Exception as e:
        print(f"处理图片 {image_path} 时出错: {str(e)}")
        return False

def process_directory(path):
    """处理指定目录下的所有子目录"""
    if not os.path.isdir(path):
        print(f"错误: {path} 不是有效目录")
        return
    
    for entry in os.listdir(path):
        subdir = os.path.join(path, entry)
        if os.path.isdir(subdir):
            for filename, target_size in TARGET_FILES.items():
                filepath = os.path.join(subdir, filename)
                if os.path.isfile(filepath):
                    if resize_image(filepath, target_size):
                        print(f"Resized: {filepath} -> {target_size[0]}x{target_size[1]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量缩放图片到标准尺寸")
    parser.add_argument('--path', required=True, help='工作路径')
    args = parser.parse_args()
    
    process_directory(args.path)