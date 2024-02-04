import os
import json
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

def format_date(date_str):
    try:
        # Parse ISO format date string
        datetime_obj = datetime.fromisoformat(date_str)
        return datetime_obj.strftime("%B %d, %Y")
    except ValueError:
        return "Unknown Date"

def format_url_name(name):
    """Format names into lowercase and hyphenated for URLs."""
    return name.lower().replace(' ', '-')

def render_posts(input_data_file, output_dir, template_dir, series_data_file):
    # Load posts data
    with open(input_data_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)

    # Load series data within the function
    with open(series_data_file, 'r', encoding='utf-8') as f:
        series_data = json.load(f)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    post_template = env.get_template('post.html')

    for post in posts_data:
        body_html = markdown.markdown(post['body'])
        title = post['metadata']['title']
        date_posted = format_date(post['post_date'])
        writtenby = post['metadata'].get('writtenby', '')
        categories_links = [f"<a href='../categories/{format_url_name(category)}.html'>{category}</a>" for category in post['metadata'].get('categories', [])]
        tags_links = [f"<a href='../tags/{format_url_name(tag)}.html'>{tag}</a>" for tag in post['metadata'].get('tags', [])]
        info_line = f"Posted on {date_posted} under categories: {', '.join(categories_links)} and tagged {', '.join(tags_links)}"
        hero_image = post['metadata'].get('hero_image', '')

        series_line = ""  # Initialize series_line as empty
        
        # Check if post is part of a series
        series_tags = post['metadata'].get('series_tag', [])
        if series_tags:
            series_name = series_tags[0]  # Assuming one series per post for simplicity
            series_name_url = format_url_name(series_name)
            series_info = series_data.get(series_name, [])
            
            # Adjust the comparison to account for Markdown to HTML conversion
            for i, series_post in enumerate(series_info):
                expected_html_filename = os.path.splitext(post['file_name'])[0] + '.html'
                if series_post["file_name"] == expected_html_filename:
                    part_number = i + 1  # Adjust for 1-based indexing
                    # Update series_line to include hyperlinks to the series page and RSS feed
                    series_line = (f"This post is part {part_number} of the "
                                   f"<a href='/tags/{series_name_url}.html'>{series_name}</a> series "
                                   f"<a href='/tags/{series_name_url}.xml'>(RSS)</a>.")
                    break  # Exit loop after finding the post

        # Debugging: Print series line
        print(f"Series line for post '{title}': {series_line}")  
        
        # Render the post with Jinja2 template
        output = post_template.render(
            title=title, 
            content=body_html, 
            info_line=info_line, 
            series_line=series_line, 
            writtenby=writtenby,
            hero_image=hero_image,
            noindex=post.get('noindex', False),
            nofollow=post.get('nofollow', False),
            config=config
        )

        # Save the rendered HTML to a file
        output_file_name = os.path.splitext(post['file_name'])[0] + '.html'
        output_file_path = os.path.join(output_dir, output_file_name)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(output)

if __name__ == '__main__':
    INPUT_DATA_FILE = 'posts_data.json'
    OUTPUT_DIR = 'output/posts'
    TEMPLATE_DIR = 'templates'
    SERIES_DATA_FILE = 'series_data.json'  # Ensure this is correctly defined or passed as an argument
    render_posts(INPUT_DATA_FILE, OUTPUT_DIR, TEMPLATE_DIR, SERIES_DATA_FILE)
