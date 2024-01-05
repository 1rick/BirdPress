import json
import os
from datetime import datetime

def format_date_from_filename(file_name):
    """Extract and format the date from the filename assuming the format 'YYYYMMDD-title.md'"""
    date_str = file_name.split('-')[0]
    try:
        return datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
        return "Unknown Date"

def insert_blog_posts(count, show_dates=False):
    # Load the posts data
    with open('posts_data.json', 'r', encoding='utf-8') as file:
        posts_data = json.load(file)

    # Sort posts by date in reverse chronological order
    posts_data.sort(key=lambda post: post['file_name'].split('-')[0], reverse=True)

    # Determine the number of posts to display
    if count == 'all':
        selected_posts = posts_data
    else:
        try:
            count = int(count)
        except ValueError:
            count = len(posts_data)  # If count is not an integer, default to all posts
        selected_posts = posts_data[:min(count, len(posts_data))]

    # Format the posts into HTML
    html_output = "<ul>"
    for post in selected_posts:
        post_url = os.path.splitext(post['file_name'])[0] + '.html'
        post_title = post['metadata']['title']
        post_date_formatted = format_date_from_filename(post['file_name'])

        date_str = f" - {post_date_formatted}" if show_dates else ''
        html_output += f"<li><a href='posts/{post_url}'>{post_title}</a>{date_str}</li>"
    html_output += "</ul>"

    return html_output
