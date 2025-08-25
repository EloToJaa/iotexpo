from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open a webpage
driver.get("https://www.example.com")

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()
