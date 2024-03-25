import threading
import time

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

from Util.Element_operation import ElementChecker
from Util.TTS_Util import TextToSpeechPlayer


def convert_to_integer(value):
    try:
        float_value = float(value)
        int_value = int(float_value)
        return int_value
    except ValueError:
        return value


def check_equality(var1, var2):
    start_time = time.time()  # 获取当前时间戳
    while var1 != var2:
        if time.time() - start_time >= 30:  # 如果持续时间超过30秒，退出循环
            break
        time.sleep(1)  # 每次等待1秒
    # 当两个变量相等时，或者持续时间超过30秒时，退出循环
    return var1 == var2


# 创建事件对象
event = threading.Event()


def long_press_thread_function(driver, value, duration, data, event):
    try:
        # 等待事件被设置
        event.wait()
        mp3_thread = threading.Thread(target=play_mp3_thread_function,
                                      args=(data, event))
        mp3_thread.start()

        element = driver.find_element(by=AppiumBy.ID, value=value)
        touch_action = TouchAction(driver)
        touch_action.long_press(element, duration=duration).release().perform()

    except NoSuchElementException:
        print("该元素不存在直接跳过")


Score_element = ''
Score = 0


def play_mp3_thread_function(data, event):
    event.wait()
    time.sleep(1)
    mp3 = data['tts']
    TextToSpeechPlayer().play_text(str(mp3))


def perform_action(driver, by, value, action, data):
    try:
        if action == "click" and by == 'xpath':
            element = driver.find_element(by=AppiumBy.XPATH, value=value)
            if element.is_enabled():
                element.click()
            else:
                print("元素不可点击，无法执行点击操作")

        elif action == 'text':
            element = driver.find_element(by=AppiumBy.XPATH, value=value)
            element_text = element.text
            global Score_element, Score
            Score_element = value
            Score = element_text
            print("元素的文本是:", element_text)

        elif action == "click" and by == 'id':
            element = driver.find_element(by=AppiumBy.ID, value=value)
            if element.is_enabled():
                element.click()
            else:
                print("元素不可点击，无法执行点击操作")

        elif action == "input":
            text = convert_to_integer(data['send_keys'])
            element = driver.find_element(by=AppiumBy.XPATH, value=value)
            if element.is_enabled():
                element.send_keys(text)
            else:
                print("元素不可点击，无法执行输入操作")

        elif action == "long_press":
            number = int(data.get('duration', 1))  # 如果未设置时间，默认1秒钟
            duration = int(data.get('duration', number))
            element = driver.find_element(by=AppiumBy.ID, value=value)
            if data['sleep']:
                time.sleep(int(data['sleep']))

                # 查看元素当前的状态
                if ElementChecker().is_element_displayed(element) and ElementChecker().is_element_clickable(element):
                    print('元素可见,可点击')
                    print(f'分值的元素值是{Score_element}')
                    # 设置事件，通知其他线程可以执行，启动长按操作的线程
                    event.set()
                    long_press_thread = threading.Thread(target=long_press_thread_function,
                                                         args=(driver, value, duration, data, event))
                    long_press_thread.start()
                    # # 查看一下游戏元素的状态
                    # value1 = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.LinearLayout'
                    # element1 = driver.find_element(by=AppiumBy.XPATH, value=value1)
                    # ElementChecker().is_element_have(element1)
                else:
                    return
            else:
                print("元素不可见，不可点击")

    except NoSuchElementException:
        name = data.get('name')
        print(f"该元素不存在直接跳过:{name}")


def check_last_digit_and_wait(number):
    # Convert number to string to easily access its last digit
    str_number = str(number)
    last_digit = int(str_number[-1])

    # Check if the last digit is greater than or equal to 7
    if last_digit >= 7:
        print("Last digit is greater than or equal to 7. Sleeping for 20 seconds...")
        time.sleep(20)
        print("Done sleeping.")
    else:
        print("Last digit is less than 7. No action taken.")
