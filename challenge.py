from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import os

class challengeSite:
    def __init__(self):
        self.driver = None


    def initialize_driver(self, site):
        self.options = Options()
        self.arguments= ["window-size=1200,1080"]

        self.options.add_argument("--headless") 
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        for i in self.arguments:
            self.options.add_argument(i)

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(site)


    # Challenge 1
    def challenge1(self, email, passw):

        try:
            self.email_xpath = "//input[@id='email' or @name='email' or @placeholder='seu@email.com']"
            self.passw_xpath = "//input[@id='password' or @name='password' or @placeholder='********']"
            self.login_btn_xpath = "//button[normalize-space()='Fazer Login']"

            email_field = self.driver.find_element(By.XPATH, self.email_xpath)
            email_field.send_keys(email)

            passw_field = self.driver.find_element(By.XPATH, self.passw_xpath)
            passw_field.send_keys(passw)

            login_btn = self.driver.find_element(By.XPATH, self.login_btn_xpath)
            login_btn.click()

            confirm_pop_up_element = '//button[@class="modal-btn" and normalize-space()="OK, Entendi"]'

            btn_confirm_pop_up = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, confirm_pop_up_element))
            )
            btn_confirm_pop_up.click()


        except Exception as e:
            print(f"Error found:\n\n {e}")


    # Challenge 2
    def challenge2(self, csv_path):
        data = pd.read_csv(csv_path)

        try:
            full_name_input= self.driver.find_element(By.XPATH, '//*[@id="nome"]')
            cpf_input= self.driver.find_element(By.XPATH, '//*[@id="cpf"]')
            email_input= self.driver.find_element(By.XPATH, '//*[@id="emailCorp"]')
            price_input= self.driver.find_element(By.XPATH, '//*[@id="valor"]')
            generate_data_btn= self.driver.find_element(By.XPATH, '/html/body/div[3]/button')

            for _, row in data.iterrows():
                full_name= row["full_name"]
                cpf= row["cpf"]
                email= row["email"]
                price= row["value_price"]

                full_name_input.clear()
                full_name_input.send_keys(full_name)

                cpf_input.clear()
                cpf_input.send_keys(cpf)

                email_input.clear()
                email_input.send_keys(email)

                price_input.clear()
                price_input.send_keys(price)

                generate_data_btn.click()

                confirm_btn= self.driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
                confirm_btn.click()
        except Exception as e:
            raise("Error:\n {e}")


    # Challenge 3
    def challenge3(self, movie_type:str):
        """
        Select some one of this options:
        Acao
        Comedia
        Drama
        Terror
        Ficção Científica
        Documentario
        """
        movie_type = movie_type.lower()

        if movie_type in ("ação", "acão", "açao"):
            movie_type = "acao"
        elif movie_type in ("comédia"):
            movie_type = "comedia"
        elif movie_type in ("ficção","ficcão","ficçao"):
            movie_type = "ficcao"
        elif movie_type in ("documentário"):
            movie_type = "documentario"
        
        dropdown = Select(self.driver.find_element(By.ID, "filmeCategoria"))
        dropdown.select_by_value(movie_type)


    # Challenge 4
    def challenge4(self, file_path:str):
        """
        Past the full filepath without quotes
        """
        upload_btn = self.driver.find_element(By.ID, "fileUpload")
        upload_btn.send_keys(file_path)

        send_btn = self.driver.find_element(By.XPATH, "//button[normalize-space()='Enviar Arquivo']")
        send_btn.click()

        ok_btn = self.driver.find_element(By.XPATH,"//button[contains(normalize-space(), 'OK')]")
        ok_btn.click()


    # Challenge 5 -> Webscraping
    def webscraping(self):
        website_url= "https://sampaiodev-rpa-desafios.vercel.app/loja.html"
        self.initialize_driver(site= website_url)

        # Wait page loads
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(normalize-space(), 'Sampaio Store')]")))

        itens= self.driver.find_elements(By.CLASS_NAME, "product-card")
        products = []

        for i in itens:
            prod_name = i.find_element(By.CLASS_NAME, "title").text
            prod_description = i.find_element(By.CLASS_NAME, "desc").text
            prod_price= i.find_element(By.CLASS_NAME, "price").text

            # Format values
            prod_price = prod_price.replace("R$ ", "").replace(",",".")


            products.append({
                'Product': prod_name,
                'Description': prod_description,
                'Price': prod_price
            })



        # Create TXT file
        with open(r"data/products_catalog.txt", "w") as file: # "w" to create the file if it not exist
            file.write(str(products))



    
