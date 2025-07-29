import os
import json

class aafacc:
	current_name = 'aafsp'
	allowed_sides = [0, 1, 2, 3]
	date = 1723456890
	version = "1.1 aafsp Act II"

class bgs:
	side_names = [
		"光", "对立", "消色", "殸"
	]

	def get_side_name(side):
		return bgs.side_names[side] if side in [0, 1, 2, 3] else ""

	lephon_bgs = [
		"designant",
		"lamentrain",
		"lephon"
	]

	achromatic_bgs = [
		"epilogue",
		"testify"
	]

	light_bgs = [
		"aegleseeker",
		"aegleseeker_grey",
		"aethercrest",
		"alice_light",
		"arcahv",
		"auxesia",
		"base_light",
		"byd_light",
		"byd2_light",
		"chunithmnew_light",
		"chuni-worldvanquisher",
		"cytus_light",
		"djmax_light",
		"dynamix_light",
		"eden_light",
		"eden_append_light",
		"eden_boss",
		"etherstrike",
		"felis",
		"finale_light",
		"fractureray",
		"gc_light",
		"gc_lance",
		"gou",
		"hime_light",
		"lanota-light",
		"maimai_light",
		"magnolia",
		"meta_mysteria",
		"mirai_light",
		"modelista",
		"musedash_light",
		"nijuusei-light-b",
		"nijuusei2_light",
		"nirvluce",
		"observer_light",
		"omatsuri_light",
		"omegafour",
		"ongeki_light",
		"pragmatism",
		"pragmatism3",
		"prelude_light",
		"quon",
		"rei",
		"ringedgenesis",
		"rotaeno_light",
		"saikyostronger",
		"shiawase",
		"shiawase2",
		"single_light",
		"single2_light",
		"solitarydream",
		"tanoc_light",
		"tanoc_red",
		"temptation",
		"tonesphere-solarsphere",
		"touhou_light",
		"undertale_light",
		"virtus",
		"vs_light",
		"vulcanus",
		"wacca_light",
		"zettai_light"
	]

	conflict_bgs = [
		"alexandrite",
		"alice_conflict",
		"alterego",
		"apophenia",
		"arcanaeden",
		"arghena",
		"aterlbus",
		"axiumcrisis",
		"base_conflict",
		"byd_conflict",
		"byd2_conflict",
		"chunithmthird_conflict",
		"chunithmnew_conflict",
		"chuni-garakuta",
		"chuni-ikazuchi",
		"cyaegha",
		"cytus_conflict",
		"cytus_boss",
		"djmax_conflict",
		"djmax_nightmare",
		"djmax_wagd",
		"dynamix_conflict",
		"eden_conflict",
		"eden_append_conflict",
		"finale_conflict",
		"gc_conflict",
		"gc_ouroboros",
		"gc_buchigire",
		"grievouslady",
		"hime_conflict",
		"lamia",
		"lanota-conflict",
		"lethaeus",
		"maimai_conflict",
		"maimai_boss",
		"megalovaniarmx",
		"mirai_awakened",
		"mirai_conflict",
		"musedash_conflict",
		"nihil",
		"nijuusei-conflict-b",
		"nijuusei2_conflict",
		"observer_conflict",
		"omatsuri_conflict",
		"ongeki_conflict",
		"pentiment",
		"prelude_conflict",
		"rotaeno_conflict",
		"sheriruth",
		"single_conflict",
		"single2_conflict",
		"spidersthread",
		"tanoc_conflict",
		"tempestissimo",
		"tempestissimo_red",
		"tiferet",
		"tonesphere-darksphere",
		"touhou_conflict",
		"undertale_conflict",
		"viciousheroism3",
		"vs_conflict",
		"wacca_conflict",
		"wacca_boss",
		"yugamu",
		"zettai"
	]

	general_light_bgs = light_bgs + achromatic_bgs + lephon_bgs
	all_bgs = light_bgs + conflict_bgs + achromatic_bgs + lephon_bgs

