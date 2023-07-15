# UrbanBot autoshortdesc: Add short descriptions to pages in a category
# UV32 -- 07/14/2023
# Version 1.5.3

"""
CHANGELOG
Version 1.5.3
* Improvements to the output information
* Even more bugfixes

Version 1.5.2
* More bugfixes

Version 1.5.1
* Bugfixes

Version 1.5
* Improve error responding, bugfixes from 1.4

Version 1.4
* Improve error responding

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

"""
Error reference

Error 0 - Unable to access Wikipedia
Error 1 - Wikipedia category does not exist
Error 2 - Unable to access corresponding item for Wikipedia page
Error 3 - Unable to write description to Wikidata item
"""

# Imports
import pywikibot

# Ask user for category name
category_name = input("Enter English Wikipedia category name: ")

# Set up site and category
try:
	site = pywikibot.Site("en", "wikipedia")
	category = pywikibot.Category(site, category_name)
except:
	print("Error 0 - Unable to access Wikipedia.")
	
# Get pages in category
try:
	pages = category.members()
except: # Category does not exist
	print("Error 1 - Wikipedia category does not exist.")
	exit()

# Ask user for category short descriptions
short_desc = input("Enter short description for pages in category " + category_name + ": ")

if len(short_desc) > 40: # Likely too many characters
	desc_too_long = input("Description inputted contains more than 40 characters. Continue? Y/n ")
	if desc_too_long.lower() == "n":
		print("Exiting program")
		exit()

if len(short_desc) < 15: # Likely too few characters
	desc_too_short = input("Description inputted contains fewer than 15 characters. Continue? Y/n ")
	if desc_too_short.lower() == "n":
		print("Exiting program")
		exit()

print("Beginning write process.")
	
scanned = 0 # Counter for all pages scanned through
counter = 0 # Counter for short descriptions added

# Loop through pages, and add descriptions to their item
for page in pages:
	# Get Wikidata item for page
	item = pywikibot.ItemPage.fromPage(page)
	# Check on Wikidata if corresponding item exists
	if not item.exists():
		print("Error 2 - Corresponding Wikidata item for " + page.title() + " does not exist.")
	else:
		# Check if item already has description
		if "en" in item.descriptions and item.descriptions["en"] != "":
			print("Description already exists for " + page.title() + " on Wikidata.")
		else:
			# If not, update item with description
			try:
				item.editDescriptions({"en": short_desc}, summary="UrbanBot task 1 - Adding description to item")
				print("Description added to Wikidata item for " + page.title())
				counter += 1 # Add another description to the counter
			except:
				print("Error 3 - Unable to write description to Wikidata item")
	scanned += 1

if scanned == 0: # Prevent the divide by zero error
	scratio = 0
else:
	scratio = round(scanned / counter, 3) # Round to the hundredths place

# Counter result
if scanned > 0: # Make sure final message doesn't print before the for loop is finished
	print("Process finished. UrbanBot scanned a total of " + str(scanned) + " items. Of these, it added descriptions to " + str(counter) + " items. There were " + str(scratio) + " items scanned per item modified.")
