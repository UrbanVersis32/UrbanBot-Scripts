# UrbanBot autoshortdesc: Add short descriptions to pages in a category
# UV32 -- 07/01/2023
# Version 1.3.2

"""
CHANGELOG
Version 1.3.2
* Small change to edit output text

Version 1.3.1
* Improve edit counter

Version 1.3
* Critical bugfixes
* Refine output messages

Version 1.2.1
* Overall cleanup of code

Version 1.2
* Update to edit Wikidata instead of Wikipedia
* Check for existing short description on Wikidata before editing

Version 1.1
* Add bot Exclusion Compliance

Version 1.0
* Initial script
"""

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

scanned = 0 # Counter for all pages scanned through
counter = 0 # Counter for short descriptions added

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
			print("Short description already exists for " + page.title() + " on Wikidata.")
		else:
			# If not, update item with short description
			item.editDescriptions({"en": short_desc}, summary="UrbanBot - Adding description to item")
			print("Short description added to Wikidata item for " + page.title() + ": " + short_desc)
			counter += 1 # Add another short description to the counter
	scanned += 1

# Counter result
print("Process finished. UrbanBot scanned a total of " + str(scanned) + " items. Of these, it added descriptions to " + str(counter) + " items. There were " + str(scanned / counter) + " items scanned per item modified.")
