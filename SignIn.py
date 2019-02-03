from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import multiprocessing
br = None
def send_login(browser, username_str):
    print(browser.current_url)
    username = browser.find_element_by_id('identifierId')
    username.send_keys(username_str)
    next_button = browser.find_element_by_id('identifierNext')
    next_button.click()
    browser.implicitly_wait(4)
    sleep(1)


def send_password(browser, password_str):
    password = WebDriverWait(browser, 1000000).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    password.send_keys(password_str)

    sign_in_button = browser.find_element_by_id('passwordNext')
    sign_in_button.click()
    browser.implicitly_wait(4)
    sleep(1)


def evaluate_video(browser, evaluate_way): #like, dislike, remove like, dislike
    browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[0].click()

    liked = browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[0].find_element_by_tag_name("yt-icon-button").get_attribute("aria-pressed")

    disliked = browser.find_element_by_id("top-level-buttons").find_elements_by_tag_name("ytd-toggle-button-renderer")[1].find_element_by_tag_name("yt-icon-button").get_attribute("aria-pressed")

    print("{} {} {}".format(evaluate_way,liked,disliked))

    if evaluate_way == "like":
        if liked == "true":
            print(3)
            return
        if liked == "false":
            print(4)
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[1]/a").click()
            return
    if evaluate_way == "dislike":
        if disliked == "true":
            print(5)
            return
        if disliked == "false":
            print(6)
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[2]/a").click()
            return
    if evaluate_way == "dismiss_all":
        if liked == "true":
            print(7)
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[1]/a").click()
            return
        if disliked == "true":
            print(8)
            browser.find_element_by_xpath("//*[@id='top-level-buttons']/ytd-toggle-button-renderer[2]/a").click()
            return


def subscribe_unsubscribe(browser, need_subscribe): #subscribe if 1 unsubscribe if 0
    subscribe_ = browser.find_element_by_xpath("//*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button").get_attribute("aria-label").startswith("Un")
    print("{} {}".format(need_subscribe,subscribe_))

    if subscribe_:
        if need_subscribe == 1:
            print(11)
            return
        if  need_subscribe == 0:
            print(12)
            subscribe = browser.find_element_by_xpath("//*[@id='subscribe-button']/ytd-subscribe-button-renderer/paper-button")
            subscribe.click()
            g = browser.find_element_by_xpath("//*[@id='confirm-button']/a")
            g.click()
            return
    if not subscribe_:
        if need_subscribe == 0:
            print(13)
            return
        if need_subscribe == 1:
            print(14)
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

"""
def evaluate( videos):
    global br
    for key in videos.keys():
        sleep(1)
        br.get("https://www.youtube.com/watch?v={}".format(key))
        sleep(1)
        evaluate_video(br, videos[key]["evaluate"])
        sleep(1)
        subscribe_unsubscribe(br, videos[key]["subscribe"])
        sleep(1)
        status(br)


def sign_in(browser, videos):
    global br
    br = browser
    status(br)
    br.implicitly_wait(4)

    with multiprocessing.Pool() as pool:
        pool.map(evaluate, videos)


"""
def sign_in(browser, username_str, password_str, video_id, evaluate_way, need_subscribe):
    status(browser)
    browser.implicitly_wait(4)

    #with multiprocessing.Pool() as pool:
     #   pool.map(evaluate, numbers)

    if evaluate_way in ["dislike", "like", "dismiss_all"]:
        print("1")
        evaluate_video(browser, evaluate_way)

    subscribe_unsubscribe(browser, need_subscribe)

    status(browser)

