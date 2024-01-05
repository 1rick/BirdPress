import os
import json
from jinja2 import Environment, FileSystemLoader
from markdown_processor import parse_markdown_file  # Import the function
from insert_posts import insert_blog_posts
from insert_cats_tags import insert_categories, insert_tags

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

# Set up Jinja environment globally
env = Environment(loader=FileSystemLoader('templates'))

def process_pages(input_dir, output_dir, template_dir):
    print(f"Starting to process pages from {input_dir}...")

    # Set up Jinja environment and register insert_blog_posts as a global function
    env = Environment(loader=FileSystemLoader(template_dir))
    # Register functions to be used in Jinja templates
    env.globals['insert_blog_posts'] = insert_blog_posts
    env.globals['insert_categories'] = insert_categories
    env.globals['insert_tags'] = insert_tags
    
    
    page_template = env.get_template('page.html')  # Use the global env instance

    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} not found. Creating it.")
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.md'):
            file_path = os.path.join(input_dir, file_name)
            # Capture noindex and nofollow values
            metadata, body, hero_image, (noindex, nofollow) = parse_markdown_file(file_path, is_page=True)
            if metadata is None:  # Skip draft pages
                continue
            if body:
                output = page_template.render(
                    page_title=metadata['title'],
                    page_content=body,
                    hero_image=hero_image,
                    noindex=noindex,  # Pass noindex to the template
                    nofollow=nofollow,  # Pass nofollow to the template
                    config=config
                )
                output_file_name = os.path.splitext(file_name)[0] + '.html'
                output_file_path = os.path.join(output_dir, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    print(f"Writing output to {output_file_path}")
                    output_file.write(output)
            else:
                print(f"Skipping file {file_name} due to errors.")


    print("Finished processing pages.")

if __name__ == '__main__':
    INPUT_DIR = 'input/pages'
    OUTPUT_DIR = 'output'
    TEMPLATE_DIR = 'templates'
    process_pages(INPUT_DIR, OUTPUT_DIR, TEMPLATE_DIR)
