import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from database import Product, get_db


# Load environment variables
load_dotenv()

with_bushing_xpath = '//*[@id="type-container"]/div/div[1]/div[1]/div[2]/div/div/div/div/a[1]'
full_ball_xpath = '//*[@id="type-container"]/div/div[1]/div[1]/div[2]/div/div/div/div/a[2]'
cabin_xpath = '//*[@id="type-container"]/div/div[1]/div[1]/div[2]/div/div/div/div/a[3]'

with_bushing = "With Bushing"
full_ball = "Full Ball"
cabin = "Cabin"

TORQUE_ROD_CATEGORY_XPATH = cabin_xpath
TORQUE_ROD_CATEGORY = cabin


UPLOAD_TO_DB = True


def get_driver():
   # Set up Chrome options
   chrome_options = Options()
   chrome_options.add_argument('--headless')  # Run in headless mode
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')
   chrome_options.add_argument('--window-size=1920,1080')  # Set window size to 1920x1080
   chrome_options.add_argument('--start-maximized')  # Start maximized


   # For Apple Silicon (M-series chips), we need to specify the binary location
   if platform.machine() == 'arm64':
       chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  
   # Initialize the Chrome WebDriver
   service = Service()
   driver = webdriver.Chrome(service=service, options=chrome_options)
  
   return driver


def login(driver):
   # Get credentials from environment variables
   username = os.getenv('AUTOMANN_USERNAME')
   password = os.getenv('AUTOMANN_PASSWORD')
  
   if not username or not password:
       raise ValueError('Please set AUTOMANN_USERNAME and AUTOMANN_PASSWORD in .env file')
  
   try:
       # Set up wait for elements
       wait = WebDriverWait(driver, 10)


       # Wait for and click initial login button
       login_button = wait.until(
           EC.element_to_be_clickable((By.XPATH, '//*[@id="navigation"]/div/a[2]'))
       )
       time.sleep(1)  # Small delay before clicking
       login_button.click()
      
       # Wait for and fill username field
       username_field = wait.until(
           EC.element_to_be_clickable((By.NAME, 'login[username]'))
       )
       time.sleep(1)  # Small delay before typing
       username_field.clear()  # Clear any existing text
       username_field.send_keys(username)
      
       # Wait for and fill password field
       password_field = wait.until(
           EC.element_to_be_clickable((By.NAME, 'login[password]'))
       )
       time.sleep(1)  # Small delay before typing
       password_field.clear()  # Clear any existing text
       password_field.send_keys(password)
      
       # Wait for and click submit button
       login_submit_button = wait.until(
           EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.w-full.mb-2.lg\:mb-0.lg\:w-fit'))
       )
       time.sleep(1)  # Small delay before clicking
       login_submit_button.click()
      
       # Wait for login to complete by checking for user's name in h3 tag
       wait.until(
           EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Hey, Ryan Bugai!')
       )
      
       print('Successfully logged in')
       return True
      
   except Exception as e:
       print(f'Login failed: {e}')
       # Take a screenshot when error occurs
       try:
           driver.save_screenshot('error_screenshot.png')
           print('Screenshot saved as error_screenshot.png')
       except:
           print('Could not save screenshot')
       return False


def nav_to_products(driver):
   wait = WebDriverWait(driver, 3)


   wizard = wait.until(
       EC.element_to_be_clickable((By.XPATH, '//*[@id="navigation"]/ul[2]/li[5]'))
   )
   time.sleep(1)
   wizard.click()


   torque_rods = wait.until(
       EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Truck Torque Rods")]'))
   )
   time.sleep(1)
   torque_rods.click()


   wait.until(
       EC.text_to_be_present_in_element((By.CSS_SELECTOR, '[data-ui-id=page-title-wrapper]'), 'Truck Torque Rods')
   )
   print('Successfully navigated to torque rods')
   return


