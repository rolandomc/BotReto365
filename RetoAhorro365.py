import json
import random
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import asyncio

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
async def generar_numero(update: Update, context: CallbackContext):
    datos = cargar_datos()
    if len(datos["numeros"]) >= 365:
        await update.message.reply_text("Ya has generado todos los números posibles.")
        return
    numero = random.randint(1, 365)
    while numero in datos["numeros"]:
        numero = random.randint(1, 365)
    datos["numeros"].append(numero)
    datos["acumulado"] += numero
    guardar_datos(datos)
    await update.message.reply_text(f"El número generado es: {numero}. Acumulado: ${datos['acumulado']}.")

# Comando: agregar número manualmente
async def agregar_numero(update: Update, context: CallbackContext):
    datos = cargar_datos()
    try:
        numero = int(context.args[0])
        if numero < 1 or numero > 365:
            await update.message.reply_text("Por favor, ingresa un número entre 1 y 365.")
            return
        if numero in datos["numeros"]:
            await update.message.reply_text("Este número ya fue agregado.")
            return
        datos["numeros"].append(numero)
        datos["acumulado"] += numero
        guardar_datos(datos)
        await update.message.reply_text(f"Número agregado: {numero}. Acumulado: ${datos['acumulado']}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, ingresa un número válido.")

# Comando: ver acumulado
async def ver_acumulado(update: Update, context: CallbackContext):
    datos = cargar_datos()
    await update.message.reply_text(f"El acumulado actual es: ${datos['acumulado']}.")

# Configurar el bot
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Añadir comandos
    application.add_handler(CommandHandler("generar", generar_numero))
    application.add_handler(CommandHandler("agregar", agregar_numero))
    application.add_handler(CommandHandler("acumulado", ver_acumulado))

    # Iniciar el bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
