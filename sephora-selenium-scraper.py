import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrollDown(driver, n_scroll):
    body = driver.find_element_by_tag_name("body")
    while n_scroll >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        n_scroll -= 1
    return driver

driver = webdriver.Chrome("/Users/richa/chromedriver")

url = "https://www.sephora.com/beauty/new-skin-care-products"
driver.get(url)

time.sleep(5)

browser = scrollDown(driver, 10)
time.sleep(2)

browser = scrollDown(driver, 10)
time.sleep(2)

browser = scrollDown(driver, 10)
time.sleep(2)

browser = scrollDown(driver, 10)
time.sleep(2)

browser = scrollDown(driver, 10)

# Get product names
product_names = []

try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    names = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='css-1gughuu']/span[2]")))
    for name in names:
        product_names.append(name.text)
except:
    pass

# Get product brands
product_brands = []

try:
    brands = browser.find_elements_by_xpath("//div[@class='css-1gughuu']/span[1]")
    for brand in brands:
        product_brands.append(brand.text)
except:
    pass

# Get product prices
product_prices = []

try:
    prices = browser.find_elements_by_xpath("//div[@class='css-68u28a']/span[1]")
    for price in prices:
        product_prices.append(price.text)
except:
    pass

# Get product links
product_links = []

try:
    links = browser.find_elements_by_xpath("//div[@class='css-1s223mm']/a")
    for link in links:
        link = link.get_attribute("href")
        product_links.append(link)
except:
    pass

# Loop through product links to get details of each product
product_details = []

for index, link in enumerate(product_links):
    driver.get(link)
    time.sleep(2)

    try:
        details = browser.find_elements_by_xpath("//div[@class='css-pz80c5']")
        for detail in details:
            product_details.append(detail.text)
    except:
        pass

driver.close()

# Remove empty values from product details list
while '' in product_details:
    product_details.remove('')

# Create dictionary for products
skincare_products = {}

skincare_products["Name"] = product_names
skincare_products["Brand"] = product_brands
skincare_products["Price"] = product_prices
skincare_products["Link"] = product_links
skincare_products["Details"] = product_details

# Save dictionary as pandas dataframe
df = pd.DataFrame(skincare_products)

# Remove products that don't have ingredients, e.g. skincare tools
df = df[df.Details.str.contains("Highlighted Ingredients")]

# Extract highlighted ingredients paragraph from all product details
product_ingredients = []
for df.Detail in df.Details:
    ingredients = re.findall("Ingredients:(.*)Ingredient", df.Detail, re.DOTALL) or re.findall("Ingredients:(.*)What", df.Detail, re.DOTALL)
    product_ingredients.append(ingredients)

skincare_products["Ingredients"] = product_ingredients

# Create ingredients column
df2 = pd.DataFrame(columns=["Ingredients"])
df = pd.concat([df, df2], axis = 1)

# Write to csv
df.to_csv("skincare_products.csv")
