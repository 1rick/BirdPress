import os
import yaml
import json

def read_post_metadata(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('---')
        metadata = yaml.safe_load(content[1])
        return metadata

def collect_categories(input_dir):
    categories = {}
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                metadata = read_post_metadata(file_path)
                post_categories = metadata.get('categories', [])
                post_title = metadata.get('title', 'Untitled')

                year = os.path.basename(os.path.dirname(file_path))  # Extract year from the file path
                for category in post_categories:
                    if category not in categories:
                        categories[category] = []
                    post_info = {
                        'title': post_title,
                        'file_name': os.path.join(year, file_name.replace('.md', '.html'))  # Include year in file name
                    }
                    categories[category].append(post_info)

    with open('categories_data.json', 'w') as f:
        json.dump(categories, f)

if __name__ == '__main__':
    INPUT_DIR = 'input/posts'
    collect_categories(INPUT_DIR)
