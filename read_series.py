import os
import yaml
import json

def read_post_metadata(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('---')
        metadata = yaml.safe_load(content[1])
        return metadata

def collect_series(input_dir):
    series = {}
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.md'):
            file_path = os.path.join(input_dir, file_name)
            metadata = read_post_metadata(file_path)
            series_tags = metadata.get('series_tag', [])
            post_title = metadata.get('title', 'Untitled')
            post_date = file_name.split('-')[0]  # date is part of the file name

            for tag in series_tags:
                if tag not in series:
                    series[tag] = []
                post_info = {
                    'title': post_title,
                    'file_name': file_name.replace('.md', '.html'),
                    'date': post_date
                }
                # Insert posts while maintaining chronological order
                series[tag].append(post_info)
                series[tag].sort(key=lambda x: x['date'])

    with open('series_data.json', 'w') as f:
        json.dump(series, f)

if __name__ == '__main__':
    INPUT_DIR = 'input/posts'
    collect_series(INPUT_DIR)
