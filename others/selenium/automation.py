# you have to download chromedriver to run the program
from selenium import webdriver

chrome_browser = webdriver.Chrome("./chromedriver")

chrome_browser.maximize_window()
chrome_browser.get("https://www.seleniumeasy.com/test/basic-first-form-demo.html")

assert "Selenium Easy Demo" in chrome_browser.title
button_text = chrome_browser.find_element_by_class_name("btn-default")
print(button_text.get_attribute("innerHTML"))

assert "Show Message" in chrome_browser.page_source

usr_msg = chrome_browser.find_element_by_id("user-message")
usr_b = chrome_browser.find_element_by_css_selector("#get-input > .btn")
print(usr_b)
usr_msg.clear()
usr_msg.send_keys("I am extra cool")

button_text.click()

output = chrome_browser.find_element_by_id("display")

assert "I am extra cool" in output.text

chrome_browser.close()
# .quit()