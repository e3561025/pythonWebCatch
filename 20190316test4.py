
from selenium import webdriver
import time
options = webdriver.FirefoxOptions()
#options.set_headless(True)
a=time.time()
options.add_argument("--headless") #设置火狐为headless无界面模式
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver")
driver.get("https://tw.yahoo.com")
driver.get_screenshot_as_file("D:\\python_Test\\python-design\\test.png")
driver.get("https://www.cnblogs.com/mengyu/p/9706770.html")
driver.get_screenshot_as_file("D:\\python_Test\\python-design\\test2.png")
driver.quit()
b=time.time()
print(b-a)