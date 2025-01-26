# UrbanBot autoshortdesc: Add short descriptions to English Wikipedia pages in a category
# UV32 -- 01/26/2025
# Version 1.9.1

"""
CHANGELOG
Version 1.9.1
* Bug fixes

Version 1.9
* Add a prompt asking to apply short desc for each page

Version 1.8
* Add additional processes to check if there is a template-applied short description on the page as well as the short desc template on the page

Version 1.7.1
* Add circumstance for user inputting "none" as a short description
* Improve output messages

Version 1.7
* Modify code to add the short description template to a page

Version 1.6
* Modify edit process to edit Wikipedia short descriptions instead of Wikidata descriptions (moving bot request and bot process to en-wiki instead)
* More improvements to the output information

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
from pywikibot import textlib

# Ask user for category name
category_name = input("INPUT: Enter English Wikipedia category name: ")

# Set up site and category
try:
    site = pywikibot.Site("en", "wikipedia")
    category = pywikibot.Category(site, category_name)
except:
    print("ERROR: Error 0 - Unable to access Wikipedia.")
    exit()

# Get pages in category
try:
    pages = category.members()
except: # Category does not exist
    print("ERROR: Error 1 - Wikipedia category specified does not exist.")
    exit()

# Ask user for category short descriptions
short_desc = input("INPUT: Enter short description for pages in category " + category_name + ": ")

if len(short_desc) > 40: # Likely too many characters
    desc_too_long = input("INPUT: Short description specified contains more than 40 characters. Continue? Y/n ")
    if desc_too_long.lower() == "n":
        print("EXIT: Exiting program")
        exit()

if len(short_desc) < 15: # Likely too few characters
    desc_too_short = input("INPUT: Short description specified contains fewer than 15 characters. Continue? Y/n ")
    if desc_too_short.lower() == "n":
        print("EXIT: Exiting program")
        exit()

if short_desc == "none" or short_desc == "None":
	short_desc = "none" # Make sure it's lowercase
	short_desc_none = input("INPUT: Short description inputted will cause the page to intentionally have no short description. Continue? Y/n ")
	if short_desc_none.lower() == "n":
		print("EXIT: Exiting program")
		exit()
	
print("INFO: Beginning write process.")

scanned = 0 # Counter for all pages scanned through
counter = 0 # Counter for short descriptions added

# Loop through pages, and add short descriptions
for page in pages:
    # Check if page already has template-applied short description
    if "Short description" in textlib.extract_templates_and_params(page.text, False, False):
        print("INFO: Template-applied short description already exists for " + page.title())
    else:
        # Check if page already has short description template
        if "{{Short description|" in page.text:
            print("INFO: Short description template already exists for " + page.title())
        else:
            # If not, update page with description template
            try:
                # Semi-automated check to ensure each page is applicable for the short desc
                allow = input("Do you want to add a short description for \"" + page.title() + "\"? Leave blank for yes, and enter anything for no:")
                if allow == "":
                    page.text = "{{Short description|" + short_desc + "}}\n" + page.text
                    page.save(summary="UrbanBot task 1 - Adding short description template")
                    print("ACTION: Short description template added to page " + page.title())
                    counter += 1 # Add another description to the counter
            except:
                print("ERROR: Error 2 - Unable to write short description template to English Wikipedia page")
    scanned += 1

if scanned == 0: # Prevent the divide by zero error
    scratio = 0
else:
    scratio = round(scanned / counter, 3) # Round to the hundredths place

# Counter result
if scanned > 0: # Make sure final message doesn't print before the for loop is finished
    print("INFO: Process finished. UrbanBot scanned a total of " + str(scanned) + " pages. Of these, it added short description templates to " + str(counter) + " pages. There were " + str(scratio) + " pages scanned per page modified.")
