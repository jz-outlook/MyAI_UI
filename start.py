import allure
import pytest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Util.Action import perform_action
from Util.GetPath import GetPath
from Util.ReadExcelhandler import OperationExcel

# 获取测试用例数据
MyAI_case_path = GetPath().get_data_case_path()
excel_data = OperationExcel(MyAI_case_path).read_excel()


@pytest.fixture(scope='session')
def driver():
    caps = {
        "platformName": "Android",
        "appium:platformVersion": "14",
        "appium:deviceName": "49MRGIFUYH6XQKQS",
        "appium:appPackage": "vip.myaitalk.myai",
        "appium:appActivity": ".ui.SplashActivity",
        "appium:noReset": False,
        "ensureWebviewsHavePages": True,
        "nativeWebScreenshot": True,
        "newCommandTimeout": 60,
        "autoGrantPermissions": True
    }
    # 初始化驱动并设置隐性等待
    driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", caps)
    driver.implicitly_wait(10)  # 设置隐性等待时间为 10 秒
    yield driver
    driver.quit()


def wait_for_element(driver, by, value, timeout=20):
    """显性等待：等待元素出现在 DOM 中"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


@allure.feature('UI自动化测试')
class TestApp:

    @pytest.mark.parametrize("case", excel_data)
    def test_ui_case(self, driver, case):
        try:
            # 使用显性等待确认元素存在后再进行操作
            wait_for_element(driver, case['by'], case['Element_value'], timeout=20)
            perform_action(driver, case['by'], case['Element_value'], case['action'], case)

            # 操作完成后立即截图（无论成功与否）
            allure.attach(driver.get_screenshot_as_png(), name=f'Success_Screenshot_{case["id"]}',
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            name = case['id']
            # 添加失败截图到 Allure 报告中
            allure.attach(driver.get_screenshot_as_png(), name=f'Screenshot_{name}',
                          attachment_type=allure.attachment_type.PNG)
            # 添加失败日志到 Allure 报告中
            allure.attach(f"步骤 {name} 执行失败，异常信息: {e}", name=f"Error_{name}",
                          attachment_type=allure.attachment_type.TEXT)
            # 打印错误并标记测试失败
            print(f'元素加载失败 {name}: {e}')
            pytest.fail(f"步骤 {name} 执行失败: {e}")


if __name__ == "__main__":
    pytest.main(['-vs'])
