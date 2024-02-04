import os
import subprocess
import json
from copy_static import copy_static
from jinja2 import Environment, FileSystemLoader
from insert_posts import insert_blog_posts

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

# Define script names and paths
read_posts_script = 'read_posts.py'
read_categories_script = 'read_categories.py'
render_categories_script = 'render_categories.py'
read_tags_script = 'read_tags.py'
read_series_script = 'read_series.py'
render_tags_script = 'render_tags.py'
render_posts_script = 'render_posts.py'
render_rss_script = 'render_rss.py'
process_pages_script = 'process_pages.py'

# Define directories and other parameters
input_posts_dir = 'input/posts'
output_posts_dir = 'output/posts'
categories_dir = 'output/categories'
tags_dir = 'output/tags'
pages_dir = 'input/pages'
output_pages_dir = 'output'
template_dir = 'templates'
series_data_file = 'series_data.json'  # Path to series_data.json

# Initialize Jinja Environment
env = Environment(loader=FileSystemLoader(template_dir))
# Register the insert_blog_posts function to be used in Jinja templates
env.globals['insert_blog_posts'] = insert_blog_posts

def run_script(script_name, *args):
    print(f"Running {script_name}...")
    subprocess.run(['python', script_name] + list(args), check=True)

def main():
    # Run the CSS generation script first
    generate_css_script = 'process_css.py'
    css_output_path = 'output/static/css/style.css'
    run_script(generate_css_script, 'CONFIG.json', css_output_path)

    # Copy static files
    input_static_dir = 'input/static'
    output_static_dir = 'output/static'
    copy_static(input_static_dir, output_static_dir)

    # Then run other scripts in sequence
    run_script(read_posts_script, input_posts_dir)
    run_script(read_categories_script, input_posts_dir)
    run_script(render_categories_script, 'categories_data.json', categories_dir, template_dir)
    run_script(read_tags_script, input_posts_dir)
    run_script(read_series_script, input_posts_dir)
    run_script(render_tags_script, 'tags_data.json', tags_dir, template_dir)
    run_script(render_posts_script, 'posts_data.json', output_posts_dir, template_dir, series_data_file)
    run_script(render_rss_script, 'posts_data.json', output_pages_dir, template_dir)
    run_script(process_pages_script, pages_dir, output_pages_dir, template_dir)

if __name__ == '__main__':
    main()
