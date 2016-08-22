import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import pyautogui
import Xlib.display


display = Display(visible=1, size=(600,400))
display.start()  # this changes the DISPLAY environment variable
# sadly, pyautogui does not detect this change
pyautogui._pyautogui_x11._display = Xlib.display.Display(
                os.environ['DISPLAY']
            )


#setting path variables for chromedriver and the prepd extension
path = os.path.dirname(os.path.abspath(__file__)) + "/"
executable_path = path + "chromedriver"
chrome_options = Options()
chrome_options.add_extension(path + "prepdFastCatch.crx")
chrome_options.add_argument("--start-fullscreen")

#initializing webdriver
driver = webdriver.Chrome(executable_path= executable_path, chrome_options=chrome_options)
driver.set_window_size(600,400)

driver.get("http://www.python.org")
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

while True:
    pyautogui.typewrite('Hello world!', interval=0.25)
#driver.get("chrome-extension://giahjhmjbiiopleefbmlmjfaafdihidd/index.html")

#driver.close()
