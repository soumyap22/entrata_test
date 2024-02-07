import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture(scope="module")
def browser():
    # Initialize Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')  # Start Chrome maximized

    # Set the path to the Chrome WebDriver binary using ChromeDriverManager
    webdriver_service = Service(ChromeDriverManager().install())

    # Initialize Chrome WebDriver with the service and options
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    yield driver
    
    driver.quit()  # Teardown - close the browser

# Test for the homepage of entrata.com
def test_homepage(browser):
    # Open entrata.com
    browser.get("https://www.entrata.com/")

    # Assert Data
    assert "Entrata" in browser.title, 'Title value is not Valid'

# Test for accepting all cookies to check if the cookie is being set
def test_accept_all_cookies(browser):
    # Click on Accept Cookie Button
    accept_cookies = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "rcc-confirm-button")))
    accept_cookies.click()

    WebDriverWait(browser, 1).until(lambda driver: driver.get_cookie("CookieConsent") is not None )
    cookie = browser.get_cookie("CookieConsent")

    # Assert Cookie Data
    assert cookie is not None, 'Cookie vaue is NULL'
    assert cookie["value"] == 'true', 'Cookie vaue is not Valid'

# Test for scheduling a demo on the resident portal
# As we cannot submit valid data, so added some valid data and some invalid fields and asserting if the proper error is coming.
def test_resident_portal_schedule_demo(browser):
    # Find the navigation bar item to hover over by its text content
    nav_bar_item = browser.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[1]/div/div/div[2]/div[1]')
    # Find the URL element to click by its text content
    url_element = browser.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[1]/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/a[3]')

    actions = ActionChains(browser)

    # Hover over the navigation bar item
    actions.move_to_element(nav_bar_item).perform()
    
    # Click on the URL element
    url_element.click()

    schedule_demo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[3]/a')))
    schedule_demo.click()

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mktoForm_1132"]/div[11]/span/button')))
    # Find Form Fields
    contact_form_first_name = browser.find_element(By.ID, "FirstName")
    contact_form_last_name = browser.find_element(By.ID, "LastName")
    contact_form_email = browser.find_element(By.ID, "Email")
    contact_form_company = browser.find_element(By.ID, "Company")
    contact_form_phone = browser.find_element(By.ID, "Phone")
    contact_form_unit = browser.find_element(By.ID, "Unit_Count__c")
    contact_form_job = browser.find_element(By.ID, "Title")

    # Fill in the contact form fields
    contact_form_first_name.send_keys("Soumya Pandey")
    contact_form_last_name.send_keys("This is a test message.")
    contact_form_email.send_keys("pandeysoumya22@gmail.com")
    
    # Submit the contact form
    submit_button = browser.find_element(By.XPATH, '//*[@id="mktoForm_1132"]/div[11]/span/button')
    submit_button.click()

    # Assert that the input element has the expected class asserting invalid fields
    assert "mktoInvalid" in contact_form_company.get_attribute("class"), "Error Class Not Found"
    assert "mktoInvalid" in contact_form_phone.get_attribute("class"), "Error Class Not Found"
    assert "mktoInvalid" in contact_form_unit.get_attribute("class"), "Error Class Not Found"
    assert "mktoInvalid" in contact_form_job.get_attribute("class"), "Error Class Not Found"

# Test for property manager login
# As we will not be making useless requests to the server by adding incorrect data, adding a username and asserting the error message
def test_property_manager_login(browser):
    # Go back to previous page
    browser.back()
    
    # Find the login button
    login_in_button = browser.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[1]/div/div/div[3]/a[2]') 
    login_in_button.click()

    property_manager_login = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div/div/div/div[1]/div/div[3]/a[1]')))
    property_manager_login.click()
    
    property_manager_sign_in = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fsm_request_demo"]/ul/li[3]/button')))

    # Enter UserName
    contact_form_first_name = browser.find_element(By.XPATH, '//*[@id="entrata-username"]')
    contact_form_first_name.send_keys("pandeysoumya22")

    property_manager_sign_in.click()

    error_message = browser.find_element(By.ID, "entrata-login-error")
    error_text = error_message.text

    expected_text = "Please enter username and password"

    # Assert error text is not empty and is giving valid error message
    assert error_text != "", "Text Value is Empty"
    assert error_text == expected_text, f"Actual text value '{error_text}' does not match expected value '{expected_text}'"
