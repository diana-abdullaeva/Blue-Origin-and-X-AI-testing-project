#import AllureReports
#import HtmlTestRunner
import unittest
import time
from unittest.case import TestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from test_helpers import WebDriverFactory, BlueOriginHelpers, BlueOriginUrls


class BaseBlueOriginTest(TestCase):
    """Base test class with common setup and teardown"""

    browser_name = None  # To be overridden in subclasses

    def setUp(self):
        """Setup method executed before each test"""
        if not self.browser_name:
            raise NotImplementedError("browser_name must be set in subclass")

        self.driver = WebDriverFactory.get_driver(self.browser_name)
        self.helpers = BlueOriginHelpers(self.driver)

    def tearDown(self):
        """Teardown method executed after each test"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def _test_navigation_back_to_search(self):
        """TC_P_001: Verify navigation back to original search system via job details page"""
        # Step 1: Open careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(3)  # Increase wait time

        # Step 2: Click the first job listing with specific class
        first_job = self.helpers.find_first_job_listing()
        self.assertIsNotNone(first_job, "First job listing not found with any selector")

        self.helpers.click_element_safely(first_job)
        time.sleep(3)

        # Step 3: Find and click "Search for Jobs" button
        navigation_success = self.helpers.navigate_to_search_jobs()
        self.assertTrue(navigation_success, "Search for Jobs button not found")
        time.sleep(1)  # Wait no more than 1 second

        # Step 4: Verify the redirected URL
        current_url = self.driver.current_url
        expected_url = BlueOriginUrls.CAREERS_SEARCH_URL

        self.assertEqual(current_url, expected_url,
                        f"Expected exact URL {expected_url}, got: {current_url}")

    def _test_keyword_search_functionality(self):
        """TC_P_002: Verify keyword search functionality"""
        # Step 1: Open careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(2)

        # Step 2: Find the specific search input and enter "software"
        search_success = self.helpers.search_for_keyword("software")
        self.assertTrue(search_success, "Search input field not found")

        # Step 3: Check and save results count
        results_count = self.helpers.get_search_results_count()
        self.assertGreater(results_count, 0, f"No search results found. Count: {results_count}")

        # Step 4: Check relevance of first 5 results
        relevant_count, job_listings = self.helpers.check_keyword_relevance_in_results("software", 5)
        self.assertGreater(relevant_count, 0,
                          f"No 'software' keyword found in top 5 results. Relevant count: {relevant_count}")

        # Click on first result for next test
        if job_listings:
            self.helpers.click_element_safely(job_listings[0])
            time.sleep(2)

    def _test_search_results_consistency(self):
        """TC_P_003: Verify consistency of search results across systems"""
        # First, run the search from TC_P_002 to get baseline
        self._test_keyword_search_functionality()

        # Now we're on a job details page after clicking on a job from search results
        # Find and click either "Search for Jobs" button or logo link
        navigation_success = self.helpers.navigate_to_search_jobs()
        self.assertTrue(navigation_success, "Neither Search for Jobs button nor logo link found")
        time.sleep(2)

        # Enter "software" in the search input
        search_success = self.helpers.search_with_new_system("software")
        self.assertTrue(search_success, "Keyword search input not found")

        # Get results count from the new system
        new_results_count = self.helpers.get_new_system_results_count()
        self.assertGreater(new_results_count, 0, "Job found text element not found")

        # Compare results
        original_count = self.helpers.search_results_count

        print(f"Original search results count (TC_P_002): {original_count}")
        print(f"New search results count (TC_P_003): {new_results_count}")

        # Check if results match
        self.assertEqual(original_count, new_results_count,
                        f"Results count mismatch: {original_count} vs {new_results_count}")

    def _test_blue_origin_career_button_navigation(self):
        """TC_P_004: Verify navigation behavior of "Blue Origin Career" logo button"""
        # Step 1: Open careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)

        # Handle cookie consent with improved error handling
        try:
            self.helpers.handle_cookie_consent()
        except Exception as e:
            print(f"Cookie consent handling failed, but continuing test: {e}")

        time.sleep(3)  # Increase wait time

        # Step 2: Locate the specific Blue Origin Career logo in header
        header_logo = self.helpers.find_header_logo()
        self.assertIsNotNone(header_logo, "Blue Origin Career header logo not found")

        # Step 3: Click the header logo
        current_url_before = self.driver.current_url
        self.helpers.click_element_safely(header_logo)
        time.sleep(3)

        # Step 4: Verify navigation behavior
        current_url_after = self.driver.current_url

        # The logo should navigate to the home page, not necessarily careers
        expected_patterns = [
            "https://www.blueorigin.com/careers"

        ]

        url_matches = any(pattern in current_url_after for pattern in expected_patterns)
        self.assertTrue(url_matches, f"Expected navigation to Blue Origin home page, got: {current_url_after}")

        # Verify URL changed from the search page
        self.assertNotEqual(current_url_after, current_url_before,
                           f"URL did not change after clicking logo. Still on: {current_url_after}")

        # Ensure we're not on search page anymore
        self.assertNotIn("/search", current_url_after,
                        f"Should not be on search page after clicking logo, got: {current_url_after}")

        # Step 5: Verify we're on a valid Blue Origin page
        content_found = self.helpers.verify_blue_origin_content()
        self.assertTrue(content_found,
                       f"Blue Origin content not found on target page. URL: {current_url_after}, "
                       f"Page title: {self.driver.title}")

    def _test_keyboard_accessibility(self):
        """TC_P_005: Verify keyboard accessibility to job search"""
        # Step 1: Open careers page (no mouse use)
        self.driver.get(BlueOriginUrls.CAREERS_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(2)

        # Step 2: Use Tab key to focus page elements and find "Search Jobs" link/button
        search_job_found = self.helpers.navigate_with_keyboard(max_tabs=20)
        self.assertTrue(search_job_found, "Search Jobs link not found via keyboard navigation")

        # Step 4: Press Enter to activate
        current_url_before = self.driver.current_url
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN).perform()
        time.sleep(3)

        # Step 5: Verify transition to job search page
        current_url_after = self.driver.current_url
        self.assertNotEqual(current_url_after, current_url_before, "URL did not change after pressing Enter")
        self.assertIn("search", current_url_after, f"Expected 'search' in URL, got: {current_url_after}")

        # Step 6: Confirm keyboard usability on new page
        search_input_found = self.helpers.find_search_input_with_keyboard(max_tabs=10)
        self.assertTrue(search_input_found, "Search input field not accessible via keyboard")

        # Test typing in search field
        actions.send_keys("test").perform()
        time.sleep(1)

        focused_element = self.driver.switch_to.active_element
        self.assertIn("test", focused_element.get_attribute("value"),
                     "Keyboard input not working in search field")


# Chrome Tests
class ChromeBlueOriginTests(BaseBlueOriginTest):
    """Test class for Chrome browser"""
    browser_name = 'chrome'

    def test_tc_p_001_navigation_back_to_search(self):
        """TC_P_001: Verify navigation back to original search system via job details page - Chrome"""
        self._test_navigation_back_to_search()

    def test_tc_p_002_keyword_search_functionality(self):
        """TC_P_002: Verify keyword search functionality - Chrome"""
        self._test_keyword_search_functionality()

    def test_tc_p_003_search_results_consistency(self):
        """TC_P_003: Verify consistency of search results across systems - Chrome"""
        self._test_search_results_consistency()

    def test_tc_p_004_blue_origin_career_button_navigation(self):
        """TC_P_004: Verify navigation behavior of "Blue Origin Career" logo button - Chrome"""
        self._test_blue_origin_career_button_navigation()

    def test_tc_p_005_keyboard_accessibility(self):
        """TC_P_005: Verify keyboard accessibility to job search - Chrome"""
        self._test_keyboard_accessibility()


# Firefox Tests
class FirefoxBlueOriginTests(BaseBlueOriginTest):
    """Test class for Firefox browser"""
    browser_name = 'firefox'

    def test_tc_p_001_navigation_back_to_search(self):
        """TC_P_001: Verify navigation back to original search system via job details page - Firefox"""
        self._test_navigation_back_to_search()

    def test_tc_p_002_keyword_search_functionality(self):
        """TC_P_002: Verify keyword search functionality - Firefox"""
        self._test_keyword_search_functionality()

    def test_tc_p_003_search_results_consistency(self):
        """TC_P_003: Verify consistency of search results across systems - Firefox"""
        self._test_search_results_consistency()

    def test_tc_p_004_blue_origin_career_button_navigation(self):
        """TC_P_004: Verify navigation behavior of "Blue Origin Career" logo button - Firefox"""
        self._test_blue_origin_career_button_navigation()

    def test_tc_p_005_keyboard_accessibility(self):
        """TC_P_005: Verify keyboard accessibility to job search - Firefox"""
        self._test_keyboard_accessibility()


# Edge Tests
class EdgeBlueOriginTests(BaseBlueOriginTest):
    """Test class for Edge browser"""
    browser_name = 'edge'

    def test_tc_p_001_navigation_back_to_search(self):
        """TC_P_001: Verify navigation back to original search system via job details page - Edge"""
        self._test_navigation_back_to_search()

    def test_tc_p_002_keyword_search_functionality(self):
        """TC_P_002: Verify keyword search functionality - Edge"""
        self._test_keyword_search_functionality()

    def test_tc_p_003_search_results_consistency(self):
        """TC_P_003: Verify consistency of search results across systems - Edge"""
        self._test_search_results_consistency()

    def test_tc_p_004_blue_origin_career_button_navigation(self):
        """TC_P_004: Verify navigation behavior of "Blue Origin Career" logo button - Edge"""
        self._test_blue_origin_career_button_navigation()

    def test_tc_p_005_keyboard_accessibility(self):
        """TC_P_005: Verify keyboard accessibility to job search - Edge"""
        self._test_keyboard_accessibility()


if __name__ == '__main__':
     # 1. Create a TestLoader instance to find tests
      loader = unittest.TestLoader()
#
#     # 2. Create a TestSuite to hold all the tests you want to run
#     suite = unittest.TestSuite()
#
#     # 3. Add tests from each browser-specific class to the suite.
#     # This makes it easy to run tests for a single browser during development.
#     print("Loading Chrome tests...")
#     suite.addTests(loader.loadTestsFromTestCase(ChromeBlueOriginTests))
#
#     print("Loading Firefox tests...")
#     suite.addTests(loader.loadTestsFromTestCase(FirefoxBlueOriginTests))
#
#     print("Loading Edge tests...")
#     suite.addTests(loader.loadTestsFromTestCase(EdgeBlueOriginTests))
#
#     # 4. Configure the HTMLTestRunner with a descriptive title and description
#     runner = HtmlTestRunner.HTMLTestRunner(
#         output='./HtmlReports',
#         report_name='Positive_Test_Report',  # You can customize the name
#         report_title='Blue Origin Positive Test Report',
#         descriptions='Cross-browser positive test scenario execution.'
#     )
#
#     # 5. Run the suite with the configured runner
#     print("\nStarting positive test run...")
#     runner.run(suite)
#     print("Test run complete. Report generated in ./HtmlReports")

    #allure report runner
# if __name__ == "__main__":
#         unittest.main(AllureReports)
