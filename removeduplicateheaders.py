# UrbanBot removeduplicateheaders: Remove headers from draft articles and AfC submissions that have the same name as the page title
# UV32 -- 07/01/2023
# Version 1.4

"""
CHANGELOG
Version 1.4
* Re-add edit counter

Version 1.3
* Critical bugfixes

Version 1.2
* Add edit counter

Version 1.1
* Bot will scan through all drafts in a category, rather than in just one user-specified page
* Bot will output a message if a duplicate header is or isn't detected
* Add exclusion compliance

Version 1.0
* Initial script
"""
# Imports
import pywikibot

# Main function to check the headers
def remove_duplicate_headers(page, modified):
    # Local function variables
    site = page.site
    title = page.title()
    text = page.text
	
    # Split the text into lines
    lines = text.split("\n")

    new_lines = []
    
    duplicate_header_detected = False  # Flag to track duplicate header detection

    for line in lines:  # Check all lines of the page
        if line.startswith("=") or line.startswith("==") or line.startswith("==="):
            header_text = line.strip().lstrip("=").strip()
            if header_text.lower() == title.lower():
                duplicate_header_detected = True  # Set flag if duplicate header is detected
                continue # Skip this line if it has the same name as the page title
            elif header_text.lower().startswith("exclusion compliance"):
                # Skip lines starting with "Exclusion Compliance"
                continue

        # Add the line to the new lines list
        new_lines.append(line)

    # Join the new lines and save the updated text
    new_text = '\n'.join(new_lines)
    try:
        page.text = new_text
        page.save("UrbanBot - Removing duplicate headers")
    except pywikibot.exceptions.OtherPageSaveError as e:
        print(f"Error occurred while saving page {title}: {e}")

    if duplicate_header_detected:
        print("Duplicate header detected and removed in page " + title + ".")
        modified = True
    else:
        print("No duplicate header detected in page " + title + ".")
        modified = False

# Ask user for category name
category_name = input("Enter English Wikipedia category name: ")

site = pywikibot.Site("en", "wikipedia")
category = pywikibot.Category(site, category_name)

# Get pages in category
pages = category.members()

# Counters
scanned = 0
counter = 0

# Loop through pages and remove duplicate headers
for page in pages:
	# Check if page is in draft namespace
	if page.namespace() == 118:
		remove_duplicate_headers(page)
		if remove_duplicate_headers(modified) == True:
			counter += 1
		scanned += 1

# Counter result
if scanned > 0: # Make sure final message doesn't print before for loop is finished
	print("Process completed. UrbanBot scanned through a total of " + str(scanned) + " drafts. A total of " + str(counter) + " pages were modified by Urban bot which makes" + str(scanned / counter) + " pages scanned per draft modified.")
