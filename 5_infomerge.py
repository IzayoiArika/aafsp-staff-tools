import argparse
import json
import os
import sys

GROUP_SERIAL = {
	'个人': 'A',
	'Bonus': 'B',
	'合作': 'C'
}

def main():
	parser = argparse.ArgumentParser(description='整合歌曲数据')
	parser.add_argument('--path', required=True, help='工作路径')
	args = parser.parse_args()

	serials = {
		'A': 0,
		'B': 0,
		'C': 0,
	}

	serial_path = os.path.join(args.path, 'serial.txt')
	info_path = os.path.join(args.path, 'info.json')
	songlist_path = os.path.join(args.path, 'songlist')
	
	missing_reports = []
	
	info_data = {}
	try:
		with open(info_path, 'r', encoding='utf-8') as f:
			info_raw_data = json.load(f)
			for info in info_raw_data.get('songs', []):
				info_id = info.get('id')
				if info_id:
					info_data[info_id] = info
	except Exception as e:
		print(f"读取info.json时出错: {e}")
		sys.exit(1)
	
	serial_data = {}
	try:
		with open(serial_path, 'r', encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if not line:
					continue
				parts = line.split(',')
				if len(parts) < 2:
					continue
				song_id = parts[0].strip()
				serial = parts[1].strip()
				serial_data[song_id] = serial
	except Exception as e:
		print(f"读取serial.txt时出错: {e}")
		for key, value in info_data.items():
			group = GROUP_SERIAL[value['group']]
			serials[group] += 1
			serial_str = f"{group}{serials[group]:02d}"
			serial_data[key] = serial_str
			print(serial_str)
		# sys.exit(1)

	songlist_data = {}
	try:
		with open(songlist_path, 'r', encoding='utf-8') as f:
			songlist_raw_data = json.load(f)
			for song in songlist_raw_data.get('songs', []):
				song_id = song.get('id')
				if song_id:
					songlist_data[song_id] = song
	except Exception as e:
		print(f"读取songlist.json时出错: {e}")
		sys.exit(1)
	
	serial_ids = set(serial_data.keys())
	info_ids = set(info_data.keys())
	songlist_ids = set(songlist_data.keys())
	
	valid_ids = serial_ids & songlist_ids & info_ids
	
	if serial_ids - valid_ids:
		missing_reports.append(f"serial.txt中多余: {', '.join(serial_ids - valid_ids)}")
	if info_ids - valid_ids:
		missing_reports.append(f"info.json中多余: {', '.join(info_ids - valid_ids)}")
	if songlist_ids - valid_ids:
		missing_reports.append(f"songlist.json中多余: {', '.join(songlist_ids - valid_ids)}")
	
	output_data = []
	skipped_songs = []
	
	for song_id in valid_ids:

		difficulties = []
		for diff in songlist_data[song_id].get('difficulties', []):
			rating = diff.get('rating', -1)
			if rating == -1:
				continue
			
			diff_entry = {
				'ratingClass': diff['ratingClass'],
				'charter': diff.get('chartDesigner', ''),
				'rating': rating,
				'ratingPlus': diff.get('ratingPlus', False)
			}
			difficulties.append(diff_entry)
		
		if not difficulties:
			skipped_songs.append(song_id)
			continue
		
		serial_str = serial_data[song_id]
		group_str = info_data[song_id]['group']
		if GROUP_SERIAL[group_str] != serial_str[0]:
			print(f"歌曲 {song_id} 的serial: {serial_str} 分组错误，应为 {group_str}，")
		
		output_data.append({
			'id': song_id,
			'title': songlist_data[song_id]['title_localized']['en'],
			'artist': songlist_data[song_id]['artist'],
			'serial': serial_str,
			'category': info_data[song_id]['category'],
			'authors': info_data[song_id]['authors'],
			'difficulties': difficulties
		})
	
	output_data.sort(key=lambda x: (x['serial']))
	output_path = os.path.join(args.path, 'merged_data.json')
	try:
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump({'songs': output_data}, f, indent=2, ensure_ascii=False)
	except Exception as e:
		print(f"写入输出文件时出错: {e}")
		sys.exit(1)
	
	if missing_reports:
		print("缺失歌曲报告:")
		for report in missing_reports:
			print(f"  - {report}")
	
	if skipped_songs:
		print(f"跳过无有效难度的歌曲: {', '.join(skipped_songs)}")
	
	print(f"整合完成! 结果已保存至: {output_path}")

if __name__ == '__main__':
	main()