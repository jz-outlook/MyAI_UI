import threading
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def check_operation(driver, by, value, action, case):
    if action == 'skip':
        pytest.skip("步骤为跳过步骤，将跳过此用例执行")
    try:
        perform_action(driver, by, value, action, case)
        if case.get('sleep') is not None:
            time.sleep(case['sleep'])
            print('执行了等待操作')
        else:
            time.sleep(0)
    except Exception as e:
        # 这里可以添加日志记录或者其他的异常处理逻辑
        print(f"执行操作时发生异常: {e}")
        raise



def wait_for_element(driver, by, value, timeout=20):
    """显性等待：等待元素出现在 DOM 中"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def perform_action(driver, by, value, action, data):
    # 显性等待目标元素
    element = wait_for_element(driver, data['by'], data['Element_value'], timeout=20)
    assert element is not None, f"元素 {data['Element_value']} 不存在或无法定位"

    try:
        if action == "click" and by == 'xpath':
            element = driver.find_element(by=AppiumBy.XPATH, value=value)
            element.click()

        elif action == 'class_name':
            element = driver.find_element(by=AppiumBy.CLASS_NAME, value=value)
            element.click()

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

        elif action == "move":
            # 定位到元素
            element = driver.find_element(by=AppiumBy.XPATH, value=value)
            element_location = element.location
            x = element_location['x']
            y = element_location['y']
            element_size = element.size
            height = element_size['height']
            width = element_size['width']
            # 计算元素中心点位置
            center_x = x + width / 2
            center_y = y + height / 2
            # 将点击位置下移10个像素
            offset_y = center_y + 30
            # 使用TouchAction执行点击操作
            action = TouchAction(driver)
            action.tap(x=center_x, y=offset_y).perform()


        elif action == 'Up_sliding':
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            # 屏幕中央起始位置
            actions.w3c_actions.pointer_action.move_to_location(529, 1187)
            actions.w3c_actions.pointer_action.pointer_down()
            # 滑动半屏
            actions.w3c_actions.pointer_action.move_to_location(529, 580)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            time.sleep(10)

        elif action == 'if':
            element = driver.find_element(by=AppiumBy.XPATH, value=value)
            element_text = element.text
            print("元素的文本是:", element_text)

        elif action == "long_press":
            number = int(data.get('duration', 1))  # 如果未设置时间，默认1秒钟
            duration = int(data.get('duration', number))
            element = driver.find_element(by=AppiumBy.ID, value=value)
            if data['sleep']:
                time.sleep(int(data['sleep']))

                # 查看元素当前的状态
                if ElementChecker().is_element_displayed(element) and ElementChecker().is_element_clickable(element):
                    # print('元素可见,可点击')
                    # print(f'分值的元素值是{Score_element}')
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
        name = data.get('id')
        print(f"该元素不存在直接跳过,元素ID:{name}")


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
