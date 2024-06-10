import asyncio
from pyppeteer import launch
import os
import paho.mqtt.client as mqtt

#ZMIENNE#

# URL strony, którą chcemy zrzutować
url = 'https://embed.windy.com/embed2.html?lat=50.370&lon=19.808&detailLat=50.456&detailLon=19.764&width=650&height=450&zoom=10&level=surface&overlay=radar&product=radar&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1'

#TESTOWY URL
#url = 'https://embed.windy.com/embed2.html?lat=39.812&lon=-86.774&detailLat=50.456&detailLon=19.764&width=650&height=450&zoom=8&level=surface&overlay=radar&product=radar&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1'

# Nazwa pliku
file_path = 'windy.png'

#####################################################



async def screenshot_embedded_windy(filepath):
    # Sprawdź, czy plik istnieje
    if os.path.exists(filepath):
        os.remove(filepath)  # Usuń plik, jeśli istnieje

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
            '--unsafely-treat-insecure-origin-as-secure="http://windy.com"', 
        
        ], executablePath='/usr/bin/google-chrome')


    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle2', timeout=60000)
    
    # Czekanie na załadowanie mapy NIE POTRZEBNE
    #await asyncio.sleep(5)
    
    # Robienie zrzutu ekranu
    await page.screenshot({'path': filepath})
    
    await browser.close()






# Callback wywoływany, gdy klient otrzyma odpowiedź CONNACK od serwera.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Połączono z wynikiem: {reason_code}")
    # Subskrypcja w funkcji on_connect() oznacza, że jeśli połączenie zostanie
    # utracone i nastąpi ponowne połączenie, subskrypcje zostaną odnowione.
    client.subscribe("pc/image")

# Callback wywoływany, gdy od serwera otrzymamy wiadomość PUBLISH.
def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
    if msg.topic == "pc/image" and msg.payload.decode() == "windy":
        print(f"Tworzenie obrazka")
        # Uruchomienie funkcji asynchronicznej
        asyncio.run(screenshot_embedded_windy(file_path))
        # Sprawdzenie czy utworzono obrazek
        if os.path.exists(file_path):
            print(f"Utworzono obrazek pomyślnie")
        else:
            print(f"Niepowodzenie przy tworzeniu obrazka")

    else:
        print(f"Otrzymano payload: {str(msg.payload)}")

# Utworzenie klienta z użyciem nowego API Callback (dla paho-mqtt v2.0.0)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Ustawienie callbacków
client.on_connect = on_connect
client.on_message = on_message

# Ustawienie nazwy użytkownika i hasła
client.username_pw_set("mqtt", "123456")

# Połączenie z brokerem Mosquitto
broker_address = "localhost"
client.connect(broker_address, 1883, 60)

# Zablokowanie wywołania, które przetwarza ruch sieciowy, rozsyła callbacki i
# obsługuje ponowne łączenie się.
client.loop_forever()
