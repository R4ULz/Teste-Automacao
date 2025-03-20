from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


# Inicia o navegador (Chrome)
driver = webdriver.Chrome()  

# Acessa um site
driver.get("https://www.magazineluiza.com.br/")

time.sleep(3)

search_box = driver.find_element(By.ID, "input-search")
search_box.send_keys("caixa de som bluetooth")
search_box.send_keys(Keys.RETURN)
time.sleep(5)

first_item = driver.find_element(By.CLASS_NAME, 'fdofhQ')
first_item.click()

time.sleep(2)

item_url = driver.current_url

print("link do item:", item_url)


#wait = WebDriverWait(driver, 20)

# driver.quit()
