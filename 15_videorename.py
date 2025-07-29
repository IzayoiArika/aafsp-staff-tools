import os
import argparse
import json

DIFFICULTY_MAP = {
    1: "Present",
    2: "Future",
    3: "Beyond",
    4: "Eternal"
}

CHAR_MAPPING = {
    '\\': '＼',
    '/': '／',
    ':': '：',
    '*': '＊',
    '?': '？',
    '"': '＂',
    '<': '＜',
    '>': '＞',
    '|': '｜',
}

def clean_filename(name):
    """将文件名中的非法字符转换为对应的全角字符"""
    cleaned = []
    for char in name:
        cleaned.append(CHAR_MAPPING.get(char, char))
    return ''.join(cleaned)

def main(path):
    
    if not os.path.exists(path):
        print(f"错误：路径 '{path}' 不存在")
        return
    
    json_path = os.path.join(path, 'merged_data.json')
    if not os.path.exists(json_path):
        print(f"错误：在 '{path}' 中找不到 merged_data.json 文件")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("错误：merged_data.json 格式不正确")
            return
    
    songs_dict = {}
    for song in data.get('songs', []):
        songs_dict[song['id']] = {
            'serial': song.get('serial', ''),
            'title': song.get('title', ''),
            'difficulties': [d['ratingClass'] for d in song.get('difficulties', [])]
        }
    
    for filename in os.listdir(path):
        if not filename.endswith('.mp4'):
            continue
        
        file_path = os.path.join(path, filename)
        
        base_name = os.path.splitext(filename)[0]
        
        diff = None
        song_id = base_name
        
        if '_' in base_name:
            parts = base_name.rsplit('_', 1)
            if parts[1].isdigit() and 1 <= int(parts[1]) <= 4:
                song_id = parts[0]
                diff = int(parts[1])
        
        song_info = songs_dict.get(song_id)
        if not song_info:
            print(f"警告：找不到歌曲ID '{song_id}' 的元数据 ({filename})")
            continue
        
        if diff is None:
            diffs = song_info['difficulties']
            if len(diffs) == 1:
                diff = diffs[0]
            else:
                print(f"错误：歌曲 '{song_id}' 有多个难度，但文件名未指定难度 ({filename})")
                continue
        
        if diff not in DIFFICULTY_MAP:
            print(f"错误：歌曲 '{song_id}' 的难度值 {diff} 无效 ({filename})")
            continue
        
        difficulty_name = DIFFICULTY_MAP[diff]
        new_name = f"{song_info['serial']}｜{song_info['title']}｜{difficulty_name}.mp4"
        
        new_name = clean_filename(new_name)
        new_path = os.path.join(path, new_name)
        
        # 执行重命名
        try:
            os.rename(file_path, new_path)
            print(f"重命名成功: {filename} -> {new_name}")
        except OSError as e:
            print(f"重命名失败 ({filename}): {str(e)}")
        except Exception as e:
            print(f"未知错误 ({filename}): {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename video files based on song metadata')
    parser.add_argument('--path', required=True, help='Path to directory containing video files and merged_data.json')
    args = parser.parse_args()
    
    main(args.path)