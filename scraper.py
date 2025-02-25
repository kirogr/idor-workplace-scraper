from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import time
from random import randint
import threading
import logging
from queue import Queue

logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CHROMEDRIVER_PATH = r'chromedriver.exe'

cookies = {"session_id": "xxxxxxxxxxxxxxxxxxx"}

max_tabs = 5
semaphore = threading.Semaphore(max_tabs)

task_queue = Queue()

def request_and_save(driver, place_id):
    with semaphore:
        try:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])

            URL = f"https://vulnerable-website.com/EmployeeList.aspx?place_id={place_id}"
            driver.get(URL)
            driver.add_cookie({"name": "session_id", "value": cookies["session_id"]})

            time.sleep(randint(1, 2))

            html_content = driver.page_source

            directory = f'places/{place_id}/'
            filename = f'{directory}/index.html'

            os.makedirs(directory, exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html_content)

            logging.info(f"Saved HTML for place {place_id} to {filename}")
            print(f"Saved HTML for place {place_id} to {filename}")

        except Exception as e:
            logging.error(f"Error requesting Place {place_id}: {e}")
            print(f"Error requesting Place {place_id} : {e}")

        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


def worker(driver):
    while not task_queue.empty():
        place_id = task_queue.get()
        request_and_save(driver, place_id)
        task_queue.task_done()


def create_and_start_threads(driver):
    for place_id in range(1, 3000):
        task_queue.put((place_id))

    threads = []
    for _ in range(max_tabs):
        thread = threading.Thread(target=worker, args=(driver,))
        thread.start()
        threads.append(thread)

    task_queue.join()
    for thread in threads:
        thread.join()

def main():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        create_and_start_threads(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
