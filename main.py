from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

def count_pdfs(download_path):
    """Zählt .pdf-Dateien im Ordner"""
    return len([f for f in os.listdir(download_path) if f.lower().endswith(".pdf")])

def run_program():
    # Setze den Pfad zum Download-Ordner (Standardpfad)
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")

    # Aktuellen PDF-Zähler ermitteln
    pdf_count_before = count_pdfs(download_path)

    # Browser-Optionen (optional: Download-Ordner festlegen)
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Optional: Download-Ordner explizit setzen
    # options.add_experimental_option("prefs", {"download.default_directory": download_path})

    driver = webdriver.Chrome(service=Service(), options=options)

    print("open webbrowser")
    driver.get("https://online2pdf.com/de/word-zu-pdf-konvertieren")

    print("upload file")
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    file_input.send_keys("C:/Users/grego/Desktop/Testdatei.docx")

    print("click convert button")
    convert_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Konvertieren')]"))
    )
    driver.execute_script("arguments[0].click();", convert_button)

    print("warte auf fertige PDF im Download-Ordner ...")
    timeout = 60  # maximale Wartezeit in Sekunden
    start_time = time.time()

    while time.time() - start_time < timeout:
        pdf_count_now = count_pdfs(download_path)
        if pdf_count_now > pdf_count_before:
            print("PDF erfolgreich heruntergeladen.")
            break
        time.sleep(1)  # kurz warten, dann erneut prüfen
    else:
        print("❌ Timeout: PDF wurde nicht rechtzeitig gefunden.")

    driver.quit()

if __name__ == "__main__":
    run_program()
