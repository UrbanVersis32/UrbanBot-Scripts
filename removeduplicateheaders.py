# UrbanBot removeduplicateheaders: Remove headers from draft articles and AfC submissions that have the same name as the page title
# UV32 -- 06/29/2023
# Version 1.0

"""
CHANGELOG
Version 1.0
* Initial script
"""
# Imports
import pywikibot

# Main function to check the headers
def remove_duplicate_headers(page):
	site = page.site
	title = page.title()
	text = page.text

	# Split the text into lines
	lines = text.split("\n")

	new_lines = []
	for line in lines: # Check all lines of the page
		if line.startswith("="):
			header_text = line.strip("=").strip()
			if header_text.lower() == title.lower():
				# Skip this line if it has the same name as the page title
				continue

		# Add the line to the new lines list
		new_lines.append(line)

	# Join the new lines and save the updated text
	new_text = '\n'.join(new_lines)
	page.text = new_text
	page.save("UrbanBot - Removing duplicate headers")
	print("Duplicate header detected and removed")

# Ask user for page title without Draft:
draft_title = input("Enter the title of the draft article - Draft:")

site = pywikibot.Site("en", "wikipedia")
page = pywikibot.Page(site, "Draft:" + draft_title)
remove_duplicate_headers(page)
