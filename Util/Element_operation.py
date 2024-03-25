from selenium.common.exceptions import NoSuchElementException


class ElementChecker:

    def is_element_clickable(self, element):
        try:
            return element.is_enabled()
        except NoSuchElementException:
            print("元素不可点击")
            return False

    def is_element_displayed(self, element):
        try:
            return element.is_displayed()
        except NoSuchElementException:
            print("元素不可见")
            return False

    def is_element_have(self, element):
        game_element = self.is_element_displayed(element)
        print("game_element的状态", game_element)
