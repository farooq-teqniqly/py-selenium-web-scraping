from selenium import webdriver


class WebDriverFactory:
    @staticmethod
    def create_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        return webdriver.Chrome("chromedriver", options=options)
