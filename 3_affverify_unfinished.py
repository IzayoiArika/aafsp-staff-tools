## 未完成

import os
import re

def verify(folder_path):
	affs = []
	msgs = []

	for entry in os.scandir(folder_path):
		if entry.is_file() and entry.name.lower().endswith('aff'):
			affs.append(entry.path)
	
	if not affs:
		return [f"路径下不存在AFF文件"]

	for aff in affs:
		f_msgs = verify_aff(aff)
		if f_msgs:
			aff_name = os.path.basename(aff)
			for f_msg in f_msgs:
				msgs.append(f"{aff_name}: {f_msg}")
	
	return msgs

def verify_aff(aff_path):
	msgs = []

	offset = None
	try:
		with open(aff_path, 'r', encoding='utf-8') as f:
			ln = 0

			is_file_head = True

			for line in enumerate(f):
				ln += 1
				
				if line == '-':
					is_file_head = False
					continue

				if is_file_head:
					args, l_msgs = parse_fhead_args(line)
				
					if l_msgs:
						msgs += [f"第 {ln} 行: {l_msg}" for l_msg in l_msgs]
					
					if args and args[0] == 'AudioOffset':
						offset = args[1]
				else:
					args, l_msgs = parse_aff_args(line)
				

	except Exception as e:
		msgs.append(f"读取AFF文件失败: {str(e)}")

def parse_aff_args(line):

	args = [s.strip() for s in re.split(r'[(),\[\];]', line) if s.strip() not in ('arctap', 'at', '')]

def parse_fhead_args(line):
	args = [s.strip() for s in line.split(':')]
	core = args[0]
	msgs = []

	if len(args) != 2:
		msgs.append(f"语句非法: {line}")
		return [], msgs
	
	if core == 'AudioOffset':
		try:
			offset = int(args[1])
			return [core, offset], msgs
		except ValueError:
			msgs.append(f"AudioOffset 值必须为 int")
			return [], msgs
	elif core == 'TimingPointDensityFactor':
		try:
			tpdf = float(args[1])
			return [core, tpdf], msgs
		except ValueError:
			msgs.append(f"TimingPointDensityFactor 值必须为 float")
			return [], msgs
	else:
		msgs.append(f"语句非法: {line}")
		return [], msgs
