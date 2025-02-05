import os
import datetime
import time
from checks.models.rule import Rule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

driver = None
driver_usercount = 0
driver_lifetime = driver_lifetime_default = 100

def init_webdriver(force: bool = False):
    global driver, driver_usercount
    driver_usercount += 1
    if driver:
        if not force:
            return
        driver.quit()

    print("\nInitializing WebDriver...")
    language = os.popen(
        'powershell.exe -Command "Get-UICulture | Select-Object -ExpandProperty Name"'
    ).read().strip() or 'en-US'

    try:
        print("Trying to set up stealth driver...")
        import undetected_chromedriver as uc
        from selenium_stealth import stealth
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.54 Safari/537.36"
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--deny-permission-prompts')
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--window-position=-32000,-32000")
        # chrome_options.add_argument('--headless=new')
        # chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent={}".format(user_agent))
        service = Service(ChromeDriverManager().install())
        driver = uc.Chrome(service=service, options=chrome_options)
        stealth(driver,
            languages=[language, "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
        )
        print("Stealth driver set up successfully!")
    except Exception as e:
        print("Error setting up stealth driver: ", e)
        print("Falling back to regular Chrome driver...")

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
    global driver, driver_lifetime, driver_lifetime_default
    if driver_lifetime <= 0:
        print("\nWebdriver lifetime exceeded, resetting driver...")
        driver.get("about:blank")
        driver.delete_all_cookies()
        driver_lifetime = driver_lifetime_default
        time.sleep(1)
        print("Driver reset completed")
    print(f"Driver lifetime: {driver_lifetime}/{driver_lifetime_default}")
    driver_lifetime -= 1
    return driver

class RuleWebsite(Rule):

    def __init__(
            self, name: str,
            url: str,
            search_text: str,
            search_element: str|None = None,
            perform_cloudflare_check: bool = False,
            timeout: int = 1
    ):
        super().__init__()
        self.name = name
        self.__url = url
        self._identifier = hash(url)
        self.__search_text = search_text
        self.__search_element = search_element
        self.__perform_cloudflare_check = perform_cloudflare_check
        self.__timeout = timeout
        init_webdriver()

    def __del__(self):
        close_webdriver()

    def check(self) -> bool|str:
        result = False

        def get_website_content_selenium(url: str):
            print(f"\nChecking website with Selenium:\n{url}")
            driver = get_driver()
            driver.get(url)
            time.sleep(self.timeout)

            if self.perform_cloudflare_check:
                try:
                    script_elements = driver.find_elements(By.TAG_NAME, "script")
                    found_cloudflare = False
                    for script_element in script_elements:
                        if "cloudflare" in script_element.get_attribute("src"):
                            found_cloudflare = True
                            print("Cloudflare detected!")
                            print("Performing blind Cloudflare check...")
                            time.sleep(2)
                            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
                            ActionChains(driver) \
                                .key_down(Keys.SPACE) \
                                .key_up(Keys.SPACE) \
                                .perform()
                            time.sleep(4)
                            print("Blind Cloudflare check completed")
                            break
                    if not found_cloudflare:
                        print("No Cloudflare detected")
                except Exception as e:
                    print("Unable to perform blind Cloudflare check")

            return driver.page_source

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
            'perform_cloudflare_check': self.perform_cloudflare_check,
            'timeout': self.timeout
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            url=data['url'],
            search_text=data['search_text'],
            search_element=data.get('search_element', None),
            perform_cloudflare_check=data.get('perform_cloudflare_check', False),
            timeout=data.get('timeout', 1)
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

    @property
    def perform_cloudflare_check(self):
        return self.__perform_cloudflare_check

    @perform_cloudflare_check.setter
    def perform_cloudflare_check(self, perform_cloudflare_check: bool):
        self.__perform_cloudflare_check = perform_cloudflare_check

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int):
        self.__timeout = timeout