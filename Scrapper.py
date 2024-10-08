from selenium import webdriver
from selenium.webdriver.common.by import By #Permet d'accéder aux différents élements de la page web
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

FIRE_DEPARTURE_URL = "https://bdiff.agriculture.gouv.fr/incendies"

class Scrapper():
  def __init__(self, driver="firefox"):
    if driver == "firefox":
      self.driver = webdriver.Firefox()
    else:
      self.driver = webdriver.Chrome()
  
  def get_fire_departure_in_france_data(self, start_date, end_date):
    d = self.driver
    d.maximize_window()
    d.get(FIRE_DEPARTURE_URL)
    assert "BDIFF : Recherche et consultation des incendies de forêt" in d.title
    time.sleep(2)
    
    # Set start and end date into date input
    start_date_input = d.find_element(By.ID, 'if_dateAlerteDeb_date')
    start_date_input.clear()
    start_date_input.send_keys("value", start_date)
    assert start_date == start_date_input.get_attribute('value')
    time.sleep(2)

    end_date_input = d.find_element(By.ID, 'if_dateAlerteFin_date')
    end_date_input.clear()
    end_date_input.send_keys("value", end_date)
    assert end_date == end_date_input.get_attribute('value')
    time.sleep(2)

    # Click on filter button
    filter_button = d.find_element(By.ID, "if_submit")
    d.execute_script("arguments[0].scrollIntoView(true);", filter_button)
    time.sleep(2)
    filter_button.click()
    
    # Retrieve all data from table of each pages
    all_data = []
    while True:
      df_page = self.__scrape_table(d)
      all_data.append(df_page)

      # Check if <a rel="next"> is disabled
      try:
        # if disabled, stop scrapping
        next_button_li = d.find_element(By.XPATH, "//li[@class='page-item disabled']/a[@rel='next']")
        print("bouton next désactivé")
        break
      except:
        print("bouton next activé")
        pass
      
      # Click on next link
      try:
        next_button = d.find_element(By.CSS_SELECTOR, 'a.page-link[rel="next"]')
        d.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)
        next_button.click()
        print("page suivante")
        time.sleep(2)
      except Exception as e:
        print("j'ai pas réussi à appuyer sur next button")
        break
    
    d.close()
    print("Scrapping done successfully...")
      
    return pd.concat(all_data, ignore_index=True)
  
  def __scrape_table(self, driver):
    table = driver.find_element(By.ID, "incendies-table")
    headers = [header.text for header in table.find_elements(By.XPATH, ".//thead/tr/th")]

    rows = table.find_elements(By.XPATH, ".//tbody/tr")

    table_data = []

    for row in rows:
      cols = [col.text for col in row.find_elements(By.TAG_NAME, "td")]
      table_data.append(cols)
    
    return pd.DataFrame(table_data, columns=headers)