import os
import datetime
import time
from checks.models.rule import Rule

driver = None
driver_usercount = 0

def init_webdriver():
    global driver, driver_usercount
    driver_usercount += 1
    if driver:
        return

    print("\nInitializing WebDriver...")
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    language = os.popen('powershell.exe -Command "Get-UICulture | Select-Object -ExpandProperty Name"').read().strip() or 'en-US'
    options = Options()
    options.headless = True
    options.add_argument(f'--lang={language}')
    # options.add_argument('--headless')
    options.add_argument('--log-level=3')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

def close_webdriver():
    global driver, driver_usercount
    driver_usercount -= 1
    if driver_usercount <= 0 and driver is not None:
        print("\nClosing WebDriver...")
        driver.quit()

def get_driver():
    global driver
    return driver

class RuleWebsite(Rule):

    def __init__(self, name: str, url: str, search_text: str, search_element: str|None = None):
        super().__init__()
        self.name = name
        self.__url = url
        self._identifier = hash(url)
        self.__search_text = search_text
        self.__search_element = search_element
        init_webdriver()

    def __del__(self):
        close_webdriver()

    def check(self) -> bool|str:
        result = False

        def get_website_content_selenium(url: str):
            print(f"\nChecking website with Selenium:\n{url}")
            get_driver().get(url)
            time.sleep(1)
            return get_driver().page_source

        content = get_website_content_selenium(self.url)
        file_name = f"{self.name}_{self.identifier}.html".replace(" ", "_").replace("/", "_")
        archive_path = os.path.join("archive", file_name)
        with open(archive_path, "w", encoding="utf-8") as file:
            file.write(content)

        if self.search_element:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            elements = soup.select(self.search_element)
            for element in elements:
                if self.search_text.lower() in element.get_text().lower():
                    result = True
        else:
            if self.search_text.lower() in content.lower():
                result = True

        self._last_status = self._status
        self._status = result
        self._last_run = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.status

    def to_dict(self):
        return {
            'class': self.__class__.__name__,
            'name': self.name,
            'url': self.url,
            'search_text': self.search_text,
            'search_element': self.search_element,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            url=data['url'],
            search_text=data['search_text'],
            search_element=data.get('search_element'),
        )

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url: str):
        self.__url = url

    @property
    def search_text(self):
        return self.__search_text

    @search_text.setter
    def search_text(self, search_text: str):
        self.__search_text = search_text

    @property
    def search_element(self):
        return self.__search_element

    @search_element.setter
    def search_element(self, search_element: str|None = None):
        self.__search_element = search_element

    @property
    def information(self):
        return f"URL: {self.url}"
