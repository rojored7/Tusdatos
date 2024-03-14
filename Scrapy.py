from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_process(process_id):
    options = Options()
    # options.headless = True  # Descomentar para modo sin cabeza

    driver = webdriver.Firefox(options=options)
    url = 'https://procesosjudiciales.funcionjudicial.gob.ec/busqueda'
    driver.get(url)
    
    wait = WebDriverWait(driver, 50)
    search_field = wait.until(EC.visibility_of_element_located((By.ID, 'texto')))
    
    max_retries = 3  # Número máximo de reintentos
    expansion_panels = []
    for attempt in range(max_retries):
        try:
            search_field.clear()
            search_field.send_keys(process_id)
            search_field.send_keys(Keys.ENTER)
            # Espera a que se carguen los resultados
            expansion_panels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'mat-expansion-panel')))
            if expansion_panels:
                break  # Si se encuentran paneles, sale del bucle
        except TimeoutException:
            print(f"Intento {attempt + 1} fallido para el proceso {process_id}. Reintentando...")
            if attempt == max_retries - 1:
                print(f"Error: No se pudieron cargar los paneles de expansión para el proceso {process_id}.")
                driver.quit()
                return {process_id: "Error: La página no cargó los resultados."}
    
    results = []
    for panel in expansion_panels:
        header = panel.find_element(By.CSS_SELECTOR, 'mat-expansion-panel-header')
        fecha_notificacion, tipo_notificacion, codigo = "N/A", "N/A", "N/A"
        try:
            header_text = header.text.split('\n')
            if len(header_text) >= 3:
                fecha_notificacion, tipo_notificacion, codigo = header_text[:3]
        except Exception as e:
            print(f"Error extrayendo información de panel para {process_id}: {e}")

        data_dict = {
            "Fecha de notificación": fecha_notificacion,
            "Tipo de notificación": tipo_notificacion,
            "Código": codigo,
            "Contenido detallado": ""  # Inicializa vacío para llenar después
        }

        if not "mat-expanded" in panel.get_attribute("class"):
            driver.execute_script("arguments[0].click();", header)
            time.sleep(2)  # Tiempo de espera para la expansión del panel

        detail_content = panel.find_element(By.CSS_SELECTOR, 'div.mat-expansion-panel-body div.informacion').text
        data_dict["Contenido detallado"] = detail_content
        results.append(data_dict)

    driver.quit()
    return {process_id: results}

# Lista de IDs de proceso 

actor_ofendido_ids = ['0968599020001', '0992339411001']  
demandado_procesado_ids = ['1791251237001', '0968599020001']  

all_results = {}

def execute_scraping_for_category(category, process_ids):
    results_category = {}
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(scrape_process, pid): pid for pid in process_ids}
        for future in as_completed(futures):
            result = future.result()
            for process_id, data in result.items():
                if process_id in results_category:
                    results_category[process_id].extend(data)
                else:
                    results_category[process_id] = data
    return results_category

# Ejecuta el scraping por categoría
results_actor_ofendido = execute_scraping_for_category('Actor/Ofendido', actor_ofendido_ids)
results_demandado_procesado = execute_scraping_for_category('Demandado/Procesado', demandado_procesado_ids)

# Combina los resultados
all_results = {
    'Actor/Ofendido': results_actor_ofendido,
    'Demandado/Procesado': results_demandado_procesado
}

# Escribe los resultados en un archivo JSON
with open('resultados_procesos.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)