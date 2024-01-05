import os
import json
from xml.etree import ElementTree as ET
from datetime import datetime

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

def format_pub_date(date_str):
    try:
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
        return datetime_obj.strftime("%a, %d %b %Y %H:%M:%S +0000")
    except ValueError:
        return "Unknown Date"

def create_rss_feed(posts_data, output_file):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = config['site_name']
    ET.SubElement(channel, 'description').text = config['site_description']
    ET.SubElement(channel, 'link').text = config['base_url']

    for post in posts_data:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post['metadata']['title']
        post_link = f"{config['base_url']}/posts/{post['file_name'].replace('.md', '.html')}"
        ET.SubElement(item, 'link').text = post_link
        ET.SubElement(item, 'description').text = post['body']
        pub_date = format_pub_date(post['post_date'])
        ET.SubElement(item, 'pubDate').text = pub_date

    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def render_rss(input_data_file, output_dir):
    try:
        with open(input_data_file, 'r') as f:
            posts_data = json.load(f)
        output_file = os.path.join(output_dir, 'rss.xml')
        create_rss_feed(posts_data, output_file)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    INPUT_DATA_FILE = 'posts_data.json'
    OUTPUT_DIR = 'output'
    render_rss(INPUT_DATA_FILE, OUTPUT_DIR)
