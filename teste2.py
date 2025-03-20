from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?hdnLocalidade=9859&hdnModalidade=Selecione&hdnValorSimulador=&hdnAceitaFGTS=&hdnAceitaFinanciamento=")

time.sleep(2)

select_State = driver.find_element(By.ID, "cmb_estado")

select1 = Select(select_State)

select1.select_by_visible_text("SP")

time.sleep(2)

btn_next = driver.find_element(By.ID, "btn_next0")
btn_next.click()

time.sleep(2)

select_TipoImovel = driver.find_element(By.ID, "cmb_tp_imovel")
select2 = Select(select_TipoImovel)
select2.select_by_visible_text("Apartamento")

time.sleep(3)

select_valorImovel = driver.find_element(By.ID, "cmb_faixa_vlr")
select3 = Select(select_valorImovel)
select3.select_by_index(3)

time.sleep(3)


btn_next2 = driver.find_element(By.ID, "btn_next1")
btn_next2.click()

time.sleep(15)


driver.quit()