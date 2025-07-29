import argparse
import os
import shutil
import json

def distrib(working_path):
    json_path = os.path.join(working_path, 'merged_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    songs = data.get('songs', [])
    
    source_dirs = [
        'aff+ogg',
        'foolish_covers',
        'fx',
        'single_songlist'
    ]
    
    for song in songs:
        song_id = song.get('id')
        livestream = song.get('livestream')
        
        target_parent = os.path.join(working_path, f"__第{livestream + 1}场谱包")
        target_dir = os.path.join(target_parent, song_id)
        
        os.makedirs(target_parent, exist_ok=True)
        
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)
        
        for source_base in source_dirs:
            source_path = os.path.join(working_path, source_base, song_id)
            if not os.path.exists(source_path):
                continue
                
            for item in os.listdir(source_path):
                source_item = os.path.join(source_path, item)
                target_item = os.path.join(target_dir, item)
                
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, target_item)
                else:
                    shutil.copy2(source_item, target_item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AAF:SP 开盒分组')
    parser.add_argument('--path', default='.', help='工作路径')
    args = parser.parse_args()
    
    distrib(args.path)