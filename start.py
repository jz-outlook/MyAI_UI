import time

import pytest
from appium import webdriver
from Util.Action import perform_action
from Util.GetPath import GetPath
from Util.ReadExcelhandler import OperationExcel


class TestApp:

    @classmethod
    @pytest.fixture(scope='session', autouse=True)
    def driver(cls):
        caps = {
            "platformName": "Android",
            "appium:platformVersion": "14",
            "appium:deviceName": "49MRGIFUYH6XQKQS",
            "appium:appPackage": "vip.myaitalk.myai",
            "appium:appActivity": ".ui.SplashActivity",
            "appium:noReset": True,
            "ensureWebviewsHavePages": True,
            "nativeWebScreenshot": True,
            "newCommandTimeout": 60,
            "noRest": True,
            "autoGrantPermissions": True
        }
        driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", caps)
        return driver

    def test_start(self, driver):
        MyAI_case_path = GetPath().get_data_case_path()
        excel_data = OperationExcel(MyAI_case_path).read_excel()
        for data in excel_data:
            try:
                perform_action(driver, data['by'], data['Element_value'], data['action'], data)
            except Exception as e:
                name = data['id']
                print(f'元素加载失败{name, e}')
        time.sleep(10)
        driver.quit()


if __name__ == "__main__":
    pytest.main(['-vs', __file__])