def iterate_products(driver):
   wait = WebDriverWait(driver, 3)

   print('Navigating to category')
   with_bushing = wait.until(
       EC.element_to_be_clickable((By.XPATH, TORQUE_ROD_CATEGORY_XPATH))
   )
   time.sleep(1)
   with_bushing.click()
   print('Successfully navigated to category')

   # Wait for products to load
   time.sleep(2)
  
   # Find all product containers
   products = driver.find_elements(By.CSS_SELECTOR, f'[data-type1="{TORQUE_ROD_CATEGORY}"]')
   print(f'Found {len(products)} products for {TORQUE_ROD_CATEGORY}')
  
   # Loop through each product
   for product in products:
       product.click()
       time.sleep(1)
       print('Scraping new product')
       scrape_products(driver)

   print('Finished scraping products')
   return



def scrape_products(driver):
    try:

        db = next(get_db())

        wait = WebDriverWait(driver, 3)
        
        # Wait for the container element
        container1 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wizard-wrap"]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]'))
        )


        container2 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wizard-wrap"]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[2]'))
        )
        # Find all rows with row-index attribute
        rows1 = container1.find_elements(By.CSS_SELECTOR, '[row-index]')
        rows2 = container2.find_elements(By.CSS_SELECTOR, '[row-index]')


        rows = zip(rows1, rows2)
        
        for row1, row2 in rows:
            new_product = Product()
            try:     
                # ROW 1 SCRAPE    
                sku = row1.find_element(By.TAG_NAME, 'a')
                new_product.sku = sku.text
                
                type1_container = row1.find_element(By.CSS_SELECTOR, '[col-id="type1"]')
                # type1 = type1_container.find_element(By.CLASS_NAME, 'w-fit')
                new_product.type1 = type1_container.text


                type2_container = row1.find_element(By.CSS_SELECTOR, '[col-id="type2"]')
                # type2 = type2_container.find_element(By.CLASS_NAME, 'w-fit')
                new_product.type2 = type2_container.text
                
                # ROW 2 SCRAPE
                c_to_c_container = row2.find_element(By.CSS_SELECTOR, '[col-id="c_to_c"]')
                new_product.c_to_c = c_to_c_container.text
                
                side_a_container = row2.find_element(By.CSS_SELECTOR, '[col-id="side_a"]')
                new_product.side_a = side_a_container.text
                
                side_b_container = row2.find_element(By.CSS_SELECTOR, '[col-id="side_b"]')
                new_product.side_b = side_b_container.text


                side_a_bushing_container = row2.find_element(By.CSS_SELECTOR, '[col-id="side_a_bushing"]')
                new_product.side_a_bushing = side_a_bushing_container.text
                
                side_b_bushing_container = row2.find_element(By.CSS_SELECTOR, '[col-id="side_b_bushing"]')
                new_product.side_b_bushing = side_b_bushing_container.text


                side_a_angle_container = row2.find_element(By.CSS_SELECTOR, '[col-id="side_a_angle"]')
                new_product.side_a_angle = side_a_angle_container.text
                
                side_b_angle_container = row2.find_element(By.CSS_SELECTOR, '[col-id="side_b_angle"]')
                new_product.side_b_angle = side_b_angle_container.text
                
                shaft_dia_container = row2.find_element(By.CSS_SELECTOR, '[col-id="shaft_dia"]')
                new_product.shaft_dia = shaft_dia_container.text


                print(f'New product: {new_product.sku} - {new_product.type2} - {new_product.side_b_bushing}')
                if UPLOAD_TO_DB:
                    db.add(new_product)
                    
            except Exception as e:
                print(f'Error processing row: {e}')
                return

        if UPLOAD_TO_DB:
            db.commit()  # Commit the transaction

    except Exception as e:
        db.rollback()  # Rollback on error
        print(f'Error processing products: {e}')


if __name__ == '__main__':
   driver = get_driver()
   try:
       # Navigate to login page
       driver.get('https://www.automann.com')
       print('Successfully connected to Automann')
      
       # Attempt login
       if login(driver):
           # Wait a bit to see the dashboard (since we're not in headless mode)
           time.sleep(5)
           nav_to_products(driver)
           iterate_products(driver)


      
   except Exception as e:
       print(f'Error: {e}')
   finally:
       driver.quit()

