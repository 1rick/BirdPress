# Birdpress Static Site & Blog Generator

## To dos

- do a fallback font to google font api, for china at least. 
- photo gallery?
- heading colors?
- fix line height in h1 headers  (this may or may not be anything, I can't recall)
- fix logo icon / image options


## Introduction

Birdpress, like many static site generators, is a simpler alternative to some popular Content Management Systems that may or may not rhyme with Birdpress. You don't need any javascript frameworks to run it, nor does the generated site use any javascript. It's proudly just HTML and CSS. Once you've adjusted the CONFIG.json parameters to your liking (site colors, logo, title, etc), and entered your content in the input directory, the make_site.py processes Markdown files, and generates static HTML pages using Jinja2 templates. 

Detailed instructions are below, but if you don't want to read, you need a few steps to fire up birdpress:

1. Install python, if it's not already on your system.
2. Install requirements
3. Modify the CONFIG.json to your needs.
4. Run make_site.py to generate the site. 

## Quick Overview

- Converts Markdown files in an "input" directory to HTML in an "output" directory with a simple command:

```
python make_site.py
```

The input directory that holds your content will look roughly like this:

```
|- input
    |- index.md
    |- about.mb
    |- contact.md
    |- images
        |- example.png
        |- logo.png
        |- favicon.png
    |- posts
        |- 20231230-hello-world.md
        |- 20240115-another-post.md
```

And when the make_site.py script is run, the resultant HTML is then output as:

```
|- output
    |- index.html
    |- about.html
    |- contact.html
    |- images
        |- example.png
        |- logo.png
        |- favicon.png
    |- posts
        |- 20231230-hello-world.html
        |- 20240115-another-post.html
    |- rss.xml

```

The script does the following:

- Processes YAML metadata for additional information.
- Supports custom pages, blog posts, categories, and tags.
- Includes a Makefile for easy building and deployment.
- Customizable with Jinja2 templates.
- Generates RSS feeds for posts, as well as for categories and tags. 
 
## Installation
To set up Birdpress, follow these steps:

1. Clone this repository.
2. Install Python 
3. Install the required Python packages: "pip install -r requirements.txt". Use a [virtual environment](https://www.youtube.com/watch?v=IAvAlS0CuxI) if you wish. 

TKTK write more later

## What do I need to do?

Good question. There are a few files that will need your attention:

1. CONFIG.json: You can change the values in this file to your, site name and description, preferred custom colors, navigation menu items, and footer links and texts. 
2. input directory: this currently contains placeholder content, which you can change to be your own. Please note the format of the markdown files, particularly the meta data at the top. 
3. Use shortcodes to list your blog posts where you want it to display. (more on that below)

## Shortcodes:

Some people like to list their blog posts on the front page. Some people like to do that on pages like posts.html or blog.html, or news.html. You can put it on any page you wish (but not posts), with this handy shortcode:

```
{{ insert_blog_posts('all') }}
```

This code above, when placed in the body text of your markdown file, will list all your blog posts as an unordered list. 

```
{{ insert_blog_posts(5) }}
```
Similarly, the above code will list the 5 most recent posts, or whatever number of posts you decide to specify. 

You can also print the dates, by passing a "true" value for the "show dates" second parameter:

```
{{ insert_blog_posts('all', true) }}
```

### Meta Data Values

Typical values that you can declare at the top of your post/page are:

title: This is a test post title
categories: ["Writing", "Side Projects"]
tags: ["Japan"]

Important notes:

* **Dates**: Note that the date is extracted from the markdown filename, which - while not as tidy as keeping them organized in subfolders - is a simpler approach, in my view. Though I realzie some might debate this choice, and indeed a previous version of Birdpress handled date in the Yaml front matter. 
* **Categories & Tags**: Note the meta-data format here, as this can be a bit finnicky. While comma separated lists can work, I've opted to put them in quotes and in braces, because I ran into occasional issues with multi-word categories and tags, such as "Side Projects"  or "Hot Dogs". The convention in the example above is what I found works best. 

#### Other more specific meta data elements:

* draft: true (if you don't want your post or page published yet)
* noindex: true  (if you don't want search engines to index this page or post)
* nofollow: true  (if you don't want search engines to follow links in your posts. More on this property [here](https://www.ilovewp.com/seo-basics-meta-robots-noindexnofollow-explained/))


#### Fancy hero images

If you want fancy full-screen hero images at the top of your post or page, simply add a link to your hero image (in static/images) to your meta data:

```
hero_image: "../static/images/your_header.jpg"
```
Note that these hero images are typically wide rectangular things, so as long as you adhere to that shape, you should be fine. 

### Font Families

I've opted for Google Fonts in Birdpress for now, though I may revisit that decision later. Some font suggestions:


* Japanese: Noto Sans JP
* Korean: Noto Sans KR

## Usage

A few initial steps:

- In the input directory, you'll want to add your own posts and pages, as well as overwrite the logo and favicon files. But if you're just testing it out, you can use the current ones as placeholders. 

To generate your static site, simply run:

python make_site.py

This command processes all Markdown files in the `input` directory and outputs HTML files to the `output` directory.

To test locally, navigate to your output directory and run:

python3 -m http.server 8000 (or whatever port you want to try it out on), then navigate to http://0.0.0.0/8000 to view your site. 

To kill this process:

lsof -i :8000 (or whatever port it is)
and then "kill [PID]"

## Writing Content

#### Linking in Markdown Files

Creating links in your markdown files to other posts, pages, or static assets (like images or documents) is straightforward. Here's how you can do it:

* Internal Linking to Posts and Pages: To link to another post or page, use the relative URL path starting from the base URL. For example, if you have a post with the slug my-awesome-post, you can link to it using [My Awesome Post](/posts/my-awesome-post.html). Similarly, for a page, if you have a page with the filename about.md, you can link to it using [About](/about.html). (Note, I'm assuming here that you are viewing the plain text version of this readme file.)
* Internal Linking to Static Assets: If you want to include static assets like images or downloadable files, place them in the input/static directory. 
    * For example, if you have an image named cool-pic.jpg in input/static/images, you can embed it in your markdown post using ![Cool Picture](/static/images/cool-pic.jpg). 
    * Note that if you want "full bleed" or "full width" images that span beyond the width of the text column across the page, you can use plain HTML to insert your image with a full-bleed class: <img src="../static/images/cool-pic.jpg" alt="" class="full-bleed">  Note that of course, this works best with images of a rectangular shape that can span across your page well. 
    * For downloadable files like PDFs stored in input/static/files, link them using [Download PDF](/static/files/myfile.pdf).
* For any title that has a colon in it, special care is needed. For example, if you have a title of "Paris: City of Lights but the Food Isn't Great", then that title must be enclosed in quotes. 

Remember, all internal URLs should be relative to the base URL of your site, ensuring that your links remain intact regardless of the domain or subdirectory your site is hosted in.

Of course, linking to external sites is easy, e.g. [google](https://www.google.com).

## CSS Extras

For most people, the basic styling should suffice (I hope). But I've added a few more options which you can turn on/off in the bottom of the CONFIG.json file per your preference:

* "include_table_css": true (When set to true, any html tables (with a class of "tidyTable") will be a little cleaner. Note that the markdown renderer I'm using doesn't support markdown tables. tidyTableBut I'd recommend using Journalistopia's Tablizer tool to convert a spreadsheet table to a HTML table.)
* include_blockquotes_css: prettier blockquotes
* include_lists_css: prettier lists
* include_codeblocks_css: prettier codeblocks.
* include_footnotes_css: prettier footnote markers for markdown style footnotes.
* include_hr_css: a prettier horizontal rule.
* include_button_css: true, (when set to true, this gives fancy 
buttons for you to use for things like downloads or whatever I guess.)

### Button usage

If you want pretty buttons, you can use the html below when the buttons css extra is set to true:

```
<a href="your-link-1.html" class="button button-primary">Primary Solid</a>

<a href="your-link-2.html" class="button button-secondary">Secondary Solid</a>

<a href="your-link-3.html" class="button button-primary-outline">Primary Outlined</a>

<a href="your-link-4.html" class="button button-secondary-outline">Secondary Outlined</a>

```

### Markdown Extras

#### Table of Contents

If you have table of contents enabled in the config file, you can insert [TOC] at the top of a post or page to generate a table of contents for your page based on the headings. Learn more on the [table of contents extensions documentation page](https://python-markdown.github.io/extensions/toc/).

#### Markdown footnotes are enabled. 

As with table of contents above, if markdown footnotes are enabled in the config file, you can use them in Birdpress. Learn more over on the footnotes [extensions page](https://python-markdown.github.io/extensions/footnotes/).

### RSS Feeds

RSS feeds are awesome, so Birdpress has an RSS feed for your posts. Also, if you enabled in the config file, (i.e. if "publish_category_feeds" or "publish_tag_feeds" are set to true) then those feeds will be published, and will be listed on that category's or tag's page. In the example input, you'll see an RSS.md page which I think is a good way to present your feed, and it includes shortcodes to list category and tag feeds. Note that the feed is exposed in the site head by default. 

## Contributing
Contributions to Birdpress are welcome. Please feel free to submit pull requests or open issues to discuss potential improvements.

## License
[Your chosen license]

## Resources

**Color Tools**:

* [colorhunt.co](https://colorhunt.co/) - Lots of great color palettes to get inspiration from.
* [NipponColors.com](https://nipponcolors.com) - "Japanese" colors
* [0to255.com](https://0to255.com/) - A handy tool if you need to adjust a color to be darker or lighter, for contrast purposes. 

**Tables**:

* [Tableizer](https://tableizer.journalistopia.com/) - Make tables easily by copying from spreadsheet into this tool. 

**RSS**

* [Please expose your RSS](https://rknight.me/blog/please-expose-your-rss/)

**Logos**:

tktk

**Favicons**:

tktk
