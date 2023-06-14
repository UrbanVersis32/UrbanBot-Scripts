# UrbanBot Task 1: Add short descriptions to pages in a category
# UV32 -- 06/14/2023
# Version 1.2.1

'''
CHANGELOG
Version 1.2.1
* Overall cleanup of code

Version 1.2
* Update to edit Wikidata instead of Wikipedia
* Check for existing short description on Wikidata before editing

Version 1.1
* Add bot Exclusion Compliance

Version 1.0
* Initial script

'''

# Imports
import pywikibot

# Ask user for category name
category_name = input("Enter English Wikipedia category name: ")

# Set up site and category
site = pywikibot.Site("en", "wikipedia")
category = pywikibot.Category(site, category_name)

# Get pages in category
pages = category.members()

# Ask user for category short descriptions
short_desc = input("Enter short description for pages in category " + category_name + ": ")

# Loop through pages, and add descriptions to their item
for page in pages:
    # Get Wikidata item for page
    item = pywikibot.ItemPage.fromPage(page)
    # Check on Wikidata if corresponding item exists
    if not item.exists():
        print("Corresponding Wikidata item for " + page.title() + " does not exist.")
    else:
        # Check if item has short description
        if "en" in item.descriptions and item.descriptions["en"] != "":
            print('Short description ("' + item.descriptions + '") already exists for ' + page.title() + ' on Wikidata.') # Using single quotes to show double quotes in the actual message.
        else:
            # If not, update item with short description
            item.editDescriptions({"en": short_desc}, summary="UrbanBot task 1 - Adding description to item")
            print("Short description added to Wikidata item for " + page.title() + ": " + short_desc)
