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