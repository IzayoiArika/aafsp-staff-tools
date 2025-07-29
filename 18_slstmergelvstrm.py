import argparse
import os
import json

DAVID_DICT = {
    'A': 'Aavid',
    'B': 'bat',
    'C': 'COM',
    'D': 'dn',
    'E': 'ehe?Toilet',
    'F': 'feat.',
    'G': 'gpoon',
}

def process_songlists(working_path):
    merged_data_path = os.path.join(working_path, 'merged_data.json')
    if not os.path.exists(merged_data_path):
        raise FileNotFoundError(f"merged_data.json not found in {working_path}")
    
    with open(merged_data_path, 'r', encoding='utf-8') as f:
        merged_data = json.load(f)
    
    song_info_map = {}
    for song in merged_data.get('songs', []):
        song_id = song.get('id')
        serial = song.get('serial')
        category = song.get('category')
        
        if not all([song_id, serial, category]):
            print(f"警告: 歌曲 {song_id} 缺少必要字段(serial/category)，已跳过")
            continue
            
        song_info_map[song_id] = (serial, category)
    
    all_songs = []
    
    for entry in os.listdir(working_path):
        song_dir = os.path.join(working_path, entry)
        
        if not os.path.isdir(song_dir):
            continue
            
        song_id = entry
        songlist_path = os.path.join(song_dir, 'songlist')
        
        if not os.path.exists(songlist_path):
            continue
            
        if song_id not in song_info_map:
            print(f"警告: 歌曲 {song_id} 不在merged_data.json中，已跳过")
            continue
            
        try:
            with open(songlist_path, 'r', encoding='utf-8') as f:
                song_data = json.load(f)
        except Exception as e:
            print(f"错误: 无法解析 {song_id}/songlist - {str(e)}")
            continue
            
        serial, category = song_info_map[song_id]
        
        if 'title_localized' not in song_data:
            song_data['title_localized'] = {}
            
        song_data['title_localized']['en'] = f"AAF: SP {serial} [{category}]"
        song_data['artist'] = f"\"{DAVID_DICT[category]}\""
        all_songs.append(song_data)
        
        try:
            os.remove(songlist_path)
            print(f"已处理: {song_id} - 删除原始songlist")
        except Exception as e:
            print(f"错误: 无法删除 {song_id}/songlist - {str(e)}")
    
    output_path = os.path.join(working_path, 'songlist')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"songs": all_songs}, f, ensure_ascii=False, indent=2)
    
    print(f"成功生成新的songlist文件: {output_path}")
    print(f"处理歌曲总数: {len(all_songs)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AAF:SP 歌曲列表处理器')
    parser.add_argument('--path', default='.', help='工作路径')
    args = parser.parse_args()
    
    process_songlists(args.path)