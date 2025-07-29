import os
import argparse
import json
import shutil

CHAR_MAPPING = {
    '\\': '＼',
    '/': '／',
    ':': '：',
    '*': '＊',
    '?': '？',
    '"': '＂',
    '<': '＜',
    '>': '＞',
    '|': '｜',
}

def clean_fn(name):
    cleaned = []
    for char in name:
        cleaned.append(CHAR_MAPPING.get(char, char))
    return ''.join(cleaned)

def main():
	parser = argparse.ArgumentParser(description='AAF: SP收集音频和图片文件')
	parser.add_argument('--input', required=True, help='输入路径')
	parser.add_argument('--output', required=True, help='输出路径')
	args = parser.parse_args()

	os.makedirs(args.output, exist_ok=True)
	
	json_path = os.path.join(args.input, 'merged_data.json')
	try:
		with open(json_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
	except Exception as e:
		print(f"读取 {json_path} 时发生错误: {str(e)}")
		return

	song_map = {}
	for song in data['songs']:
		song_map[song['id']] = {
			'title': song['title'],
			'serial': song['serial']
		}

	for item in os.listdir(args.input):
		item_path = os.path.join(args.input, item)
		
		if not os.path.isdir(item_path):
			continue
		
		song_id = item
		if song_id not in song_map:
			print(f"未在JSON中找到 {item} 有关的信息")
			continue
		
		song_info = song_map[song_id]
		title = clean_fn(song_info['title'])
		serial = clean_fn(song_info['serial'])
		base_name = f"{serial} {title}"

		ogg_src = os.path.join(item_path, 'base.ogg')
		ogg_dest = os.path.join(args.output, f"{base_name}.ogg")

		if os.path.exists(ogg_src):
			shutil.copy2(ogg_src, ogg_dest)
		else:
			print(f"{item}/base.ogg 不存在")
			continue

		jpg_src = os.path.join(item_path, 'base.jpg')
		jpg_dest = os.path.join(args.output, f"{base_name}.jpg")
		
		if os.path.exists(jpg_src):
			shutil.copy2(jpg_src, jpg_dest)
		else:
			print(f"{item}/base.jpg 不存在")

if __name__ == "__main__":
	main()