def verify(folder_path):
	msgs = []

	try:
		with open(os.path.join(folder_path, 'songlist'), 'r', encoding='utf-8') as f:
			content = f.read().rstrip()
	except Exception as e:
		return False, [f"读取文件时发生错误: {e}"]

	# songlist生成器生成的songlist有以下特征：
	# 1. 结尾自带逗号
	# 2. 缩进为5空格
	if not content.endswith(','):
		msgs.append(f"songlist 文件末尾缺少逗号")

	lines = content.split('\n')
	for line in lines:
		i = 0
		while i < len(line) and line[i] == ' ':
			i += 1
		if i % 5 != 0:
			msgs.append(f"songlist 未使用5空格缩进")
			break
	
	# 解析JSON，然后核验各项是否合规
	json_raw = content.rstrip(',') + '\n'
	try:
		json_data = json.loads(json_raw)
	except json.JSONDecodeError as e:
		msgs.append(f"songlist 不为合法JSON，{e}")
		return False, msgs
	
	def pass_verify(x):
		return True, []

	fields = [
		("id", lambda x: verify_id(x, folder_path)),
		("title_localized", verify_title_localized),
		("artist", verify_artist),
		("bpm", verify_bpm),
		("bpm_base", verify_bpm_base),
		("set", verify_set),
		("purchase", verify_purchase),
		("side", pass_verify),
		("date", verify_date),
		("version", verify_version),
		("audioPreview", pass_verify),
		("audioPreviewEnd", pass_verify),
		("_comment", verify__comment),
		("just_kidding", verify_just_kidding),
		("difficulties", lambda x: verify_difficulties(x, folder_path)),
		("bg", pass_verify)
	]

	field_exists = {
		field: field in json_data for field, _ in fields
	}

	for field, validator in fields:
		if not field_exists[field]:
			msgs.append(f"songlist 缺少字段 \"{field}\"")
		else:
			succeeded, field_msgs = validator(json_data[field])
			if not succeeded:
				msgs += field_msgs
	
	if field_exists['audioPreview'] and field_exists['audioPreviewEnd']:
		succeeded, f_msgs = verify_audioPreviews(json_data['audioPreview'], json_data['audioPreviewEnd'])
		if not succeeded:
			msgs += f_msgs
	
	if field_exists['side'] and field_exists['bg']:
		succeeded, f_msgs = verify_bg_and_side(json_data['bg'], json_data['side'], folder_path)
		if not succeeded:
			msgs += f_msgs
	
	return msgs

def verify_id(id, folder_path):
	if type(id) is not str:
		return False, [f"id 必须为 str"]
	if not str.isidentifier(id) or str.lower(id) != id:
		return False, [f"id: {id} 不合法，必须为合法的无大写标识符"]
	
	folder_name = os.path.basename(folder_path)
	if id != folder_name:
		return False, [f"songlist 提供的 id: {id} 与文件夹名: {folder_name} 不匹配"]
	return True, []

def verify_title_localized(title_obj):
	if type(title_obj) is not dict:
		return False, ["title_localized 必须为 dict"]
	if list(title_obj.keys()) != ["en"]:
		return False, ["title_localized 必须包含唯一键值对，且键必须为\"en\""]
	if type(title_obj["en"]) is not str:
		return False, ["title_localized.en 必须为 str"]
	return True, []

def verify_artist(artist):
	valid = type(artist) is str
	return valid, [] if valid else [f"artist 必须为 str"]

def verify_bpm(bpm):
	valid = type(bpm) is str
	return valid, [] if valid else [f"bpm 必须为 str"]

def verify_bpm_base(bpm_base):
	valid = type(bpm_base) in (int, float) and bpm_base > 0
	return valid, [] if valid else [f"bpm_base 必须为正 int/float"]

def verify_set(set_str):
	valid = set_str == aafacc.current_name
	return valid, [] if valid else [f"set 必须为 \"{aafacc.current_name}\""]

def verify_purchase(purchase):
	valid = purchase == aafacc.current_name
	return valid, [] if valid else [f"purchase 必须为 \"{aafacc.current_name}\""]

def verify_date(date):
	valid = date == aafacc.date
	return valid, [] if valid else [f"date 必须为 {aafacc.date}"]

def verify_version(version):
	valid = version == aafacc.version
	return valid, [] if valid else [f"version 必须为 \"{aafacc.version}\""]

def verify_audioPreviews(apr, apre):
	if type(apr) is not int or apr < 0:
		return False, [f"audioPreview 必须为 0 或正 int"]
	if type(apre) is not int or apre <= 0:
		return False, [f"audioPreviewEnd 必须为正 int"]
	if apre <= apr:
		return False, [f"audioPreviewEnd 不得早于 audioPreview"]
	return True, []

