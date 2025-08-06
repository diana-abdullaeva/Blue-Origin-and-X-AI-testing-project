import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class WebDriverFactory:
    """Factory class for creating browser instances with proper configuration"""

    @staticmethod
    def create_chrome_driver(disable_javascript=False):
        """Create Chrome WebDriver with optimized settings"""
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if disable_javascript:
            chrome_options.add_argument("--disable-javascript")

        driver = webdriver.Chrome(options=chrome_options)
        if not disable_javascript:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        return driver

    @staticmethod
    def create_firefox_driver(disable_javascript=False):
        """Create Firefox WebDriver with optimized settings"""
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference('useAutomationExtension', False)
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        if disable_javascript:
            firefox_options.set_preference("javascript.enabled", False)

        driver = webdriver.Firefox(options=firefox_options)
        if not disable_javascript:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        return driver

    @staticmethod
    def create_edge_driver(disable_javascript=False):
        """Create Edge WebDriver with optimized settings"""
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")

        if disable_javascript:
            edge_options.add_argument("--disable-javascript")

        # Edge driver path configuration through environment variable
        if os.getenv('EDGE_DRIVER_PATH'):
            driver = webdriver.Edge(executable_path=os.getenv('EDGE_DRIVER_PATH'), options=edge_options)
        else:
            driver = webdriver.Edge(options=edge_options)

        if not disable_javascript:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        return driver

    @staticmethod
    def get_driver(browser_name, disable_javascript=False):
        """Get driver instance based on browser name"""
        browser_name = browser_name.lower()
        if browser_name == 'chrome':
            return WebDriverFactory.create_chrome_driver(disable_javascript)
        elif browser_name == 'firefox':
            return WebDriverFactory.create_firefox_driver(disable_javascript)
        elif browser_name == 'edge':
            return WebDriverFactory.create_edge_driver(disable_javascript)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")


class BlueOriginLocators:
    """Class containing all locators for Blue Origin career website"""

    # Main search page elements
    SEARCH_INPUT = (By.CSS_SELECTOR, ".JobBoardSearch_input__Y3mFB")
    SEARCH_BUTTON_ID = (By.ID, "job-board-search-submit-button")
    SEARCH_BUTTON_CLASS = (By.CSS_SELECTOR, ".JobBoardSearch_submitButton__SWZ48")
    SEARCH_BUTTON_TYPE = (By.CSS_SELECTOR, "button[type='submit']")

    # Job listings elements
    JOB_LISTING_TITLE = (By.CSS_SELECTOR, ".JobBoardListItem_title___2_Sp")
    JOB_LISTING_LINK = (By.CSS_SELECTOR, ".JobBoardListItem_link__kjhe9")
    JOB_LISTING_TITLE_LINK = (By.CSS_SELECTOR, ".JobBoardListItem_title___2_Sp a")
    JOB_LISTING_GENERIC = (By.CSS_SELECTOR, "a[class*='JobBoardListItem_link']")

    # Results count elements
    RESULTS_COUNT = (By.CSS_SELECTOR, ".JobBoardJobCount_count__2Yol3")
    JOB_FOUND_TEXT = (By.CSS_SELECTOR, 'p[data-automation-id="jobFoundText"]')

    # Navigation elements
    SEARCH_FOR_JOBS_BUTTON = (By.CSS_SELECTOR, 'button[data-automation-id="navigationItem-Search for Jobs"]')
    LOGO_LINK = (By.CSS_SELECTOR, 'a[data-automation-id="logoLink"]')
    KEYWORD_SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-automation-id="keywordSearchInput"]')

    # Header logo elements
    HEADER_LOGO_ID = (By.ID, "header-logo")
    HEADER_LOGO_CSS = (By.CSS_SELECTOR, "#header-logo")
    HEADER_LOGO_CLASS = (By.CSS_SELECTOR, ".HeaderLogo_headerLogo__2vsJe a")
    HEADER_LOGO_SPECIFIC = (By.CSS_SELECTOR, "a#header-logo")

    # Cookie consent elements
    COOKIE_SELECTORS = [
        (By.ID, "onetrust-accept-btn-handler"),
        (By.ID, "onetrust-button-group"),
        (By.CSS_SELECTOR, "#onetrust-button-group button"),
        (By.CSS_SELECTOR, "#onetrust-accept-btn-handler"),
        (By.XPATH, "//div[@id='onetrust-button-group']//button"),
        (By.XPATH, "//button[@id='onetrust-accept-btn-handler']"),
        (By.CSS_SELECTOR, ".onetrust-close-btn-handler"),
        (By.CSS_SELECTOR, ".accept-cookies-btn"),
        (By.XPATH, "//button[contains(text(), 'Accept')]"),
        (By.XPATH, "//button[contains(text(), 'Allow')]"),
    ]

    # Workday platform locators
    WORKDAY_COOKIE_SELECTORS = [
        (By.ID, "gdpr-cookie-accept"),
        (By.CSS_SELECTOR, "[data-automation-id='cookieAcceptButton']"),
        (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'OK')]"),
        (By.CSS_SELECTOR, ".css-1hwfws3"),
        (By.ID, "cookie-accept"),
    ]

    WORKDAY_JOB_COUNT_SELECTORS = [
        (By.CSS_SELECTOR, "[data-automation-id='jobFoundText']"),
        (By.CSS_SELECTOR, ".css-12psxof"),
        (By.XPATH, "//span[contains(text(), 'jobs') or contains(text(), 'Jobs')]"),
        (By.CSS_SELECTOR, "[data-automation-id='jobCount']"),
        (By.XPATH, "//div[contains(@class, 'job') and contains(text(), 'of')]"),
    ]

    WORKDAY_SEARCH_SELECTORS = [
        (By.CSS_SELECTOR, "[data-automation-id='keywordSearchInput']"),
        (By.CSS_SELECTOR, "input[placeholder*='Search']"),
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.XPATH, "//input[contains(@placeholder, 'search') or contains(@placeholder, 'Search')]"),
    ]

    WORKDAY_JOB_TITLE_SELECTOR = (By.CSS_SELECTOR, "[data-automation-id='jobTitle']")


