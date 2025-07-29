import argparse
import os
import json

DATA_FN = 'merged_data.json'
OUTPUT_FN = 'result.txt'
DIFF_NAMES = {
	0: 'Past',
	1: 'Present',
	2: 'Future',
	3: 'Beyond',
	4: 'Eternal'
}

def diff_str(diff):
	return DIFF_NAMES.get(diff['ratingClass'], '') + ' ' \
		+ ('?' if diff['rating'] == 0 else str(diff['rating'])) \
		+ ('+' if diff['ratingPlus'] else '')

def writesheet(working_path):
	
	sheet_path = os.path.join(working_path, OUTPUT_FN)
	data_path = os.path.join(working_path, DATA_FN)

	with open(data_path, 'r', encoding='utf-8') as fdata:
		songs = json.loads(fdata.read())['songs']
		songs.sort(key=lambda x: x['serial'])

		with open(sheet_path, 'w', encoding='utf-8') as fres:
			for song in songs:
				diffs = song['difficulties']
				first = True
				for diff in diffs:
					s = '\t'.join([
						song['serial'] if first else '',
						song['category'] if first else '',
						str(song['livestream']) if first else '',
						song['id'] if first else '',
						song['title'] if first else '',
						song['artist'] if first else '',
						diff['charter'].replace('\n', '\\n').replace('\r',''),
						diff_str(diff),
						'',
						', '.join(song['authors']) if first else ''
					]) + '\n'
					fres.write(s)
					first = False

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 整理歌单')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()

	writesheet(args.path)