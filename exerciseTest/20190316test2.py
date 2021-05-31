from selenium import webdriver
from time import sleep
driver = webdriver.Chrome(executable_path='D:/python_Test/python-design/chromedriver')
driver.get('http://sahitest.com/demo/index.htm')
print(driver.current_window_handle)  # 查看当前window handle

driver.find_element_by_link_text('Window Open Test').click()  # 打开新window1
driver.find_element_by_link_text('Window Open Test With Title').click()  # 打开新window2
print(driver.window_handles)  # 查看所有window handles
sleep(5)
driver.close()
print(driver.window_handles)  
# 查看现在的所有window handles，可看到只是关闭了最开始的一个window，其他两个window还在



sleep(5) #test 5 second

driver.quit()  # 看到所有window都被关闭 
