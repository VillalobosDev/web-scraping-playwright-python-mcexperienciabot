from playwright.sync_api import sync_playwright
import time
import sys
import random


reviews = "reviews.txt"
usedreviews = "reviewsusadas.txt"
clientes = "clientes.txt"
clientesusados = "clientesusados.txt"
user_agents_file = r"C:\Users\Nelson\Desktop\McExperienciSurvey\user_agents.txt"


def get_user_agents():
    try:
        with open(user_agents_file, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: {user_agents_file} file not found.")
        return []

def get_first_review():
    try:
        with open(reviews, "r", encoding='latin-1') as file:  # Changed to 'latin-1' for compatibility
            lines = file.readlines()
            if lines:
                review_info = lines[0].strip()
                with open(reviews, "w", encoding='latin-1') as updated_file:
                    updated_file.writelines(lines[1:])
                return review_info
            else:
                print("No more reviews in the file.")
                return None
    except FileNotFoundError:
        print(f"Error: {reviews} file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while getting review info: {e}")
        return None

def move_review_to_used(review_info):
    try:
        with open(usedreviews, "a", encoding='latin-1') as used_file:  # Added encoding for consistency
            used_file.write(review_info + "\n")
    except FileNotFoundError:
        print(f"Error: {usedreviews} file not found.")
    except Exception as e:
        print(f"An error occurred while moving review info to the used file: {e}")
       
def get_first_client():
    try:
        with open(clientes, "r", encoding='latin-1') as file:  # Changed to 'latin-1' for compatibility
            lines = file.readlines()
            if lines:
                client_info = lines[0].strip()
                with open(clientes, "w", encoding='latin-1') as updated_file:
                    updated_file.writelines(lines[1:])
                return client_info
            else:
                print("No more clients in the file.")
                return None
    except FileNotFoundError:
        print(f"Error: {clientes} file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while getting client info: {e}")
        return None

def move_client_to_used(client_info):
    try:
        with open(clientesusados, "a", encoding='latin-1') as used_file:  # Added encoding for consistency
            used_file.write(client_info + "\n")
    except FileNotFoundError:
        print(f"Error: {clientesusados} file not found.")
    except Exception as e:
        print(f"An error occurred while moving client info to the used file: {e}")

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

            page.goto("https://mcexperienciasurvey.com/Index.aspx?c=053609")
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
                str(hora)
            else:
                print("Porfavor elige un numero valido")    
            print()
            minutos = input("RECUERDA COLOCAR UN MINUTO CONGRUENTE O EL SISTEMA LO RECHAZARA! \n Elige un valor del 00 al 60 \nIntroduce el valor para los minutos: ")

            if len(minutos) == 2 and minutos.isdigit():
                minutos = int(minutos)
            
                if 0 <= minutos <= 60:
                    minutos = f"{minutos:02}"
                    print(f"Has introducido un valor válido para los minutos: {minutos}")
                else:
                    print("Por favor, elige un número válido entre 00 y 60.")
            else:
                print("Por favor, introduce un número válido en formato de dos dígitos (ej. '01', '02', ..., '60').")
            print()
            

            page.fill(".coupon-length-4", "MU2")  
            page.click("button.ui-datepicker-trigger")  
            page.click("td.ui-datepicker-today")    
            page.click("#InputHour")
            page.select_option("#InputHour", hora)
            page.click("#InputMinute")
            page.select_option("#InputMinute", minutos)
            page.click("#InputMinute")
            time.sleep(1)        
            page.click("#NextButton")

            print("##############################################")
            print("Eligiendo sector de compra\n\n\n\n")
            sectors = ["Mostrador", "Centro de postres", "Automac"]

            print("Selecciona por donde fué tu compra:")
            for i, sector in enumerate(sectors, 1):
                print(f"{i}. {sector}\n\n")

            choice = input("Introduce el numero que corresponde a tu selección: ")

            try:
                choice = int(choice)
                if 1 <= choice <= len(sectors):
                    selected_sector = sectors[choice - 1]
                    print(f"Selecionaste: {selected_sector}")
                    try:
                        if choice == 1:
                            page.click(".Opt1 label")
                        elif choice == 2:
                            page.click(".Opt3 label")
                        elif choice == 3:
                            page.click(".Opt5 label")

                    except ValueError as error:
                        print(f"Error:{error}.")
                else:
                    print("Selección invalida.")
            except ValueError as error:
                print(f"Error:{error}. Selección invalida, usa un numero.")
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
            print("##############################################")
            print("Escribiendo reseña\n\n\n\n\n\n\n")
            review = get_first_review()
            print(review)
            if review:
                print(f"La review es: {review}")
                time.sleep(3)

                # Fill in the review field and move to used
                time.sleep(1)
                page.fill("#S000019", review)
                move_review_to_used(review)
            else:
                print("No more reviews available.")
                browser.close()
                sys.exit()  # Exit the program if there are no reviews left


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
            else:
                print("No more clients available.")
                browser.close()
                sys.exit()


            print("##############################################")
            print("Thanks page")
            page.click(".Opt2 label")
            page.click("#NextButton")
            print(":PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP\n\n\n\n\n")


            time.sleep(10)
            page.close()

if __name__ == '__main__':
    try:
        num_reviews = int(input("¿Cuántas reseñas quieres enviar? "))
        main(num_reviews) 
    except ValueError:
        print("Por favor, ingresa un número válido.")
        