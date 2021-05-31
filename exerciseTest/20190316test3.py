from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='chromedriver',chrome_options=chrome_options)
driver.get('https://tw.yahoo.com/')
print(driver.page_source)
driver.close()
driver.quit()