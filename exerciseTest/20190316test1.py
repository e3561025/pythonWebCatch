from selenium import webdriver

driver = webdriver.phantomjs(executable_path='phantomjs')
driver.get('http://www.pixiv.net/')
driver.save_screenshot('D:/python_Test/python-design/testjpg.png')  # 保存截圖

driver.close()
