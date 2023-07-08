import requests
from PIL import Image
import img2pdf
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time
import random

# Name of the book
name = input('Paste the name of the book:')
# URL of the webpage you want to download
url = input('Paste the url here:')
# Service path
service_path = input('Paste the service path here. Default is C:/Program Files/Google/Chrome/Application/chromedriver.')\
               or "C:/Program Files/Google/Chrome/Application/chromedriver"
# content class
content_class = 'duxiuimg'
# The prefix of a image
base_url = 'http://img.estudy.dlufl.edu.cn/'

# Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Choose Chrome Browser
webdriver_service = Service(service_path)
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Find all the input tags with class 'Jimg'
inputs = soup.find_all('input', {'class': 'Jimg'})

# Extract the 'scr' attribute from each tag
scr_values = [i['scr'] for i in inputs if i.has_attr('scr')]

# Add each 'scr' value to the base url
urls = [base_url + scr for scr in scr_values]

# Pring massage.
print('Get urls sucessfully. This book consists of {} pages.'.format(len(urls)) )
print('You need to wait a while. To avoid being banned, script will sleep 1 second every image, 5 to 10 seconds every 5 images, 1 minute every 100 images.')

# Create the pdf file

# Make sure the name directory exists
if not os.path.exists(name):
    os.makedirs(name)

image_data = []

# Loop through the URLs and download the images
for index, url in enumerate(urls):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    # Save the image in a local file
    image_path = name+'/image_{}.png'.format(index)
    image.save(image_path)
    image_data.append(image_path)

    # Sleep 1 second every image
    time.sleep(1)

    # Sleep 5 to 10 seconds every 5 images
    if (index + 1) % 5 == 0:
        time.sleep(random.uniform(5, 10))

    # Sleep 1 minute every 100 images
    if (index + 1) % 100 == 0:
        time.sleep(60)

# Now convert the images to a PDF file
with open(name+'.pdf', "wb") as f:
    f.write(img2pdf.convert(image_data))

print('The book has been downloaded sucessfully.')
