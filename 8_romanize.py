import argparse
import os
import json

DATA_FN = 'merged_data.json'

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def romanize(file_path):
	
	with open(file_path, 'r', encoding='utf-8') as f:
		songs = json.loads(f.read())['songs']
		songs.sort(key=lambda x: x['serial'])

		for song in songs:
			title_ascii = song.get('title_ascii', song['title'])
			while not is_ascii(title_ascii):
				title_ascii = input(f"曲名 {title_ascii} 不为纯ASCII字符串，请重新提供：")
			song['title_ascii'] = title_ascii

			artist_ascii = song.get('artist_ascii', song['artist'])
			while not is_ascii(artist_ascii):
				artist_ascii = input(f"艺术家名 {artist_ascii} 不为纯ASCII字符串，请重新提供：")
			song['artist_ascii'] = artist_ascii
	
	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump({"songs": songs}, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 整理歌单')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()

	romanize(os.path.join(args.path, DATA_FN))
