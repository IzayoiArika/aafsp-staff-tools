import os

def verify(path):
	msgs = []
	folder_name = os.path.basename(path)
	
	for file in ["base.jpg", "base_256.jpg", "base.ogg", "songlist"]:
		if not os.path.exists(os.path.join(path, file)):
			msgs.append(f"{folder_name} 缺少文件 {file}")
	
	aff_found = False
	for diff in range(0, 5):
		aff_path = os.path.join(path, f"{diff}.aff")
		if os.path.exists(aff_path):
			aff_found = True
			break
	
	if not aff_found:
		msgs.append(f"在 {folder_name} 未找到任何有效的aff文件")
	
	return msgs

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 检测文件夹结构')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()
	
	msgs = []
	for entry in os.scandir(args.path):
		if not entry.is_dir():
			continue
		msgs += verify(entry.path)
	
	if msgs:
		for msg in msgs:
			print(f"  - {msg}")
	else:
		print(f"  - 全部文件夹通过基础结构检查")