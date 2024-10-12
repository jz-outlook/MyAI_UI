import allure
import pytest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Util.Action import perform_action, check_operation
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
    def test_case(self, driver, case):
        try:
            # 1. 检查 and 执行
            check_operation(driver, case['by'], case['Element_value'], case['action'], case)

            # 2. 检查操作后的状态
            if 'expected_element_by' in case and 'expected_element_value' in case:
                # 检查操作后预期元素是否存在
                with allure.step(f"验证元素 {case['expected_element_value']} 是否存在"):
                    expected_element = wait_for_element(driver, case['expected_element_by'],
                                                        case['expected_element_value'], timeout=10)
                    assert expected_element is not None, f"操作后预期元素 {case['expected_element_value']} 不存在"

            # 4. 操作完成后立即截图（无论成功与否）
            allure.attach(driver.get_screenshot_as_png(), name=f'Success_Screenshot_{case["id"]}',
                          attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            name = case['id']
            allure.attach(driver.get_screenshot_as_png(), name=f'Screenshot_{name}',
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(f"步骤 {name} 执行失败，异常信息: {e}", name=f"Error_{name}",
                          attachment_type=allure.attachment_type.TEXT)
            print(f'元素加载失败 {name}: {e}')
            pytest.fail(f"步骤 {name} 执行失败: {e}")


if __name__ == "__main__":
    pytest.main(['-vs'])
