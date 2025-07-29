import os
from PIL import Image

def main():
    COVERS_DIR = 'D:\\UserFiles\\Downloads\\covers'
    
    if not os.path.exists(COVERS_DIR):
        print(f"文件夹 '{COVERS_DIR}' 不存在")
        return
    
    supported_extensions = ('.jpg', '.jpeg', '.png')
    
    for filename in os.listdir(COVERS_DIR):
        if filename.lower().endswith(supported_extensions):
            name_without_ext = os.path.splitext(filename)[0].lower()
            original_path = os.path.join(COVERS_DIR, filename)
            
            output_dir = os.path.join(COVERS_DIR, name_without_ext)
            os.makedirs(output_dir, exist_ok=True)
            
            try:
                print(f"正在处理：{original_path}")
                with Image.open(original_path) as img:
                    sizes = {
                        (768, 768): '1080_base.jpg',
                        (384, 384): '1080_base_256.jpg',
                        (512, 512): 'base.jpg',
                        (256, 256): 'base_256.jpg'
                    }
                    
                    for size, output_name in sizes.items():
                        resized_img = img.resize(size, Image.LANCZOS)
                        
                        if img.mode in ('RGBA', 'P'):
                            resized_img = resized_img.convert('RGB')
                        
                        output_path = os.path.join(output_dir, output_name)
                        resized_img.save(output_path, quality=95)
            
            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")

if __name__ == '__main__':
    main()