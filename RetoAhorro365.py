import json
import random
import os
from datetime import datetime
from telegram import Updater
from telegram.ext import Updater, CommandHandler, CallbackContext

# Cargar token del bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Archivo para guardar los datos
DATA_FILE = "ahorro_data.json"

# Inicializar datos
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump({"acumulado": 0, "numeros": []}, file)

# Cargar datos desde el archivo
def cargar_datos():
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Guardar datos en el archivo
def guardar_datos(datos):
    with open(DATA_FILE, "w") as file:
        json.dump(datos, file)

# Comando: generar número aleatorio
def generar_numero(update: Update, context: CallbackContext):
    datos = cargar_datos()
    if len(datos["numeros"]) >= 365:
        update.message.reply_text("Ya has generado todos los números posibles.")
        return
    numero = random.randint(1, 365)
    while numero in datos["numeros"]:
        numero = random.randint(1, 365)
    datos["numeros"].append(numero)
    datos["acumulado"] += numero
    guardar_datos(datos)
    update.message.reply_text(f"El número generado es: {numero}. Acumulado: ${datos['acumulado']}.")

# Comando: agregar número manualmente
def agregar_numero(update: Update, context: CallbackContext):
    datos = cargar_datos()
    try:
        numero = int(context.args[0])
        if numero < 1 or numero > 365:
            update.message.reply_text("Por favor, ingresa un número entre 1 y 365.")
            return
        if numero in datos["numeros"]:
            update.message.reply_text("Este número ya fue agregado.")
            return
        datos["numeros"].append(numero)
        datos["acumulado"] += numero
        guardar_datos(datos)
        update.message.reply_text(f"Número agregado: {numero}. Acumulado: ${datos['acumulado']}.")
    except (IndexError, ValueError):
        update.message.reply_text("Por favor, ingresa un número válido.")

# Comando: ver acumulado
def ver_acumulado(update: Update, context: CallbackContext):
    datos = cargar_datos()
    update.message.reply_text(f"El acumulado actual es: ${datos['acumulado']}.")

# Configurar el bot
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Añadir comandos
    dp.add_handler(CommandHandler("generar", generar_numero))
    dp.add_handler(CommandHandler("agregar", agregar_numero))
    dp.add_handler(CommandHandler("acumulado", ver_acumulado))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
