import os
import argparse
import random
from PIL import Image

def generate_resized_images(source_path, target_folder):
	"""生成512x512和256x256版本的图片到目标文件夹"""
	try:
		img = Image.open(source_path)
		for size, filename in [
			((512, 512), 'foolish_base.jpg'),
			((256, 256), 'foolish_base_256.jpg'),
		]:
			img_new = img.resize(size, Image.LANCZOS)
			img_new.save(os.path.join(target_folder, filename))
		print(f"{os.path.basename(target_folder)} 已使用图片 {source_path}")
	except Exception as e:
		print(f"处理图片 {source_path} 时出错: {str(e)}")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--path', required=True, help='主目标文件夹路径')
	parser.add_argument('--cpath', required=True, help='封面图片根目录路径')
	args = parser.parse_args()

	main_path = os.path.normpath(args.path)
	covers_root = os.path.normpath(args.cpath)
	specified_dir = os.path.join(covers_root, 'specified')
	general_dir = os.path.join(covers_root, 'general')

	random_folders = []
	processed_ids = set()

	for folder_name in os.listdir(main_path):
		folder_path = os.path.join(main_path, folder_name)
		if not os.path.isdir(folder_path):
			continue
		
		specified_cover = os.path.join(specified_dir, f"{folder_name}.jpg")
		if os.path.exists(specified_cover):
			generate_resized_images(specified_cover, folder_path)
			processed_ids.add(folder_name)
		else:
			random_folders.append(folder_name)

	general_covers = []
	if os.path.exists(general_dir):
		for fname in os.listdir(general_dir):
			if fname.lower().endswith('.jpg'):
				general_covers.append(os.path.join(general_dir, fname))

	if general_covers and random_folders:
		folder_count = len(random_folders)
		cover_count = len(general_covers)
		
		base_assign = folder_count // cover_count
		extra_assign = folder_count % cover_count
		
		assignment_plan = []
		for idx, cover in enumerate(general_covers):
			count = base_assign + 1 if idx < extra_assign else base_assign
			assignment_plan.extend([cover] * count)
		
		random.shuffle(assignment_plan)
		
		for folder_name, cover_path in zip(random_folders, assignment_plan):
			folder_path = os.path.join(main_path, folder_name)
			generate_resized_images(cover_path, folder_path)

if __name__ == "__main__":
	main()