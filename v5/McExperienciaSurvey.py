from playwright.sync_api import sync_playwright
import time
import random
from datetime import datetime
import pytz
from config import clientes, clientesusados
from user_agent import get_user_agents
from reviews_handler import get_first_review, move_review_to_used
from clients_handler import get_first_client, move_client_to_used

def main(num_reviews):

    user_agents = get_user_agents()
    if not user_agents:
        print("No se encontraron user agents")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for _ in range(num_reviews):
            user_agent = random.choice(user_agents)
            print(user_agent)
            page = browser.new_page(user_agent=user_agent)
            page.set_default_navigation_timeout(180000)  

            page.goto("https://mcexperienciasurvey.com/")
            time.sleep(5)
            page.click('#NextButton')
            ##############################################
            print("##############################################")
            print("Eligiendo el país\n\n\n\n\n\n")
            time.sleep(2)
            page.click("label[for='Index_CountryPicker.20']")
            page.click('#NextButton')
            time.sleep(2)

            print("##############################################")
            print("Eligiendo restaurante y fecha actual\n\n\n\n\n\n\n")
            hora = input("RECUERDA COLOCAR UNA HORA CONGRUENTE O EL SISTEMA LO RECHAZARA! \n Elige un valor del 10 al 20 \nIntroduce el valor para la hora (Formato 24h): ")
            hora = int(hora)
            if 10 <= hora <= 20: 
                hora = f"{hora:02}"
            else:
                print("Porfavor elige un numero valido")    
            print()
            minutos = input("RECUERDA COLOCAR UN MINUTO CONGRUENTE O EL SISTEMA LO RECHAZARA! \n Elige un valor del 00 al 60 \nIntroduce el valor para los minutos: ")

            if len(minutos) == 2 and minutos.isdigit():
                minutos = int(minutos)
            
                if 0 <= minutos <= 60:
                    minutos = f"{minutos:02}"
                    print(minutos)
                    print(f"Has introducido un valor válido para los minutos: {minutos}")
                else:
                    print("Por favor, elige un número válido entre 00 y 60.")
            else:
                print("Por favor, introduce un número válido en formato de dos dígitos (ej. '01', '02', ..., '60').")
            print()


            country_timezone = pytz.timezone("America/Caracas")
            now = datetime.now(country_timezone)
            current_day = now.day
            current_month = now.month
            current_hour = now.hour
            current_minute = now.minute
            print(f"Today is {current_month}, {current_day}, {current_hour}, {current_minute}")
            input("Pause, enter to skip")

            current_day = str(current_day)
            current_month = str(current_month)
            #css
            #id "#"
            #class "."
            page.fill(".coupon-length-4", "MU2")  
            page.click("#InputDay")  
            page.select_option("#InputDay", current_day)
            page.click("#InputMonth")
            page.select_option("#InputMonth", current_month)
            page.select_option("#InputHour", hora)
            page.click("#InputMinute")
            page.select_option("#InputMinute", minutos)
            page.click("#InputMinute")
            time.sleep(1)        
            page.click("#NextButton")

            print("##############################################")
            
            print("Eligiendo sector de compra\n\n\n\n")
            page.click(".Opt1 label")
            time.sleep(2)        
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo tipo de consumo (llevar/local)\n\n\n\n\n\n\n")

            time.sleep(2)
            page.click(".Opt1 label")
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo si llevo o no un niño\n\n\n\n\n\n\n")
            time.sleep(2)
            page.click(".rbList .Opt2 label")
            page.click("#NextButton")


            print("##############################################")
            print("Eligiendo la experiencia general\n\n\n\n\n\n")
            time.sleep(2)
            page.click(".Opt5")
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo aspectos del servicio\n\n\n\n\n\n\n\n")
            time.sleep(2)
            rates = page.query_selector_all('.Opt5 .radioSimpleInput')

            for rate in rates:
                rate.click()  
                time.sleep(0.5)
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo si el pedido fue tal cual lo pedido\n\n\n\n\n\n\n")
            time.sleep(1)
            page.click(".Opt1")
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo las intenciones de volver al local y recomendación\n\n\n\n\n\n")
            page.click(".Opt5 label")
            time.sleep(1)
            page.click(".Opt10 label")
            time.sleep(1)
            page.click("#NextButton")


            print("##############################################")
            print("Escribiendo reseña\n\n\n\n\n\n\n")
            
            review = get_first_review()
            input("Press enter to next step")
            print(f"The review is:{review}")
            input("Press enter to next step")
            if review:

                print(f"La review es: {review}")
                time.sleep(3)

                # Fill in the review field and move to used
                time.sleep(1)
                page.fill("#S000019", review)
                move_review_to_used(review)
                input("Press enter to next step")
            else:
                print("No more reviews available.")
                input("Press enter to next step")
                browser.close()


            time.sleep(3)
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo si hubo algún problema\n\n\n\n")
            time.sleep(1)
            page.click(".Opt2")
            page.click("#NextButton")

            print("##############################################")
            print("Colocando datos del cliente\n\n\n\n\n\n")

            clientes = get_first_client()
            print(clientes)
            input("Press enter to next step")

            if clientes:
                print(f"el cliente seleccionado fue: {clientes}")
                nombre, correo = clientes.split(" - ")
                time.sleep(1)
                page.fill("#S000036", nombre)
                page.fill("#S000033", correo)
                page.fill("#S000034", correo)
                time.sleep(3)
                page.click("#NextButton")
                move_client_to_used(clientes)
                input("Press enter to next step")
            else:
                print("No more clients available.")
                input("Press enter to next step")
                browser.close()


            print("##############################################")
            print("Thanks page")
            page.click(".Opt2 label")
            page.click("#NextButton")
            print(":PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP\n\n\n\n\n")
            input("Press enter to next step")


            time.sleep(10)
            page.close()

if __name__ == '__main__':
    try:
        num_reviews = int(input("¿Cuántas reseñas quieres enviar? "))
        main(num_reviews) 
    except ValueError:
        print("Por favor, ingresa un número válido.")
        