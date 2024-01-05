import os
import json
from datetime import datetime
from markdown_processor import parse_markdown_file

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

def extract_date_from_filename(file_name):
    """Extract the date from the filename assuming the format 'YYYYMMDD-title.md'"""
    date_str = file_name.split('-')[0]
    try:
        return datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        return None

def serialize_date(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def read_posts(input_dir):
    posts_data = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.md'):
            file_path = os.path.join(input_dir, file_name)
            metadata, body, hero_image, (noindex, nofollow) = parse_markdown_file(file_path, is_page=False)
            if metadata is None:  # Skip draft posts
                continue
            if body:
                post_date = extract_date_from_filename(file_name)
                if not post_date:
                    continue  # Skip files with invalid date format
                post_data = {
                    'file_name': file_name,
                    'metadata': metadata,
                    'body': body,
                    'hero_image': hero_image,
                    'noindex': noindex,
                    'nofollow': nofollow,
                    'post_date': post_date  # Include extracted date information
                }
                writtenby = metadata.get('writtenby', None)
                if writtenby:
                    post_data['writtenby'] = writtenby
                posts_data.append(post_data)

    with open('posts_data.json', 'w') as f:
        json.dump(posts_data, f, default=serialize_date)

if __name__ == '__main__':
    INPUT_DIR = 'input/posts'
    read_posts(INPUT_DIR)
