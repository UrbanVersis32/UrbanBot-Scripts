# UrbanBot Task 1: Add short descriptions to pages in a category
# Version 1.0
# UV32 -- 06/12/2023

import pywikibot

# Ask user for category name
category_name = input("Enter category name: ")

# Set up site and category
site = pywikibot.Site('en', 'wikipedia')
category = pywikibot.Category(site, category_name)

# Get pages in category
pages = category.members()

# Ask user for category short descriptions
short_desc = input("Enter short description for pages in category " + category_name + ": ")

# Loop through pages
for page in pages:
    # Check if page has short description
    if 'shortdesc' not in page.properties():
        # Update page with short description
        page.editDescriptions({site.lang: short_desc}, summary='UrbanBot task 1 - Adding short description')
        print(page.title() + " was successfully given the following short description: " + short_desc)