class BlueOriginHelpers:
    """Helper class containing all methods for Blue Origin career testing"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.search_results_count = 0
        self.workday_url = "https://blueorigin.wd5.myworkdayjobs.com/en-US/BlueOrigin"
        self.workday_job_count = 0

    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears with improved error handling"""
        for selector_type, selector_value in BlueOriginLocators.COOKIE_SELECTORS:
            try:
                # Wait longer for cookie consent to appear
                cookie_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )

                # Check if element is visible
                if cookie_button.is_displayed():
                    # Scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cookie_button)
                    time.sleep(1)

                    # Wait for element to be clickable
                    clickable_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )

                    try:
                        # Try normal click first
                        clickable_button.click()
                    except ElementClickInterceptedException:
                        # If normal click fails, use JavaScript click
                        self.driver.execute_script("arguments[0].click();", clickable_button)

                    time.sleep(1)
                    return True

            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                continue

        # If cookie consent not found or couldn't click, it's not critical
        return False

    def handle_workday_cookie_consent(self):
        """Handle cookie consent on Workday site"""
        for selector_type, selector_value in BlueOriginLocators.WORKDAY_COOKIE_SELECTORS:
            try:
                cookie_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                cookie_button.click()
                time.sleep(1)
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False

    def find_first_job_listing(self):
        """Find and return the first job listing element"""
        selectors_to_try = [
            BlueOriginLocators.JOB_LISTING_TITLE,
            BlueOriginLocators.JOB_LISTING_LINK,
            BlueOriginLocators.JOB_LISTING_TITLE_LINK,
            BlueOriginLocators.JOB_LISTING_GENERIC
        ]

        for selector in selectors_to_try:
            try:
                first_job = self.wait.until(EC.element_to_be_clickable(selector))
                return first_job
            except TimeoutException:
                continue

        return None

    def click_element_safely(self, element):
        """Safely click an element with fallback to JavaScript click"""
        # Scroll to element before clicking
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)

        try:
            element.click()
        except ElementClickInterceptedException:
            # If normal click doesn't work, use JavaScript
            self.driver.execute_script("arguments[0].click();", element)

    def search_for_keyword(self, keyword):
        """Perform keyword search with multiple fallback options and improved error handling"""
        try:
            search_input = self.wait.until(EC.presence_of_element_located(BlueOriginLocators.SEARCH_INPUT))
            search_input.clear()
            search_input.send_keys(keyword)

            # Try to click search button or use Enter key
            search_button_found = False
            search_button_selectors = [
                BlueOriginLocators.SEARCH_BUTTON_ID,
                BlueOriginLocators.SEARCH_BUTTON_CLASS,
                BlueOriginLocators.SEARCH_BUTTON_TYPE,
                (By.XPATH, "//button[@type='submit' and contains(@class, 'JobBoardSearch_submitButton')]"),
                (By.XPATH, "//button[.//title[text()='Search']]"),
                (By.XPATH, "//button[@id='job-board-search-submit-button']")
            ]

            for selector in search_button_selectors:
                try:
                    search_button = self.driver.find_element(*selector)

                    # Try multiple click methods
                    try:
                        # Method 1: Regular click
                        search_button.click()
                        search_button_found = True
                        break
                    except ElementClickInterceptedException:
                        try:
                            # Method 2: Scroll to element and click
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
                            time.sleep(1)
                            search_button.click()
                            search_button_found = True
                            break
                        except ElementClickInterceptedException:
                            try:
                                # Method 3: JavaScript click
                                self.driver.execute_script("arguments[0].click();", search_button)
                                search_button_found = True
                                break
                            except:
                                continue
                except NoSuchElementException:
                    continue

            if not search_button_found:
                # Fallback to Enter key
                search_input.send_keys(Keys.RETURN)

            time.sleep(3)
            return True

        except TimeoutException:
            return False

    def search_with_special_characters(self, query_with_special_chars):
        """Search with special characters and spaces"""
        try:
            search_input = self.wait.until(EC.presence_of_element_located(BlueOriginLocators.SEARCH_INPUT))
            search_input.clear()
            search_input.send_keys(query_with_special_chars)
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
            return True
        except TimeoutException:
            return False

    def get_search_results_count(self):
        """Get the count of search results"""
        try:
            results_count_element = self.wait.until(
                EC.presence_of_element_located(BlueOriginLocators.RESULTS_COUNT)
            )
            results_text = results_count_element.text

            # Extract total number of jobs (e.g., from "Showing jobs 1 – 25 of 573")
            match = re.search(r'of (\d+)', results_text)
            if match:
                self.search_results_count = int(match.group(1))
            else:
                # Fallback: try to extract any number from the text
                numbers = re.findall(r'\d+', results_text)
                self.search_results_count = int(numbers[-1]) if numbers else 0

            return self.search_results_count

        except TimeoutException:
            return 0

    def check_keyword_relevance_in_results(self, keyword, max_results=5):
        """Check relevance of keyword in search results"""
        try:
            # Wait for job listings to load
            job_listings = self.wait.until(
                EC.presence_of_all_elements_located(BlueOriginLocators.JOB_LISTING_TITLE)
            )

            top_results = job_listings[:max_results]
            relevant_count = 0

            for result in top_results:
                result_text = result.text.lower()
                if keyword.lower() in result_text:
                    relevant_count += 1

            return relevant_count, job_listings

        except TimeoutException:
            return 0, []

    def navigate_to_search_jobs(self):
        """Navigate to search jobs page using button or logo link"""
        try:
            # Try to find "Search for Jobs" button first
            try:
                search_button = self.wait.until(
                    EC.element_to_be_clickable(BlueOriginLocators.SEARCH_FOR_JOBS_BUTTON)
                )
                search_button.click()
                return True
            except TimeoutException:
                # Fallback to logo link
                logo_link = self.wait.until(
                    EC.element_to_be_clickable(BlueOriginLocators.LOGO_LINK)
                )
                logo_link.click()
                return True

        except TimeoutException:
            return False

    def search_with_new_system(self, keyword):
        """Search using the new system interface"""
        try:
            search_input = self.wait.until(
                EC.presence_of_element_located(BlueOriginLocators.KEYWORD_SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(keyword)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)
            return True

        except TimeoutException:
            return False

    def get_new_system_results_count(self):
        """Get results count from the new system"""
        try:
            results_element = self.wait.until(
                EC.presence_of_element_located(BlueOriginLocators.JOB_FOUND_TEXT)
            )
            results_text = results_element.text  # e.g., "583 JOBS FOUND"

            match = re.search(r'(\d+)', results_text)
            return int(match.group(1)) if match else 0

        except TimeoutException:
            return 0

    def find_header_logo(self):
        """Find the header logo element"""
        header_logo_selectors = [
            BlueOriginLocators.HEADER_LOGO_ID,
            BlueOriginLocators.HEADER_LOGO_CSS,
            BlueOriginLocators.HEADER_LOGO_CLASS,
            BlueOriginLocators.HEADER_LOGO_SPECIFIC,
            (By.XPATH, "//img[@alt='Blue Origin | Careers']/.."),
            (By.XPATH, "//img[contains(@alt, 'Blue Origin') and contains(@alt, 'Careers')]/.."),
            (By.CSS_SELECTOR, ".HeaderLogo_headerLogo__2vsJe > a"),
            (By.CSS_SELECTOR, ".HeaderLogo_headerLogoImage__DkqYM/.."),
            (By.XPATH, "//span[contains(@class, 'HeaderLogo')]//a"),
        ]

        for selector in header_logo_selectors:
            try:
                header_logo = self.wait.until(EC.presence_of_element_located(selector))

                # Verify this is the correct logo element
                if header_logo.is_displayed() and header_logo.is_enabled():
                    # Check if it has the correct href (should be "/" for home page)
                    href = header_logo.get_attribute("href") or ""
                    if href.endswith("/") or "blueorigin.com" in href:
                        return header_logo

            except (TimeoutException, NoSuchElementException):
                continue

        return None

    def verify_blue_origin_content(self):
        """Verify that we're on a valid Blue Origin page"""
        blue_origin_content_selectors = [
            (By.XPATH, "//h1[contains(text(), 'Blue Origin')]"),
            (By.XPATH, "//img[contains(@alt, 'Blue Origin')]"),
            (By.CSS_SELECTOR, "[alt*='Blue Origin']"),
            (By.XPATH, "//title[contains(text(), 'Blue Origin')]"),
            (By.TAG_NAME, "title"),
        ]

        for selector_type, selector_value in blue_origin_content_selectors:
            try:
                elements = self.driver.find_elements(selector_type, selector_value)
                for element in elements:
                    if element.is_displayed() or selector_value == "title":
                        element_text = element.text.lower() if element.text else ""
                        if selector_value == "title":
                            element_text = self.driver.title.lower()
                        if "blue origin" in element_text:
                            return True
            except NoSuchElementException:
                continue

        # Additional check: verify page title contains Blue Origin
        page_title = self.driver.title.lower()
        return "blue origin" in page_title

    def navigate_with_keyboard(self, max_tabs=20):
        """Navigate using keyboard to find search jobs link"""
        actions = ActionChains(self.driver)

        for i in range(max_tabs):
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.5)

            # Check if current focused element is search jobs link
            focused_element = self.driver.switch_to.active_element
            element_text = focused_element.text.lower() if focused_element.text else ""
            element_href = focused_element.get_attribute("href") or ""

            if ("search job" in element_text or
                    "job search" in element_text or
                    "/careers/search" in element_href):
                return True

        return False

    def find_search_input_with_keyboard(self, max_tabs=10):
        """Find search input field using keyboard navigation"""
        actions = ActionChains(self.driver)

        for i in range(max_tabs):
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.5)

            focused_element = self.driver.switch_to.active_element
            if (focused_element.tag_name == "input" and
                    focused_element.get_attribute("type") in ["search", "text"]):
                return True

        return False

    # NEW METHODS FOR NEGATIVE TESTING

    def get_workday_job_count(self):
        """Get job count from Workday careers page"""
        try:
            self.driver.get(self.workday_url)
            time.sleep(2)  # Wait for page to load

            # Handle potential cookie consent on Workday
            self.handle_workday_cookie_consent()

            # Look for job count indicators on Workday
            for selector_type, selector_value in BlueOriginLocators.WORKDAY_JOB_COUNT_SELECTORS:
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    text = element.text

                    # Extract number from text like "1-25 of 583 jobs"
                    match = re.search(r'of (\d+)', text)
                    if match:
                        self.workday_job_count = int(match.group(1))
                        return self.workday_job_count

                    # Extract number from text like "583 jobs found"
                    match = re.search(r'(\d+)\s+jobs?', text, re.IGNORECASE)
                    if match:
                        self.workday_job_count = int(match.group(1))
                        return self.workday_job_count

                except (TimeoutException, NoSuchElementException):
                    continue

            # Fallback: count visible job listings
            job_listings = self.driver.find_elements(*BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTOR)
            if job_listings:
                return len(job_listings)

            return 0

        except Exception as e:
            print(f"Error getting Workday job count: {e}")
            return 0

    def search_workday_platform(self, keyword):
        """Search for keyword on Workday platform"""
        try:
            # Find search input on Workday
            for selector_type, selector_value in BlueOriginLocators.WORKDAY_SEARCH_SELECTORS:
                try:
                    search_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    search_input.clear()
                    search_input.send_keys(keyword)
                    search_input.send_keys(Keys.RETURN)
                    time.sleep(3)
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue

            return False

        except Exception as e:
            print(f"Error searching on Workday: {e}")
            return False

    def get_first_available_job_title(self):
        """Get the title of the first available job listing on the current page"""
        try:
            # Wait for page to load completely
            time.sleep(3)

            # Try different selectors to find job listings
            job_listing_selectors = [
                BlueOriginLocators.JOB_LISTING_TITLE,
                BlueOriginLocators.JOB_LISTING_TITLE_LINK,
                BlueOriginLocators.JOB_LISTING_LINK,
                (By.CSS_SELECTOR, "a[href*='/careers/']"),
                (By.CSS_SELECTOR, "h3 a"),
                (By.CSS_SELECTOR, ".job-title"),
                (By.CSS_SELECTOR, "[data-automation-id='jobTitle']"),  # Workday selector
                (By.CSS_SELECTOR, "h2 a"),
                (By.CSS_SELECTOR, "h1 a"),
                (By.XPATH, "//a[contains(@href, 'job') or contains(@href, 'career')]"),
            ]

            for selector in job_listing_selectors:
                try:
                    job_elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(selector)
                    )

                    # Find the first visible job element with meaningful text
                    for element in job_elements:
                        if element.is_displayed():
                            job_title = element.text.strip()
                            if job_title and len(job_title) > 5:  # Ensure it's a meaningful title
                                # Additional validation: check if it looks like a job title
                                job_keywords = ['engineer', 'manager', 'analyst', 'specialist', 'technician',
                                                'developer', 'designer', 'coordinator', 'director', 'associate',
                                                'intern', 'senior', 'junior', 'lead', 'principal', 'staff']

                                if any(keyword in job_title.lower() for keyword in job_keywords):
                                    return job_title

                                # If no job keywords found but if it's substantial text, use it anyway
                                if len(job_title) > 10:
                                    return job_title

                except (TimeoutException, NoSuchElementException):
                    continue

            # Fallback: try to extract from page source using regex
            page_source = self.driver.page_source
            import re

            # Look for job title patterns in HTML
            job_patterns = [
                r'<h[1-6][^>]*>([^<]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^<]*)</h[1-6]>',
                r'<a[^>]*href="[^"]*(?:careers|job)[^"]*"[^>]*>([^<]+)</a>',
                r'title="([^"]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^"]*)"',
                r'data-automation-id="jobTitle"[^>]*>([^<]+)<',
                r'class="[^"]*job[^"]*title[^"]*"[^>]*>([^<]+)<'
            ]

            for pattern in job_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    job_title = match.strip()
                    if job_title and len(job_title) > 5:
                        return job_title

            return None

        except Exception as e:
            print(f"Error getting first job title: {str(e)}")
            return None

    def get_first_workday_job_title(self):
        """Get the title of the first available job listing from Workday platform"""
        try:
            # Wait for Workday page to load completely
            time.sleep(2)

            # Try different selectors specific to Workday to find job listings
            workday_job_title_selectors = [
                (By.CSS_SELECTOR, "[data-automation-id='jobTitle']"),
                (By.CSS_SELECTOR, "a[data-automation-id='jobTitle']"),
                (By.CSS_SELECTOR, ".css-1id7k8c a"),
                (By.CSS_SELECTOR, "h3[data-automation-id='jobTitle']"),
                (By.CSS_SELECTOR, "div[data-automation-id='compositeHeaderContent'] a"),
                (By.CSS_SELECTOR, ".css-k008qs a"),
                (By.XPATH, "//a[@data-automation-id='jobTitle']"),
                (By.XPATH, "//h3[@data-automation-id='jobTitle']"),
                (By.XPATH, "//div[contains(@class, 'css-') and contains(@aria-label, 'job')]//a"),
                (By.CSS_SELECTOR, "a[href*='/job/']"),
            ]

            print("Searching for job titles on Workday using multiple selectors...")

            for i, selector in enumerate(workday_job_title_selectors):
                try:
                    print(f"Trying selector {i + 1}: {selector}")

                    # Wait for elements to be present
                    job_elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(selector)
                    )

                    print(f"Found {len(job_elements)} elements with selector {selector}")

                    # Find the first visible job element with meaningful text
                    for j, element in enumerate(job_elements):
                        try:
                            if element.is_displayed():
                                job_title = element.text.strip()
                                print(f"Element {j + 1} text: '{job_title}'")

                                if job_title and len(job_title) > 5:
                                    # Additional validation: check if it looks like a job title
                                    job_keywords = ['engineer', 'manager', 'analyst', 'specialist', 'technician',
                                                    'developer', 'designer', 'coordinator', 'director', 'associate',
                                                    'intern', 'senior', 'junior', 'lead', 'principal', 'staff',
                                                    'supervisor', 'administrator', 'consultant', 'officer',
                                                    'representative']

                                    job_title_lower = job_title.lower()

                                    # Check if it contains job-related keywords
                                    if any(keyword in job_title_lower for keyword in job_keywords):
                                        print(f"Found valid job title: '{job_title}'")
                                        return job_title

                                    # If no job keywords found but if it's substantial text and looks professional
                                    if (len(job_title) > 10 and
                                            not any(char in job_title for char in ['@', '#', '$', '%', '&']) and
                                            job_title.count(' ') >= 1):  # Has at least one space (multi-word)
                                        print(f"Found potential job title: '{job_title}'")
                                        return job_title

                        except Exception as e:
                            print(f"Error processing element {j + 1}: {str(e)}")
                            continue

                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Selector {selector} failed: {str(e)}")
                    continue

            # Fallback: try to extract from page source using regex patterns
            print("Primary selectors failed, trying regex fallback...")
            page_source = self.driver.page_source
            import re

            # Workday-specific regex patterns
            workday_job_patterns = [
                r'data-automation-id="jobTitle"[^>]*>([^<]+)<',
                r'<a[^>]*data-automation-id="jobTitle"[^>]*>([^<]+)</a>',
                r'<h3[^>]*data-automation-id="jobTitle"[^>]*>([^<]+)</h3>',
                r'aria-label="([^"]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^"]*)"',
                r'title="([^"]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^"]*)"',
            ]

            for i, pattern in enumerate(workday_job_patterns):
                print(f"Trying regex pattern {i + 1}: {pattern}")
                matches = re.findall(pattern, page_source, re.IGNORECASE)

                for match in matches:
                    job_title = match.strip()
                    if job_title and len(job_title) > 5:
                        print(f"Found job title via regex: '{job_title}'")
                        return job_title

            # Final fallback: look for any text that resembles a job title in common HTML structures
            print("Regex patterns failed, trying generic job title patterns...")
            generic_patterns = [
                r'<h[1-6][^>]*>([^<]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^<]*)</h[1-6]>',
                r'<a[^>]*href="[^"]*job[^"]*"[^>]*>([^<]+)</a>',
                r'<div[^>]*class="[^"]*job[^"]*title[^"]*"[^>]*>([^<]+)</div>',
            ]

            for pattern in generic_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    job_title = match.strip()
                    if job_title and len(job_title) > 5:
                        print(f"Found job title via generic pattern: '{job_title}'")
                        return job_title

            print("Could not find any job titles on Workday page")
            return None

        except Exception as e:
            print(f"Error getting first Workday job title: {str(e)}")
            return None

    def get_workday_search_results_count(self):
        """Get search results count from Workday after search"""
        try:
            # Wait for search results to load
            time.sleep(3)

            result_count_selectors = [
                (By.CSS_SELECTOR, "[data-automation-id='jobFoundText']"),
                (By.XPATH, "//span[contains(text(), 'jobs found') or contains(text(), 'Jobs Found')]"),
                (By.XPATH, "//div[contains(text(), 'of') and contains(text(), 'jobs')]"),
            ]

            for selector_type, selector_value in result_count_selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    text = element.text

                    # Extract number from various formats
                    match = re.search(r'(\d+)\s+jobs?\s+found', text, re.IGNORECASE)
                    if match:
                        return int(match.group(1))

                    match = re.search(r'of (\d+)', text)
                    if match:
                        return int(match.group(1))

                except (TimeoutException, NoSuchElementException):
                    continue

            # Fallback: count visible job listings
            job_listings = self.driver.find_elements(*BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTOR)
            return len(job_listings)

        except Exception:
            return 0

    def check_for_search_functionality(self):
        """Check if search functionality is still available on the page"""
        search_selectors = [
            BlueOriginLocators.SEARCH_INPUT,
            BlueOriginLocators.KEYWORD_SEARCH_INPUT,
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.CSS_SELECTOR, "input[placeholder*='search' i]"),
        ]

        for selector in search_selectors:
            try:
                search_element = self.driver.find_element(*selector)
                if search_element.is_displayed() and search_element.is_enabled():
                    return True
            except NoSuchElementException:
                continue

        return False

    def find_exact_job_title_in_results(self, exact_title):
        """Find exact job title in search results"""
        try:
            # Try Blue Origin selectors first
            try:
                job_listings = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(BlueOriginLocators.JOB_LISTING_TITLE)
                )
            except TimeoutException:
                # Try Workday selectors
                job_listings = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTOR)
                )

            for job in job_listings:
                if job.text.strip() == exact_title:
                    return True

            return False

        except TimeoutException:
            return False

    def test_javascript_disabled_career_functionality(self, test_case):
        """Test career page functionality with JavaScript disabled"""

        # Verify basic page accessibility
        page_title = self.driver.title
        test_case.assertIn("Blue Origin", page_title, "Page title not accessible without JavaScript")
        print(f"Page title accessible: {page_title}")

        # Check for basic HTML content
        try:
            body_element = self.driver.find_element(By.TAG_NAME, "body")
            body_text = body_element.text
            test_case.assertGreater(len(body_text), 100, "Page content not accessible without JavaScript")
            print(f"Page content accessible: {len(body_text)} characters")
        except NoSuchElementException:
            test_case.fail("Basic HTML body element not found")

        # Test navigation links accessibility
        try:
            nav_links = self.driver.find_elements(By.TAG_NAME, "a")
            accessible_links = [link for link in nav_links if link.is_displayed() and link.get_attribute("href")]
            test_case.assertGreater(len(accessible_links), 0, "No navigation links accessible without JavaScript")
            print(f"Found {len(accessible_links)} accessible navigation links")
        except Exception as e:
            print(f"Warning: Navigation links check failed: {str(e)}")

        # Test form elements accessibility (search inputs, etc.)
        form_elements_found = 0
        try:
            # Look for various input types
            input_selectors = [
                "input[type='search']",
                "input[type='text']",
                "input[name*='search']",
                "input[placeholder*='search' i]"
            ]

            for selector in input_selectors:
                try:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    visible_inputs = [inp for inp in inputs if inp.is_displayed()]
                    form_elements_found += len(visible_inputs)
                except:
                    continue

            if form_elements_found > 0:
                print(f"Found {form_elements_found} accessible form elements")

                # Try to interact with first accessible search input
                try:
                    search_input = None
                    for selector in input_selectors:
                        try:
                            inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for inp in inputs:
                                if inp.is_displayed() and inp.is_enabled():
                                    search_input = inp
                                    break
                            if search_input:
                                break
                        except:
                            continue

                    if search_input:
                        # Test basic input functionality
                        search_input.clear()
                        search_input.send_keys("test search")
                        entered_value = search_input.get_attribute("value")
                        test_case.assertEqual(entered_value, "test search",
                                              "Input field not functional without JavaScript")
                        print("Basic form input functionality works")

                        # Try form submission
                        try:
                            search_input.send_keys(Keys.RETURN)
                            time.sleep(2)
                            new_url = self.driver.current_url
                            print(f"Form submission attempted, current URL: {new_url}")
                        except Exception as e:
                            print(f"Form submission failed (expected without JS): {str(e)}")

                except Exception as e:
                    print(f"Form interaction test failed: {str(e)}")
            else:
                print("No accessible form elements found (may be JS-dependent)")

        except Exception as e:
            print(f"Form elements check failed: {str(e)}")

        # Test that page structure remains intact
        try:
            # Check for essential HTML elements
            essential_elements = [
                ("html", By.TAG_NAME, "html"),
                ("head", By.TAG_NAME, "head"),
                ("body", By.TAG_NAME, "body")
            ]

            for element_name, selector_type, selector_value in essential_elements:
                element = self.driver.find_element(selector_type, selector_value)
                test_case.assertIsNotNone(element, f"{element_name} element not found")

            print("Essential HTML structure intact")

        except NoSuchElementException as e:
            test_case.fail(f"Essential HTML structure compromised: {str(e)}")

        # Test CSS accessibility (styles should still load)
        try:
            # Check if any elements have computed styles
            body = self.driver.find_element(By.TAG_NAME, "body")
            background_color = self.driver.execute_script(
                "return window.getComputedStyle(arguments[0]).backgroundColor", body
            )
            if background_color and background_color != "rgba(0, 0, 0, 0)":
                print("✓ CSS styles are loading (some styling detected)")
            else:
                print("Basic CSS styling may not be applied")
        except Exception as e:
            print(f"CSS check failed: {str(e)}")

        # Verify no JavaScript errors crashed the page
        try:
            # Check if we can still interact with the page
            page_source = self.driver.page_source
            test_case.assertGreater(len(page_source), 1000, "Page source too short, may indicate crash")

            # Check for error messages in page content
            error_indicators = ["error", "failed", "not found", "500", "404"]
            page_text_lower = self.driver.find_element(By.TAG_NAME, "body").text.lower()

            critical_errors = []
            for indicator in error_indicators:
                if indicator in page_text_lower and ("page" in page_text_lower or "server" in page_text_lower):
                    critical_errors.append(indicator)

            if critical_errors:
                print(f"Warning: Possible error indicators found: {critical_errors}")
            else:
                print("✓ No critical error indicators detected")

        except Exception as e:
            test_case.fail(f"Page stability check failed: {str(e)}")

        # Final verification
        try:
            current_url = self.driver.current_url
            test_case.assertTrue(
                "blueorigin.com" in current_url.lower(),
                "Not on Blue Origin domain, possible redirect or crash"
            )
            print(f"Still on Blue Origin domain: {current_url}")

        except Exception as e:
            test_case.fail(f"Domain verification failed: {str(e)}")

        print("Career page handled JavaScript disabled state gracefully")



class BlueOriginUrls:
    """Class containing all URLs for Blue Origin career website"""

    BASE_URL = "https://www.blueorigin.com"
    CAREERS_URL = f"{BASE_URL}/careers"
    CAREERS_SEARCH_URL = f"{BASE_URL}/careers/search"
    WORKDAY_URL = "https://blueorigin.wd5.myworkdayjobs.com/en-US/BlueOrigin"