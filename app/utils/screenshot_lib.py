"""
    屏幕截图模块
"""
import base64
from typing import Optional, Tuple

from PIL import Image
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class Driver:
    """ WebDriver instance """

    DEFAULT_DRIVER = "chromedriver"

    def __init__(self):
        self.driver_path: str = self.DEFAULT_DRIVER
        self.driver: Optional[Chrome] = None
        self.initial()

    def __enter__(self) -> "Driver":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """ 关闭模拟浏览器 """
        if self.driver is not None:
            print("Begin close...")
            self.driver.quit()

    def initial(self) -> None:
        options = Options()
        options.headless = True
        self.driver = Chrome(executable_path=self.driver_path, options=options)

    def save_screenshot(
        self,
        url: str,
        filename: str,
        class_name: Optional[str] = None,
        top: Optional[int] = None,
        left: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """
        :param url: 访问地址
        :param filename: 文件图片保存地址
        :param class_name: unique class name
        :param top: 顶
        :param left: 左
        :param width: 宽度
        :param height: 高度
        :return:
        """
        try:
            self.driver.get(url=url)
            self.driver.set_window_size(1920, 1080)
            self.driver.save_screenshot(filename)
            if class_name is not None:

                elem = self.driver.find_element_by_class_name(class_name)
                _left, _top = elem.location["x"], elem.location["y"]
                size_w, size_h = elem.size["width"], elem.size["height"]
                _right, _down = _left + size_w, _top + size_h

                if top is not None:
                    _top = top
                if left is not None:
                    _left = _left
                if width is not None:
                    _right = _left + width
                if height is not None:
                    _down = _top + height

                box = (_left, _top, _right, _down)
                self.img_crop(filename, box)
        except Exception as e:
            print(f"Exception in screenshot. errors: {e}")
            return False
        else:
            return True

    @staticmethod
    def img_crop(filename: str, box: Tuple, output: Optional[str] = None):
        """
        对图片进行裁剪
        :param filename: 原始图片地址
        :param box: 裁剪区域
        :param output: 处理后图片保存地址
        :return:
        """
        if output is None:
            output = filename
        with Image.open(filename) as img:
            img = img.crop(box)
            img.save(output)

    @staticmethod
    def to_base64(filename: str) -> str:
        """
        图片转 base64
        :param filename: 图片地址
        """
        with open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
