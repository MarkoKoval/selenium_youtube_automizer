from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import multiprocessing
import time
from test_params import username, password, video_id, geckodriver_exe_file_path
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


def send_login(browser, username_str):
    username = browser.find_element_by_id('identifierId')
    username.send_keys(username_str)
    next_button = browser.find_element_by_id('identifierNext')
    next_button.click()
    browser.implicitly_wait(4)
    sleep(2)


def send_password(browser, password_str):
    password = WebDriverWait(browser, 1000000).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    password.send_keys(password_str)

    sign_in_button = browser.find_element_by_id('passwordNext')
    sign_in_button.click()
    browser.implicitly_wait(4)
    sleep(2)


def evaluate_video(browser, evaluate_way): #like, dislike, remove like, dislike
    browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[0].click()

    liked = browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[0].find_element_by_tag_name("yt-icon-button").get_attribute("aria-pressed")

    disliked = browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[1].find_element_by_tag_name("yt-icon-button").get_attribute("aria-pressed")

    #print("{} {} {}".format(evaluate_way,liked,disliked))

    if evaluate_way == "like":
        if liked == "true":
            return
        if liked == "false":
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[1]/a").click()
            return
    if evaluate_way == "dislike":
        if disliked == "true":
            return
        if disliked == "false":
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[2]/a").click()
            return
    if evaluate_way == "dismiss_all":
        if liked == "true":
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[1]/a").click()
            return
        if disliked == "true":
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[2]/a").click()
            return


def subscribe_unsubscribe(browser, need_subscribe): #subscribe if 1 unsubscribe if 0
    subscribe_ = browser.find_element_by_xpath("//*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button").get_attribute("aria-label").startswith("Un")
    print("{} {}".format(need_subscribe,subscribe_))

    if subscribe_:
        if need_subscribe == 1:
            return
        if  need_subscribe == 0:
            subscribe = browser.find_element_by_xpath("//*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button")
            subscribe.click()
            g = browser.find_element_by_xpath("//*[@id='confirm-button']/a")
            g.click()
            return
    if not subscribe_:
        if need_subscribe == 0:
            return
        if need_subscribe == 1:
            subscribe = browser.find_element_by_xpath(
                "//*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button")
            subscribe.click()


def status(browser):
    print("Subscribed? {}".format(browser.find_element_by_xpath(
        "//*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button").get_attribute(
        "aria-label")))  # чи підписаний ти
    print("Liked? {}".format(
        browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[
            0].find_element_by_tag_name("yt-icon-button").get_attribute("aria-pressed")))


def sign_in_(browser,  video_id, evaluate_way, need_subscribe):
    browser.get("https://www.youtube.com/watch?v={}".format(video_id))
    sleep(1)  # 5
    status(browser)
    browser.implicitly_wait(4)

    if evaluate_way in ["dislike", "like", "dismiss_all"]:
        print("1")
        evaluate_video(browser, evaluate_way)

    subscribe_unsubscribe(browser, need_subscribe)

    status(browser)


def sign_in( values):
    start = time.time()
    options = Options()
    options.headless = True
    options.set_preference("media.volume_scale", "0.0")

    browser = webdriver.Firefox(options=options,
                                executable_path=geckodriver_exe_file_path)

    # SEND LOGIN AND PASSWORD FOR YOUTUBE
    browser.get((
                    'https://accounts.google.com/signin/v2/identifier?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26hl%3Den%26app%3Ddesktop%26action_handle_signin%3Dtrue&hl=en&uilel=3&service=youtube&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward'))
    send_login(browser, username)
    send_password(browser, password)

    video_id_,  need_subscribe, evaluate_way = values
    browser.get("https://www.youtube.com/watch?v={}".format(video_id_))
    sleep(1)  # 5
    status(browser)
    browser.implicitly_wait(4)

    if evaluate_way in ["dislike", "like", "dismiss_all"]:

        evaluate_video(browser, evaluate_way)

    subscribe_unsubscribe(browser, need_subscribe)

    status(browser)
    browser.quit()
    end = time.time()
    print(end - start)
    sleep(1)


def do_stuff_in_some_processes(values):
    print(multiprocessing.cpu_count())
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        pool.map(sign_in,  values)