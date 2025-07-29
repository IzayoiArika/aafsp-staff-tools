import argparse
import os
import json
import random

DATA_FN = 'merged_data.json'

SKIP_IDS = [
	"bassline",
	"lightofmuse",
	"aleajactaest",
	"isogashiihi",
	"rnrmonsta",
	"concvssion",
	"kingatlantis",
	"sphalerite",
	"venusinvader",
	"amusingflavor",
	"netsuijou_i",
	"wodebeishangshishuizuode",
	"foolishofme",
	"paraparasakura",
	"zhongkouwei",
	"moonglow",
	"secretspell",
	"quasarpulse",
	"thisgame",
	"rokuchounen",
	"diesirae",
	"invain",
	"netsuijou_b",
	"tetoris",
	"pupaendorfinrmx_fr",
]

def split_array(arr, n: int):
    arr_len = len(arr)
    base_size = arr_len // n
    extra = arr_len % n
    result = []
    start = 0
    
    for i in range(n):
        size = base_size + (1 if i < extra else 0)
        end = start + size
        if size > 0:
            result.append(arr[start:end])
        else:
            result.append([])
        start = end
    
    return result

def shuffle_gr(file_path, dict_path):
	
	with open(file_path, 'r', encoding='utf-8') as fsongs:
		songs = json.loads(fsongs.read())['songs']
		songs = [s for s in songs if s['id'] not in SKIP_IDS]
		songs.sort(key=lambda x: x['serial'])
		random.shuffle(songs)

		for i, gr_songs in enumerate(split_array(songs, 6)):
			with open(os.path.join(dict_path, f"title_{i}.txt"), 'w', encoding='utf-8') as ftitle:
				for song in gr_songs:
					ftitle.write(f"{song['title_ascii']}\n")
			with open(os.path.join(dict_path, f"artist_{i}.txt"), 'w', encoding='utf-8') as ftitle:
				for song in gr_songs:
					ftitle.write(f"{song['artist_ascii']}\n")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 开字母分组')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()

	dict_path = os.path.join(args.path, '__dicts')
	if not os.path.exists(dict_path):
		os.mkdir(dict_path)
	shuffle_gr(os.path.join(args.path, DATA_FN), dict_path)