def verify__comment(comment):
	valid = comment == "stdslstgen.js"
	return valid, [] if valid else [f"_comment 必须为 \"stdslstgen.js\""]

def verify_just_kidding(jk):
	valid = type(jk) is bool
	return valid, [] if valid else [f"just_kidding 必须为 bool"]

def verify_bg_and_side(bg, side, folder_path):
	msgs = []
	side_valid = True

	if type(side) is not int:
		msgs.append(f"side 必须为 int")
		side_valid = False
	elif side not in aafacc.allowed_sides:
		msgs.append(f"side 必须为 {aafacc.allowed_sides} 中的一个")
		side_valid = False

	if bg not in bgs.all_bgs:
		if not os.path.exists(os.path.join(folder_path, f"{bg}.jpg")):
			msgs.append(f"bg '{bg}' 不存在于官方背景列表，也未能找到自定义背景图")
	elif side_valid:
		side_name = bgs.get_side_name(side)
		if (side in [0, 2, 3] and bg not in bgs.general_light_bgs) or (side in [1] and bg not in bgs.conflict_bgs):
			msgs.append(f"side: {side}（{side_name}）与 bg： {bg} 不匹配")
	
	return len(msgs) == 0, msgs

def verify_difficulties(diff_list, folder_path):
	rcs = []
	activated_diffs = []
	msgs = []

	if type(diff_list) is not list:
		return False, ["difficulties 必须是 list"]
	
	if len(diff_list) < 3 or len(diff_list) > 4:
		msgs.append("difficulties 必须包括 3 或 4 个难度")

	for i, diff in enumerate(diff_list):
		if type(diff) is not dict:
			msgs.append(f"difficulties index-{i} 必须是 dict")

		if "ratingClass" not in diff:
			msgs.append(f"difficulties index-{i} 缺少字段 \"ratingClass\"")
			continue

		rc = diff['ratingClass']
		if type(rc) is not int:
			msgs.append(f"difficulties index-{i} 字段 \"ratingClass\" 必须为 int")
			continue
		if rc not in [0, 1, 2, 3, 4]:
			msgs.append(f"difficulties index-{i} 字段 \"ratingClass\" 必须为 [0, 1, 2, 3, 4] 中的一个")
			continue
		if rc in rcs:
			msgs.append(f"difficulties[{rc}] 重复")
			continue
		else:
			rcs.append(rc)
		
		for field in ["chartDesigner", "jacketDesigner"]:
			if field not in diff:
				msgs.append(f"difficulties[{rc}] 缺少字段 \"{field}\"")
			elif type(diff[field]) is not str:
				msgs.append(f"difficulties[{rc}].{field} 必须为 str")
		
		if "rating" not in diff:
			msgs.append(f"difficulties[{rc}] 缺少字段 \"rating\"")
		else:
			rating = diff["rating"]
			if type(rating) is not int or not (rating == -1 or rating > 0):
				msgs.append(f"difficulties[{rc}].rating 必须为 -1 或 正整数")
			elif rating != -1:
				activated_diffs.append(rc)
		
		if "ratingPlus" in diff:
			if diff["ratingPlus"] is not True:
				msgs.append(f"difficulties[{rc}].ratingPlus 存在时必须为 true")
	
	if not {0, 1, 2}.issubset(set(rcs)):
		msgs.append(f"difficulties 必须同时囊括 ratingClass 0、1、2")

	if 3 in rcs and 4 in rcs:
		msgs.append(f"difficulties 中不得同时出现 ratingClass 3、4")

	for activated_diff in activated_diffs:
		if not os.path.exists(os.path.join(folder_path, f"{activated_diff}.aff")):
			msgs.append(f"songlist 中声明了 ratingClass {activated_diff}，但未能找到对应的AFF文件")
	
	return len(msgs) == 0, msgs

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 检测文件夹结构')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()
	
	all_passed = True
	for entry in os.scandir(args.path):
		if not entry.is_dir():
			continue
		msgs = verify(entry.path)
		if msgs:
			print(f"{os.path.basename(entry.path)}")
			for msg in msgs:
				print(f"  - {msg}")
				all_passed = False

	if all_passed:
		print(f"  - 全部文件夹通过songlist检查")