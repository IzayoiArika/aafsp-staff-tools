import os
import re

VIOLATIONS = {
	"float_tap": "浮点Tap",
	"float_hold": "浮点Hold",
	"rescaled_arctap": "大小键",
	"designant_trace": "Designant红线",
	"camera": "Camera",
	"arcahvdistort": "Arcahv Distort",
	"arcahvdebris": "Arcahv Debris",
	"angle": "Angle",
	"flick": "Flick"
}
WARNINGS = {
	"fx_w_offset": "延迟不为0时，特殊天键音效会偏离正确位置"
}

def verify(folder_path):
	"""
	验证AFF文件
	返回: (success, messages)
	"""
	messages = []
	aff_files = []

	succeeded = True
	
	for entry in os.scandir(folder_path):
		if entry.is_file() and entry.name.lower().endswith('.aff'):
			aff_files.append(entry.path)
	
	if not aff_files:
		messages.append("该路径下没有AFF文件")
		return False, messages
	
	for aff_file in aff_files:
		file_msgs = []
		offset = None
		fxs = []
		violations = {key: False for key in [
			"float_tap", "float_hold", "rescaled_arctap", "designant_trace",
			"camera", "arcahvdistort", "arcahvdebris", "angle", "flick"
		]}
		warnings = {"fx_w_offset": False}
		
		try:
			ln = 0 # 行号
			with open(aff_file, 'r', encoding='utf-8') as reader:
				for line in reader:
					ln += 1

					args = [s.strip() for s in re.split(r'[(),:;]', line) if s.strip() != '']
					core = args[0]
					
					if core == "AudioOffset":
						offset = int(args[1])
					elif core == "" and len(args) > 2:
						if '.' in args[2]:
							violations["float_tap"] = True
					elif core == "hold" and len(args) > 3:
						if '.' in args[3]:
							violations["float_hold"] = True
					elif core == "flick":
						violations["flick"] = True
					elif core == "camera":
						violations["camera"] = True
					elif core == "scenecontrol" and len(args) > 3:
						if args[2] in ["arcahvdistort", "arcahvdebris"]:
							violations[args[2]] = True
						if '.' not in args[3]:
							file_msgs.append(f"第 {ln} 行 scenecontrol 语句语法错误：第 3 参数应为 float")
							succeeded = False
					elif core == "arc" and len(args) > 10:
						arctype = args[10]
						if arctype == "designant":
							violations["designant_trace"] = True
						elif arctype == "true":
							fx = args[9]
							if fx != "none" and fx not in fxs:
								fxs.append(fx)
								fx_name = fx.replace('_', '.')
								if not os.path.exists(os.path.join(folder_path, fx_name)):
									file_msgs.append(f"缺少音效文件: {fx_name}")
								if offset != 0:
									warnings["fx_w_offset"] = True
						else:
							if args[8] == "3" and args[1] == args[2]:
								violations["rescaled_arctap"] = True
					elif core == "timinggroup" and len(args) > 1:
						if any(s.startswith("angle") for s in args[1].split('_')):
							violations["angle"] = True
		except Exception as e:
			file_msgs.append(f"读取AFF文件失败: {str(e)}")
		
		# 添加违规信息
		for key, violated in violations.items():
			if violated:
				succeeded = False
				file_msgs.append(f"禁止使用: {VIOLATIONS[key]}")
		for key, warned in warnings.items():
			if warned:
				file_msgs.append(f"警告: {WARNINGS[key]}")
		
		if file_msgs:
			messages.append(f"文件 {os.path.basename(aff_file)} 存在以下问题:")
			messages.extend([f"  > {msg}" for msg in file_msgs])
	
	return messages

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 检测AFF内容')
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
		print(f"  - 全部文件夹通过AFF检查")