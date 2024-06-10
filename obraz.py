import asyncio
from pyppeteer import launch
import os
import paho.mqtt.client as mqtt
import re
from datetime import datetime
import time

# Zmienne konfiguracyjne
MQTT_USER = "user" #Nazwa użytkownika serwera mqtt
MQTT_PASSWORD = "pass" #Hasło serwera mqtt
MQTT_BROKER = "192.168.1.45" #Adres serwera mqtt
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Funkcja do robienia zrzutu ekranu
async def screenshot_embedded_windy(url, filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        
        browser = await launch(headless=True, args=[
            '--disable-infobars',
            '--disable-extensions',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--allow-running-insecure-content',
            '--enable-features=OverlayScrollbar',
            '--ignore-certificate-errors',
            '--ignore-certificate-errors-spki-list',
            '--use-fake-ui-for-media-stream',
            '--use-fake-device-for-media-stream',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-popup-blocking',
            '--enable-precise-location',
        ], executablePath='/usr/bin/google-chrome')

        page = await browser.newPage()
        await page.goto(url, waitUntil='networkidle2', timeout=60000)
        await page.screenshot({'path': filepath})
        await browser.close()
        log(f"Zrzut ekranu zapisany pomyślnie: {filepath}")
    except Exception as e:
        log(f"Błąd podczas robienia zrzutu ekranu: {e}")

# Funkcja logująca z dodaniem daty i godziny
def log(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {message}")

# Callback wywoływany, gdy klient otrzyma odpowiedź CONNACK od serwera
def on_connect(client, userdata, flags, reason_code, properties):
    log(f"Połączono z wynikiem: {reason_code}")
    client.subscribe("pc/image/#")

# Callback wywoływany, gdy od serwera otrzymamy wiadomość PUBLISH
def on_message(client, userdata, msg):
    log(f"Otrzymano wiadomość na temat: {msg.topic} z payloadem: {msg.payload.decode()}")
    
    topic_parts = msg.topic.split('/')
    if len(topic_parts) == 3 and topic_parts[0] == "pc" and topic_parts[1] == "image":
        filename_variable = topic_parts[2]
        url = msg.payload.decode()

        # Dodaj rozszerzenie .png do nazwy pliku
        file_path = f"{filename_variable}.png"

        # Sprawdzenie poprawności nazwy pliku i URL
        if re.match(r'^[\w-]+\.png$', file_path) and url.startswith("http"):
            log(f"Tworzenie obrazka {file_path} z URL: {url}")
            # Użycie asyncio.run() aby uruchomić asynchroniczną funkcję
            asyncio.run(screenshot_embedded_windy(url, file_path))
        else:
            log("Błędny format nazwy pliku lub URL")
    else:
        log("Niewłaściwy temat")

# Utworzenie instancji klienta z użyciem nowego API Callback
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Ustawienie callbacków
client.on_connect = on_connect
client.on_message = on_message

# Ustawienie nazwy użytkownika i hasła
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Funkcja do ponawiania połączeń z brokerem MQTT
def connect_with_retries(client, broker_address, port, keepalive):
    while True:
        try:
            client.connect(broker_address, port, keepalive)
            return
        except Exception as e:
            log(f"Nie udało się połączyć z brokerem MQTT: {e}")
            log("Ponawianie połączenia za 10 sekund...")
            time.sleep(10)

# Próba połączenia z brokerem bez limitu prób
connect_with_retries(client, MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

# Zablokowanie wywołania przetwarzającego ruch sieciowy, rozsyłającego callbacki i obsługującego ponowne łączenie
client.loop_forever()
