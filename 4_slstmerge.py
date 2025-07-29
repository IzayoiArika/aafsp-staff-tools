import os
import json

def merge(working_path):

	msgs = []
	songs = []

	for entry in os.scandir(working_path):
		if not entry.is_dir():
			continue

		slst_path = os.path.join(entry, "songlist")
		try:
			with open(slst_path, 'r', encoding='utf-8') as f:
				json_str = f.read().strip().rstrip(',')
				data = json.loads(json_str)

				data['purchase'] = ''
				data['set'] = 'base'

				for term in ['_comment', 'just_kidding']:
					if term in data:
						del data[term]
				
				songs.append(data)
		except Exception as e:
			msgs.append(f"处理 {os.path.basename(entry) } 失败: {str(e)}")
	
	if not songs:
		return False, msgs
	
	try:
		slst_path = os.path.join(working_path, 'songlist')
		with open(slst_path, 'w', encoding='utf-8') as f:
			json.dump({"songs": songs}, f, indent=4, ensure_ascii=False)
		return True, msgs
	except Exception as e:
		msgs.append(f"合并文件失败: {str(e)}")
		return False, msgs


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 文件夹重命名')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()
	
	_, msgs = merge(args.path)
	if msgs:
		for msg in msgs:
			print(f"  - {msg}")
	else:
		print("  - 全部songlist合并成功")