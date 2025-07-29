import os
import argparse
import shutil

def main():
    parser = argparse.ArgumentParser(description='Collect output.mp4 files from Rendering subfolders.')
    parser.add_argument('--path', required=True, help='Root directory path to search')
    args = parser.parse_args()
    
    root_path = args.path
    collected_dir = os.path.join(root_path, '__videos')
    
    # 创建目标目录（如果不存在）
    os.makedirs(collected_dir, exist_ok=True)
    
    # 遍历根目录的直接子文件夹
    for item in os.listdir(root_path):
        subdir_path = os.path.join(root_path, item)
        
        # 只处理子文件夹
        if os.path.isdir(subdir_path):
            # 检查Rendering子文件夹
            rendering_path = os.path.join(subdir_path, 'Rendering')
            output_file = os.path.join(rendering_path, 'output.mp4')
            
            if os.path.exists(output_file):
                # 生成目标文件名（避免冲突）
                new_name = f"{item}.mp4"
                dest_path = os.path.join(collected_dir, new_name)
                
                # 处理文件名冲突
                counter = 1
                while os.path.exists(dest_path):
                    new_name = f"{item}_{counter}.mp4"
                    dest_path = os.path.join(collected_dir, new_name)
                    counter += 1
                
                # 移动文件
                shutil.move(output_file, dest_path)

if __name__ == "__main__":
    main()