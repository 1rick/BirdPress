import os
import yaml
import markdown
import json
from jinja2 import Environment, FileSystemLoader
from insert_posts import insert_blog_posts  
from insert_cats_tags import insert_categories, insert_tags

# Load configuration
with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)

# Jinja environment setup
env = Environment(loader=FileSystemLoader('templates'))
    # Register functions to be used in Jinja templates
env.globals['insert_blog_posts'] = insert_blog_posts
env.globals['insert_categories'] = insert_categories
env.globals['insert_tags'] = insert_tags

def parse_markdown_file(file_path, is_page=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().split('---')
            if len(content) >= 3:
                metadata = yaml.safe_load(content[1])
                if metadata.get('status') == 'draft':
                    return None, None, None, None  # Skip draft posts/pages

                # Extract noindex and nofollow
                noindex = metadata.get('noindex', False)
                nofollow = metadata.get('nofollow', False)

                # Determine which Markdown extensions to enable
                markdown_extensions = []
                if config.get("enable_footnotes"):
                    markdown_extensions.append("markdown.extensions.footnotes")
                if config.get("enable_tableofcontents"):
                    markdown_extensions.append("toc")
                if config.get("enable_fenced_codeblocks"):  # Add fenced code blocks support
                    markdown_extensions.append("markdown.extensions.fenced_code")

                # Render content
                rendered_content = env.from_string(content[2].strip()).render(config=config)
                body = markdown.markdown(rendered_content, extensions=markdown_extensions)

                hero_image = metadata.get('heroimage', None)
                additional_data = metadata.get('writtenby', None) if not is_page else hero_image

                return metadata, body, additional_data, (noindex, nofollow)
            else:
                print(f"Warning: Incorrect format in Markdown file {file_path}")
                return None, None, None, None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML content in {file_path}: {e}")
        return None, None, None, None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None, None, None
