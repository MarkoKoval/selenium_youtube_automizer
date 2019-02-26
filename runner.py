from SignIn import *
from test_params import username, password, video_id
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import  dill as  pickle
import copy


options = Options()
options.headless = True
options.set_preference("media.volume_scale", "0.0")
browser = webdriver.Firefox(options=options, executable_path=r"C:/Users\Acer\Desktop\Python Projects\geckodriver.exe")

print(browser.current_url)
# SEND LOGIN AND PASSWORD FOR YOUTUBE
browser.get("https://accounts.google.com/signin/v2/identifier?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26hl%3Den%26app%3Ddesktop%26action_handle_signin%3Dtrue&hl=en&uilel=3&service=youtube&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward")
send_login(browser, username)
send_password(browser, password)
print("browser {}".format(browser.current_url))
browser1 = copy.copy(browser)
browser2 = copy.copy(browser)
browser1.get('https://www.google.com/')
print("browser {}".format(browser.current_url))
print("browser1 {}".format(browser1.current_url))
print("browser2 {}".format(browser2.current_url))
#sign_in_(browser,  video_id, "like", 0)
#sign_in(browser, videos)
#sign_in(browser, video_id, "like", 1)
#browser.quit()
'''

if __name__ == "__main__":
    videos = {"6bJrHkJ2M_I&t=": {"subscribe": 0, "evaluate": "like"}}
    values = [(k, v["subscribe"], v["evaluate"]) for k, v in videos.items()]*8
    #print(values)
    start = time.time()
    find_sums(values)
    end = time.time()
    print(end - start)'''
#pickle serialization of gmail login