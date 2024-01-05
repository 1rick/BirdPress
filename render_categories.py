import os
import json
from jinja2 import Environment, FileSystemLoader
from xml.etree import ElementTree as ET
from datetime import datetime

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

def create_rss_feed(category, posts_info, output_file):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = f"{config['site_name']} - {category}"
    ET.SubElement(channel, 'description').text = f"{config['site_description']} - {category}"
    ET.SubElement(channel, 'link').text = config['base_url']

    for post in posts_info:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post['title']
        post_link = f"{config['base_url']}/{post['file_name']}"  # Removed additional "posts/"
        ET.SubElement(item, 'link').text = post_link
        ET.SubElement(item, 'description').text = post['title']  # Modify as needed for post summary/body

    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def render_category_pages(input_data_file, output_dir, template_dir):
    with open(input_data_file, 'r', encoding='utf-8') as f:
        categories = json.load(f)

    env = Environment(loader=FileSystemLoader(template_dir))
    category_template = env.get_template('category.html')

    os.makedirs(output_dir, exist_ok=True)

    for category, posts_info in categories.items():
        category_filename = category.replace(" ", "-").lower()  # Replace spaces with hyphens and make lowercase
        posts = [{'title': post['title'], 'url': f"/{post['file_name']}"} for post in posts_info]  # Corrected the URL format
        output = category_template.render(category=category, posts=posts, config=config)
        file_name = f"{category_filename}.html"
        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
            file.write(output)

        # Generate RSS feed if enabled in config
        if config.get('publish_category_feeds', False):
            rss_file = os.path.join(output_dir, f"{category_filename}.xml")
            create_rss_feed(category, posts_info, rss_file)

if __name__ == '__main__':
    INPUT_DATA_FILE = 'categories_data.json'
    OUTPUT_DIR = 'output/categories'
    TEMPLATE_DIR = 'templates'
    render_category_pages(INPUT_DATA_FILE, OUTPUT_DIR, TEMPLATE_DIR)
