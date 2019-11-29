Gigabyte distributors scraper
=============================

# Use

The scraper extracts dealers (distributors, resellers, retailers, online stores) for Gigabyte corporation products (Laptops, Grpahical Cards, Motherboards etc.) from their website's sales section https://www.gigabyte.com/Buy#,,1,1,1-0.

The script requires python 3 and selenium library so you need to install it via `pip install selenium`. It also uses chromedriver which is tested to work on Linux but if you use a different operating system, you may have to replace the chromedriver with the appropriate one for your system. You can find different drivers here https://sites.google.com/a/chromium.org/chromedriver/downloads.

To start scraping, run `python scraper.py`

# Required improvements

Currently the script scrapes only graphical cards from all regions. More versatility for the scraper is coming soon.