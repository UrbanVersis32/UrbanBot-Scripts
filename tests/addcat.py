# SCRIPT TEST_01

# UrbanBot's first test -- Add bot category to its userpage
# UV32, 06/12/2023

import pywikibot

site = pywikibot.Site("en", "wikipedia")
page = pywikibot.Page(site, "User:UrbanBot")

category = pywikibot.Category(site, 'All Wikipedia bots')
page.text += '\n[[{}]]'.format(category.title())
page.save('First test of UrbanBot: Add "All Wikipedia bots" category to its userpage')
