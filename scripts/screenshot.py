from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    def save_screenshot(self, url, filename, class_name=None, top=None, left=None, width=None, height=None):
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
            self.chrome.get(url=url)
            self.chrome.set_window_size(1920, 1080)
            self.chrome.save_screenshot(filename)
            if class_name is not None:
                elem = self.chrome.find_element_by_class_name(class_name)
                _left, _top = elem.location['x'], elem.location['y']
                size_w, size_h = elem.size['width'], elem.size['height']
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
    f = "../var/xinzuowu.png"
    _class = "c_main"
    d.save_screenshot(u, f, _class, height=535)

    u = "http://wufazhuce.com/"
    f = "../var/one.png"
    _class = "carousel-inner"
    d.save_screenshot(u, f, _class)
