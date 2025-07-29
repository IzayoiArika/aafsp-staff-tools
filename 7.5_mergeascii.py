import argparse
import os
import json

def merge_ascii(working_path):
    # 1. 构建文件路径
    merged_file = os.path.join(working_path, 'merged_data.json')
    ascii_file = os.path.join(working_path, 'asciis.json')
    
    # 2. 检查文件是否存在
    if not os.path.exists(merged_file):
        raise FileNotFoundError(f"merged_data.json 文件不存在于: {working_path}")
    if not os.path.exists(ascii_file):
        raise FileNotFoundError(f"asciis.json 文件不存在于: {working_path}")
    
    # 3. 读取两个JSON文件
    with open(merged_file, 'r', encoding='utf-8') as f:
        merged_data = json.load(f)
    
    with open(ascii_file, 'r', encoding='utf-8') as f:
        ascii_data = json.load(f)
    
    # 4. 创建ASCII数据的ID映射（提高查找效率）
    ascii_map = {song['id']: song for song in ascii_data.get('songs', [])}
    
    # 5. 更新merged_data中的歌曲信息
    updated_count = 0
    for song in merged_data.get('songs', []):
        song_id = song.get('id')
        if not song_id:
            continue
        
        # 查找匹配的ASCII数据
        ascii_song = ascii_map.get(song_id)
        if not ascii_song:
            continue
        
        # 复制ASCII字段
        if 'title_ascii' in ascii_song:
            song['title_ascii'] = ascii_song['title_ascii']
        if 'artist_ascii' in ascii_song:
            song['artist_ascii'] = ascii_song['artist_ascii']
        
        updated_count += 1
    
    # 6. 保存更新后的merged_data.json
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    
    print(f"成功更新 {updated_count} 首歌曲的ASCII信息")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AAF:SP 合并ASCII信息')
    parser.add_argument('--path', default='.', help='工作路径')
    args = parser.parse_args()
    
    merge_ascii(args.path)