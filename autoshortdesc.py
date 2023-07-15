# UrbanBot autoshortdesc: Add short descriptions to English Wikipedia pages in a category
# UV32 -- 07/15/2023
# Version 1.7

"""
CHANGELOG
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

# Ask user for category name
category_name = input("Enter English Wikipedia category name: ")

# Set up site and category
try:
    site = pywikibot.Site("en", "wikipedia")
    category = pywikibot.Category(site, category_name)
except:
    print("Error 0 - Unable to access Wikipedia.")
    exit()

# Get pages in category
try:
    pages = category.members()
except: # Category does not exist
    print("Error 1 - Wikipedia category specified does not exist.")
    exit()

# Ask user for category short descriptions
short_desc = input("Enter short description for pages in category " + category_name + ": ")

if len(short_desc) > 40: # Likely too many characters
    desc_too_long = input("Short description specified contains more than 40 characters. Continue? Y/n ")
    if desc_too_long.lower() == "n":
        print("Exiting program")
        exit()

if len(short_desc) < 15: # Likely too few characters
    desc_too_short = input("Short description specified contains fewer than 15 characters. Continue? Y/n ")
    if desc_too_short.lower() == "n":
        print("Exiting program")
        exit()

print("Beginning write process.")

scanned = 0 # Counter for all pages scanned through
counter = 0 # Counter for short descriptions added

# Loop through pages, and add short descriptions
for page in pages:
    # Check if page already has description
    if "{{Short description|" in page.text:
        print("Short description template already exists for " + page.title())
    else:
        # If not, update page with description template
        try:
            page.text = "{{Short description|" + short_desc + "}}\n" + page.text
            page.save(summary="UrbanBot task 1 - Adding short description template")
            print("Short description template added to page " + page.title())
            counter += 1 # Add another description to the counter
        except:
            print("Error 2 - Unable to write short description template to English Wikipedia page")
    scanned += 1

if scanned == 0: # Prevent the divide by zero error
    scratio = 0
else:
    scratio = round(scanned / counter, 3) # Round to the hundredths place

# Counter result
if scanned > 0: # Make sure final message doesn't print before the for loop is finished
    print("Process finished. UrbanBot scanned a total of " + str(scanned) + " pages. Of these, it added short description templates to " + str(counter) + " pages. There were " + str(scratio) + " pages scanned per page modified.")
