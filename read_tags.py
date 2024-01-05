import os
import yaml
import json

def read_post_metadata(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('---')
        metadata = yaml.safe_load(content[1])
        return metadata

def collect_tags(input_dir):
    tags = {}
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.md'):
            file_path = os.path.join(input_dir, file_name)
            metadata = read_post_metadata(file_path)
            post_tags = metadata.get('tags', [])
            post_title = metadata.get('title', 'Untitled')

            for tag in post_tags:
                if tag not in tags:
                    tags[tag] = []
                post_info = {
                    'title': post_title,
                    'file_name': file_name.replace('.md', '.html')
                }
                tags[tag].append(post_info)

    with open('tags_data.json', 'w') as f:
        json.dump(tags, f)

if __name__ == '__main__':
    INPUT_DIR = 'input/posts'
    collect_tags(INPUT_DIR)
