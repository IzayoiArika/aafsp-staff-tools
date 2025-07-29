import os
import json

def normalize(working_path):

	msgs = []

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
			
			with open(slst_path, 'w', encoding='utf-8') as f:
				json.dump(data, f, indent=4, ensure_ascii=False)
		except Exception as e:
			msgs.append(f"处理 {os.path.basename(entry) } 失败: {str(e)}")
	
	return msgs

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 文件夹重命名')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()
	
	msgs = normalize(args.path)
	if msgs:
		for msg in msgs:
			print(f"  - {msg}")