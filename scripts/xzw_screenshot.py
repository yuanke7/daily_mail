import time
from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


class Driver:
    """ selenium web driver instance """
    DEFAULT_DRIVER = 'chromedriver'

    def __init__(self):
        self.driver_path = 'chromedriver'
        self.chrome = None
        self.initial()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def initial(self):
        if self.chrome is None:
            options = Options()
            options.headless = True
            if Path(self.driver_path).exists():
                executable_path = self.driver_path
            else:
                executable_path = self.DEFAULT_DRIVER
            self.chrome = webdriver.Chrome(
                executable_path=executable_path,
                options=options
            )

    def save_screenshot(self, url, filename, div_id=None):
        """
        :param url: 访问地址
        :param filename: 文件图片保存地址
        :param div_id: dom ID
        :return:
        """
        try:
            self.chrome.get(url=url)
            time.sleep(1)
            self.chrome.maximize_window()
            self.chrome.save_screenshot(filename)
            if div_id is not None:
                elem = self.chrome.find_element_by_class_name(div_id)
                left, top = elem.location['x'], elem.location['y']
                size_w, size_h = elem.size['width'], elem.size['height']
                print(left, top, size_h, size_w)
                box = (left, top, left + size_w, top + size_h)
                self.img_crop(filename, box)
        except TimeoutException as e:
            print(f'Exception in loading page. errors: {e}')
            return False
        except Exception as e:
            print(f'Exception in screenshot. errors: {e}')
            return False
        else:
            return True

    def close(self):
        """ 关闭模拟浏览器 """
        if self.chrome is not None:
            print('Begin close...')
            self.chrome.quit()

    @staticmethod
    def img_crop(filename, box, output=None):
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


if __name__ == "__main__":
    d = Driver()
    u = "https://www.xzw.com/fortune/cancer/"
    f = "./a.png"
    div = "c_main"
    d.save_screenshot(u, f, div)
