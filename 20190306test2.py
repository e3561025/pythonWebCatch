from selenium import webdriver

driver = webdriver.PhantomJS(executable_path="phantomjs-2.1.1-windows/bin/phantomjs")
driver.get('http://pala.tw/js-example/')
pageSource = driver.page_source
print(pageSource)
driver.close()