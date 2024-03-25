import pytest
from appium import webdriver
from Util.Action import perform_action
from Util.GetPath import GetPath
from Util.ReadExcelhandler import OperationExcel

MyAI_case_path = GetPath().get_case_path()
excel_data = OperationExcel(MyAI_case_path).read_excel()


class TestApp:

    @classmethod
    @pytest.fixture(scope='session', autouse=True)
    def driver(cls):
        caps = {
            "platformName": "Android",
            "platformVersion": "10",
            "deviceName": "49MRGIFUYH6XQKQS",
            "appPackage": "vip.myaitalk.myai",  # 要测试的App
            "appActivity": ".ui.SplashActivity",  # 要测试的App活动
            "ensureWebviewsHavePages": True,
            "nativeWebScreenshot": True,
            "newCommandTimeout": 180,
            "connectHardwareKeyboard": True,
            "noRest": True,
            "autoGrantPermissions": True
        }
        driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", caps)
        try:
            driver.implicitly_wait(5)  # 隐式等待
        except Exception as e:
            print(f'超过最大等待时间{e}')
        return driver

    def test_start(self, driver):
        for data in excel_data:
            if data['mode'] == 'login':
                try:
                    perform_action(driver, data['by'], data['Element_value'], data['action'], data)
                except Exception as e:
                    name = data['Procedure']
                    print(f'元素加载失败{name, e}')
            elif data['mode'] == 'case':
                try:
                    perform_action(driver, data['by'], data['Element_value'], data['action'], data)
                except Exception as e:
                    name = data['Procedure']
                    print(f'元素加载失败name = {name, e}')
            else:
                case_name = data['Procedure']
                print(f'{case_name}用例执行完毕')
        print('所有用例执行完毕')


if __name__ == "__main__":
    pytest.main(['-vs', __file__])
