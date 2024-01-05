import json
import os
from jinja2 import Environment, FileSystemLoader

def generate_css(config_file, css_output_dir, extras_dir):
    # Load the configuration
    with open(config_file, 'r') as file:
        config = json.load(file)

    # Determine the theme stylesheet path
    theme_stylesheet_path = os.path.join('templates', config['theme_stylesheet'])

    # Ensure the output directory exists
    os.makedirs(css_output_dir, exist_ok=True)

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(theme_stylesheet_path)))

    # Load the theme CSS template
    theme_template = env.get_template(os.path.basename(theme_stylesheet_path))

    # Render the CSS with configuration variables
    rendered_css = theme_template.render(config=config)

    # Append additional CSS if enabled
    extras = {
        'include_table_css': 'tables.css',
        'include_headings_css': 'headings.css',
        'include_button_css': 'buttons.css',
        'include_hr_css': 'hr.css',
        'include_codeblock_css': 'codeblocks.css',
        'include_lists_css': 'lists.css',
        'include_footnotes_css': 'footnotes.css',
        'include_blockquote_css': 'blockquotes.css'
    }

    for key, filename in extras.items():
        if config.get(key, False):
            with open(os.path.join(extras_dir, filename), 'r') as file:
                rendered_css += "\n\n" + file.read()

    # Write the rendered CSS to file
    output_css_file = os.path.join(css_output_dir, 'style.css')
    with open(output_css_file, 'w') as file:
        file.write(rendered_css)

if __name__ == '__main__':
    generate_css('CONFIG.json', 'input/static/css', 'templates/extras')
