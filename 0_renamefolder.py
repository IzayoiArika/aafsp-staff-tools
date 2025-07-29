import os
import re
import json

def rename(path):
	errs = []
	msgs = []

	new_name = os.path.basename(path)
	pieces = [s.strip() for s in re.split(r'[【】 \+]', new_name) if s.strip() != '']

	group = pieces[0]
	category = pieces[1]
	id = pieces[2]
	authors = pieces[3:]
	
	id = id.split(' ', 1)[0] if ' ' in id else id
	
	working_path = os.path.dirname(path)
	new_path = os.path.join(working_path, id)
	if os.path.exists(new_path):
		errs.append(f"名称 \"{id}\" 已被占用")
		return errs, msgs, id, category, group, authors
	
	try:
		os.rename(path, new_path)

		for subentry in os.scandir(new_path):
			if subentry.is_file() and subentry.name != 'songlist' and subentry.name in ['songlist.txt', 'songlist.json']:
				try:
					os.rename(subentry.path, os.path.join(new_path, "songlist"))
					msgs.append(f"在 {id} 检测到 {subentry.name}，已自动去除文件后缀名")
				except Exception as e:
					errs.append(f"在 {id} 重命名文件 {subentry.name} 失败: {str(e)}")
	except Exception as e:
		errs.append(f"重命名 {os.path.basename(path)} 为 {id} 时失败: {str(e)}")

	return errs, msgs, id, category, group, authors

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 文件夹重命名')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()
	
	with open(os.path.join(args.path, 'info.json'), 'w', encoding='utf-8') as f:
		errs = []
		msgs = []
		songs = []
		for entry in os.scandir(args.path):
			if not entry.is_dir():
				continue
			f_errs, f_msgs, id, category, group, authors = rename(entry.path)
			errs += f_errs
			msgs += f_msgs

			if not f_errs:
				songs.append({
					'id': id,
					'category': category,
					'group': group,
					'authors': authors
				})
		json.dump({"songs": songs}, f, indent=4, ensure_ascii=False)

	if errs:
		for err in errs:
			print(f"  - {err}")
	else:
		print(f"  - 全部文件夹重命名成功")
	
	for msg in msgs:
		print(f"  - {msg}")