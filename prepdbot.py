import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import pyautogui
import Xlib.display
import time

#user variables
email = ""
password = ""
maxTimeout = 30
shortTimeout = 2

#test stuff
theURL = raw_input("URL: ")

#application variables
firstRun = True

#initialize virtual display
display = Display(visible=1, size=(800,600))
display.start()
pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])


#setting path variables for chromedriver and the prepd extension
path = os.path.dirname(os.path.abspath(__file__)) + "/"
executable_path = path + "chromedriver"
chrome_options = Options()
#chrome_options.add_extension(path + "prepdFastCatch.crx")
#chrome_options.add_argument("--user-data-dir=" + path + "chrome")

chrome_options.add_argument("--user-data-dir=/home/isaac/git/prepdbot_v3/chromeContent")
print "--user-data-dir=" + path + "chrome"
chrome_options.add_argument("--test-type")
chrome_options.add_argument("--start-fullscreen")

#initializing webdriver
driver = webdriver.Chrome(executable_path= executable_path, chrome_options=chrome_options)
driver.set_window_size(800,600)
driver.implicitly_wait(maxTimeout)

print "text"

#function that actually cuts
def prepdBot(url):
    global email
    global password
    global firstRun
    global maxTimeout
    global shortTimeout
    global driver

    #open page
    print "URL: " + url
    driver.get(url)

    #on first opening
    if firstRun == True:
        #open and access prepd extension
        print "opening prepd extension"

        pyautogui.click(x=724, y=59, clicks=1, interval=0, button='left')
        driver.switch_to_frame(driver.find_element_by_id("fast-catch-KFoi8cNdjb"))

        #enter password and email
        print "authenticating"


        passwordElement = driver.find_element_by_xpath("//input[@placeholder='Password']")
        passwordElement.send_keys(password)

        emailElement = driver.find_element_by_xpath("//input[@placeholder='Email']")
        emailElement.send_keys(email)

        passwordElement.send_keys(Keys.RETURN)

    #click "next" button
    print "saving article"
    time.sleep(shortTimeout)
    driver.find_element_by_class_name("-important").click()
    print "clicked"

    '''
    #click "extemp" button

    driver.find_element_by_class_name("-extemp").click()
    '''

    #view article
    articleViewElement = driver.find_element_by_tag_name("a")

    articleViewURL = articleViewElement.get_attribute("href")
    print "Article View URL: " + articleViewURL

    #driver.switchTo().defaultContent();

    driver.get(articleViewURL)

    #highlighting
    print "*****************************"

    sentenceArray = driver.find_elements_by_xpath("//div[@data-paragraph-id]")

    for i in xrange(0,len(sentenceArray)):
        print sentenceArray[i]
        for j in xrange(0,len(sentenceArray[i])):
            if sentenceArray[i][j].isdigit():
                #highlighting
                for k in xrange(0,3):
                    sentenceArray[i][j].click()

                    actions = ActionChains(driver)

                    #hover over highlight div
                    highlightElement = driver.find_element_by_class_name("highlighter")
                    actions.move_to_element(highlightElement)

                    #hover over highlight color selector
                    highlightColorElement = driver.find_element_by_by_xpath("//div[@style = 'background-color: rgb(234, 227, 63);']")
                    actions.move_to_element(highlightColorElement)

                    actions.perform()

                break

    #set first run bool to false
    firstRun = False

    print "-----------------------------"

#runtime
prepdBot(theURL)
