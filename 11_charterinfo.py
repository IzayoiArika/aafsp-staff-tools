import random
import json
import os
import math

DATA_FN = 'merged_data.json'

def randsongs(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			json_raw = f.read()
			json_data = json.loads(json_raw)
			songs = json_data['songs']

			for song in songs:
				if 'livestream' in song:
					del song['livestream']

			song_cnt = len(songs)
			max_per_group = math.ceil(song_cnt / LVSTRM_CNT)

			groups = [ [] for _ in range(LVSTRM_CNT)]

			for id, f_gr in FORCED_ASSIGNED.items():
				for song in songs:
					if song['id'] == id:
						song['livestream'] = f_gr
						groups[f_gr].append(song)
						break
			
			random.shuffle(songs)
			for song in songs:
				if 'livestream' in song:
					continue

				available = [p for p in range(LVSTRM_CNT) if len(groups[p]) < max_per_group]
				n_gr = random.choice(available)

				song['livestream'] = n_gr
				groups[n_gr].append(song)

		with open(file_path, 'w', encoding='utf-8') as f:
			json.dump({"songs": songs}, f, indent=4, ensure_ascii=False)
		return songs, groups
	except:
		print(f"打开文件 {DATA_FN} 失败")
		return []

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 谱师统计')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()

	charters = {} # 谱师和他们写的谱数
	charter_combs = [] # 谱师组合

	data_file_path = os.path.join(args.path, DATA_FN)
	with open(data_file_path, 'r', encoding='utf-8') as f:
		songs = json.load(f)['songs']

		for song in songs:
			authors = song['authors']
			authors.sort()
			chart_cnt = len(song['difficulties'])
			for author in authors:
				if author not in charters:
					charters[author] = {
						'A': 0,
						'B': 0,
						'C': 0,
					}
				charters[author][song['serial'][0]] += chart_cnt
			
			author_str = ', '.join(authors)
			author_obj = {
					'str': author_str,
					'hcnt': len(authors)
				}
			if author_obj not in charter_combs:
				charter_combs.append(author_obj)
	charter_combs.sort(key=lambda x: (x['hcnt'], x['str']))
	
	charter_list = []
	for charter, cinfo in charters.items():
		charter_list.append({
			'str': charter,
			'A': cinfo['A'],
			'B': cinfo['B'],
			'C': cinfo['C'],
		})
	charter_list.sort(key=lambda x: (x['A'], x['B'], x['C'], x['str']))

	with open(os.path.join(args.path, 'charters_info.txt'), 'w', encoding='utf-8') as f:
		f.write(f"谱师列表\n")
		f.write(f"------------------------------\n")
		for charter in charter_list:
			f.write(f"{charter['str']}\t")
			f.write(f"{charter['A'] + charter['B'] + charter['C']}\t")
			f.write(f"{charter['A'] if charter['A'] != 0 else ''}\t")
			f.write(f"{charter['C'] if charter['C'] != 0 else ''}\t")
			f.write(f"{charter['B'] if charter['B'] != 0 else ''}\n")
		f.write(f"\n")
		f.write(f"所有谱师及组合\n")
		f.write(f"------------------------------\n")
		for comb in charter_combs:
			f.write(f"{comb['str']}\n")
