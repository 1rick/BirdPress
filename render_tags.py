import os
import json
from jinja2 import Environment, FileSystemLoader
from xml.etree import ElementTree as ET
from datetime import datetime

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

def create_rss_feed(tag, posts_info, output_file):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = f"{config['site_name']} - {tag}"
    ET.SubElement(channel, 'description').text = f"{config['site_description']} - {tag}"
    ET.SubElement(channel, 'link').text = config['base_url']

    for post in posts_info:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post['title']
        post_link = f"{config['base_url']}/posts/{post['file_name']}"
        ET.SubElement(item, 'link').text = post_link
        ET.SubElement(item, 'description').text = post['title']  # Modify as needed for post summary/body

    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def render_tag_pages(input_data_file, output_dir, template_dir):
    with open(input_data_file, 'r', encoding='utf-8') as f:
        tags = json.load(f)

    env = Environment(loader=FileSystemLoader(template_dir))
    tag_template = env.get_template('tag.html')

    os.makedirs(output_dir, exist_ok=True)

    for tag, posts_info in tags.items():
        tag_filename = tag.replace(" ", "-").lower()  # Format for filename
        posts = [{'title': post['title'], 'url': f"/posts/{post['file_name']}"} for post in posts_info]
        output = tag_template.render(tag=tag, posts=posts, config=config)
        file_name = f"{tag_filename}.html"
        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
            file.write(output)

        # Generate RSS feed if enabled in config
        if config.get('publish_tag_feeds', False):
            rss_file = os.path.join(output_dir, f"{tag_filename}.xml")
            create_rss_feed(tag, posts_info, rss_file)

if __name__ == '__main__':
    INPUT_DATA_FILE = 'tags_data.json'
    OUTPUT_DIR = 'output/tags'
    TEMPLATE_DIR = 'templates'
    render_tag_pages(INPUT_DATA_FILE, OUTPUT_DIR, TEMPLATE_DIR)
