import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import csv
import os


def set_up_scraping(folder, logFileName='scrape_log.txt'):
    global logFilePath
    if not os.path.exists(folder):
        os.mkdir(folder)
    logFilePath = folder + '/' + logFileName
    logFile = open(logFilePath, 'w')
    logFile.write('')
    logFile.close()


# Checks for proper spelling of regions and whether they can be selected on website
def get_regions(regions):
    with open("regions.txt") as fajl:
        allRegs = [x.strip() for x in fajl.readlines()]
        if not regions:
            return allRegs
        else:
            for reg in regions:
                if reg not in allRegs:
                    print(
                        "ERROR, region = ", reg,
                        " is probably misspelled and cannot be found on gigabyte site, check your input again"
                    )
                    return []
            return regions


def scrape_logger(text):
    fh = open(logFilePath, 'a')
    fh.write(text + '\n')
    print(text)
    fh.close()


def select_field(driver, element_id, field, field_name):
    select = Select(driver.find_element_by_id(element_id))
    try:
        select.select_by_visible_text(field)
        scrape_logger("currently scraping", field, field_name)
    except:
        scrape_logger(field_name, field, 'could not be selected')
    time.sleep(3)


def scrape_region(driver, region, csv_dict_writer):

    # SELECT REGION BY VISIBLE TEXT
    select_field(driver=driver, element_id='country-select', field=region, field_name="region")

    # SELECT PRODUCT LINE BY VISIBLE TEXT
    select_field(driver=driver, element_id='productLine', field='Graphics Card', field_name='product')

    # SCRAPE REGION WITH SELECTED OPTIONS
    try:
        number_of_dealers = driver.find_elements_by_class_name("totalItem")[0].find_elements_by_class_name("items")[0].text
        if int(number_of_dealers) < 1:
            return
        else:
            scrape_logger("page loaded, ", number_of_dealers, " dealers found")
    except:
        scrape_logger("no dealers found in region ", region)
        continue

    end_pagination = False
    page = 1
    while not end_pagination:
        miniCards = driver.find_elements_by_css_selector("div.tag-inline.tag-inline-bottom")
        scrape_logger("on page ", page, " we have ", len(miniCards), " dealers")
        for card in miniCards:
            dealer = card.find_element_by_css_selector("div.storeName.Pc-storeName")
            company = dealer.text
            try:
                site = dealer.find_element_by_tag_name('a').get_attribute('href')
            except:
                site = ''
            other_fields = card.find_elements_by_css_selector("div.tag-inline.tag-inline-desc")
            product = other_fields[0].text
            try:
                address = other_fields[1].text
            except:
                address = ''
            if len(other_fields) >= 3:
                phone = other_fields[2].text
                record = {'Company': company, 'Country': region, 'Product': product, 'Address': address, 'Phone_Number': phone, 'Website': site}
                csv_dict_writer.writerow(record)
            else:
                print("    careful on page ", page, ", company = ", company, ", other fields have length ", len(other_fields), ", a phone number is probably missing")
                record = {'Company': company, 'Country': region, 'Product': product, 'Address': address, 'Phone_Number': None, 'Website': site}
                csv_dict_writer.writerow(record)
        page = page + 1
        try:
            next_page = driver.find_element_by_class_name("btn-group-next")
            time.sleep(3)
            next_page.click()
            time.sleep(3)
        except:
            end_pagination = True
            print("reached end of pagination\n")


def gigabyte_full_scrape(driver, filehandler, regions_to_select=[], site='https://www.gigabyte.com/Buy#,,1,1,1-0'):
    # 1. PREPAR EREGIONS YOU WISH TO SCRAPE
    regions = get_regions(regions_to_select)

    # 2. SCRAPE SETUP
    driver.get(site)
    record = {'Company': None, 'Country': None, 'Product': None, 'Address': None, 'Phone_Number': None, 'Website': None}
    csv_dict_writer = csv.DictWriter(filehandler, record.keys())
    csv_dict_writer.writeheader()
    time.sleep(3)

    # 3. SCRAPE EVERY REGION
    for reg in regions:
        scrape_region(driver, filehandler, reg, csv_dict_writer)


if __name__ == "__main__":

    # 1. POSTAVLJAMO OPCIJE ZA SELENIUM WEB DRIVER
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('chromedriver', chrome_options=options)

    # 2. OTVARAMO FOLDER I FAJLOVE U KOME SKLADIŠTIMO PODATKE
    folder = 'scraping_files'
    set_up_scraping(folder)
    outFileName = 'data.csv'
    with open(folder + '/' + outFileName, 'w') as filehandler:
        gigabyte_full_scrape(driver, filehandler)
