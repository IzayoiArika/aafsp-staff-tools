import os
import datetime

def process_directory(directory_path):
	target_time = datetime.datetime(2000, 3, 18, 7, 21, 0)  # 目标时间：2000-03-18 07:21:00
	
	for root, _, files in os.walk(directory_path):
		try:
			os.utime(root, (target_time.timestamp(), target_time.timestamp()))
		except Exception as e:
			print(f"处理 {root} 时发生错误: {str(e)}")
			
		for filename in files:
			file_path = os.path.join(root, filename)
			try:
				os.utime(file_path, (target_time.timestamp(), target_time.timestamp()))
			except Exception as e:
				print(f"处理 {file_path} 时发生错误: {str(e)}")
	
	print(f"所有文件时间戳已统一设置为: {target_time}")

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='AAF:SP 统一修改时间')
	parser.add_argument('--path', default='.', help='工作路径')
	args = parser.parse_args()
	
	process_directory(args.path)