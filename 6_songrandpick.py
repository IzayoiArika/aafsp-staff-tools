import random
import json
import os
import math
import colorama

class RGB_Fore:
	@staticmethod
	def hex(hex_code):
		hex_code = hex_code.lstrip('#')
		r = int(hex_code[0:2], 16)
		g = int(hex_code[2:4], 16)
		b = int(hex_code[4:6], 16)
		return f"\033[38;2;{r};{g};{b}m"
	
	@staticmethod
	def reset():
		return "\033[0m"

class ArcDiff:
	PST = RGB_Fore.hex("#33ACE9")
	PRS = RGB_Fore.hex("#8ED448")
	FTR = RGB_Fore.hex("#A13D92")
	BYD = RGB_Fore.hex("#D22D35")
	ETR = RGB_Fore.hex("#9B84C1")
	RESET = RGB_Fore.reset()
	
	@staticmethod
	def parseFrom(diff):
		ratingClass = diff['ratingClass']
		ratingStr = str(diff['rating']) + ('+' if diff.get('ratingPlus', False) else '')
		if ratingClass == 0:
			return ArcDiff.PST + '[PST] ' + ratingStr + ArcDiff.RESET
		elif ratingClass == 1:
			return ArcDiff.PRS + '[PRS] ' + ratingStr + ArcDiff.RESET
		elif ratingClass == 2:
			return ArcDiff.FTR + '[FTR] ' + ratingStr + ArcDiff.RESET
		elif ratingClass == 3:
			return ArcDiff.BYD + '[BYD] ' + ratingStr + ArcDiff.RESET
		elif ratingClass == 4:
			return ArcDiff.ETR + '[ETR] ' + ratingStr + ArcDiff.RESET
		else:
			return ratingStr

DATA_FN = 'merged_data.json'
LVSTRM_CNT = 3
FORCED_ASSIGNED = {
	# 11+以上手动分配保证平均
	'quasarpulse': 0,
	'kingatlantis': 0,
	'astralparadox': 0,

	'whatsuppop': 1,
	'diesirae': 1,
	'chousaishuukichikuimoutoflandres': 1,
	'pangramist': 1,

	'latentkingdom': 2,
	'gloriousdays': 2,
	'galvanizer': 2,

	# 避免主播打到自己的谱
	'tokugawacupnoodlekinshirei': 0,
	'riot': 0,

	'elusiveenforcer': 1,
	'rebirthofthemyth': 1,

	'thisgame': 2,

	# 避嫌
	'invain': 1,
	"rgbyoasobi": 1,

	# 撞曲尽量分到不同场
	'pupaendorfinrmx_fr': 0,

	'pupaendorfinrmx_sm': 1,
	'netsuijou_b': 1,

	'netsuijou_i': 2,

	# 主催要求我把这对OP和ED加进来
	'futarinostartbutton': 0,
	'amusingflavor': 2,
}
LVSTRM_INFO = {
	0: '2025.7.28 晚上 07:21 IA',
	1: '2025.7.29 下午 03:18 竹轮墨色',
	2: '2025.7.29 晚上 07:21 IA',
}

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
		return [], []

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 抽取场次')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()

	data_file_path = os.path.join(args.path, DATA_FN)
	songs, groups = randsongs(data_file_path)

	random.shuffle(songs)
	i = 1
	gap = 5
	print('\033c')
	diffstrs = {}

	while songs:
		song = songs.pop()
		if (i - 1) % 5 == 0:
			r = min(gap - 1, len(songs))
			input(f"等待抽取第 {i} ~ {i + r} 首 ...Enter")
			print('\033c')
			print(f"----------------------------------")
		
		diffstr = ''
		diffs = song['difficulties']
		diffs.sort(key=lambda x: x['ratingClass'], reverse=True)
		for diff in diffs:
			diffstr += ArcDiff.parseFrom(diff) + ' '
		
		diffstrs[song['id']] = diffstr
		
		print(f"")
		print(f"歌曲 {colorama.Fore.CYAN}{song['title']} - {song['artist']}{colorama.Fore.RESET} {diffstr}")
		print(f"已被分配至 第 {colorama.Fore.CYAN}{song['livestream'] + 1}{colorama.Fore.RESET} 场")
		print(colorama.Fore.GREEN + LVSTRM_INFO[song['livestream']] + colorama.Fore.RESET)
		print(f"")

		print(f"----------------------------------")
		i += 1
	
	print(f"全部 {i - 1} 首曲目均已抽取完毕")
	for gr, gr_songs in enumerate(groups):
		input(f"... Enter")
		if not gr:
			print('\033c')
		print(f"")
		print(f"第 {gr + 1} 场 共 {len(gr_songs)} 首：")
		gr_songs.sort(key=lambda x: x['serial'])
		while gr_songs:
			song = gr_songs.pop(0)
			song_type = song['serial'][0]
			if song_type == 'A':
				color = RGB_Fore.hex('#b9bbdf')
			elif song_type == 'B':
				color = RGB_Fore.hex('#ffaaa5')
			elif song_type == 'C':
				color = RGB_Fore.hex('#a8e6cf')
			print(f"  - {color}{song['serial']} {song['title']}{colorama.Fore.RESET} {diffstrs[song['id']]}")
	
	input(f"今天的节目全部结束 谢谢大家")