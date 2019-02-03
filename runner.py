from SignIn import *
from test_params import username, password, video_id
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


videos = {"6bJrHkJ2M_I&t=":{"subscribe":0, "evaluate":"like"}}

options = Options()
options.headless = True
options.set_preference("media.volume_scale", "0.0")
browser = webdriver.Firefox(options=options, executable_path=r'C:\Users\Acer\Desktop\Python Projects\geckodriver.exe')

# SEND LOGIN AND PASSWORD FOR YOUTUBE
browser.get(('https://accounts.google.com/signin/v2/identifier?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26hl%3Den%26app%3Ddesktop%26action_handle_signin%3Dtrue&hl=en&uilel=3&service=youtube&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward'))
send_login(browser, username)
send_password(browser, password)

browser.get("https://www.youtube.com/watch?v={}".format(video_id))
sleep(1)  # 5
##
#sign_in(browser, videos)
sign_in(browser, username, password, video_id, "like", 1)

browser.quit()
