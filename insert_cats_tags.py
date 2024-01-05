import json

def insert_categories(show_rss=False, context="page"):
    # Disallow use in posts
    if context == "post":
        return "Usage of insert_categories in posts is not allowed."

    # Load the categories data
    with open('categories_data.json', 'r', encoding='utf-8') as file:
        categories_data = json.load(file)

    # Format the categories into HTML
    html_output = "<ul>"
    for category in categories_data.keys():
        category_url = f"categories/{category.replace(' ', '-').lower()}.html"
        rss_link = f" <a href='categories/{category.replace(' ', '-').lower()}.xml'>(RSS)</a>" if show_rss else ''
        html_output += f"<li><a href='{category_url}'>{category}</a>{rss_link}</li>"
    html_output += "</ul>"

    return html_output

def insert_tags(show_rss=False, context="page"):
    # Disallow use in posts
    if context == "post":
        return "Usage of insert_tags in posts is not allowed. Sorry. Truly, I am."

    # Load the tags data
    with open('tags_data.json', 'r', encoding='utf-8') as file:
        tags_data = json.load(file)

    # Format the tags into HTML
    html_output = "<ul>"
    for tag in tags_data.keys():
        tag_url = f"tags/{tag.replace(' ', '-').lower()}.html"
        rss_link = f" <a href='tags/{tag.replace(' ', '-').lower()}.xml'>(RSS)</a>" if show_rss else ''
        html_output += f"<li><a href='{tag_url}'>{tag}</a>{rss_link}</li>"
    html_output += "</ul>"

    return html_output