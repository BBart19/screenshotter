# Screenshotter

## Description
The "Screenshotter" program is a tool for automatically taking screenshots of web pages. It operates within a Docker environment, ensuring isolation and easy scalability. The program retrieves the URL of the web page from an MQTT payload, generates a screenshot, and then makes the resulting PNG file available through a local HTTP server in the Docker container.

## Features
1. **Receiving URLs via MQTT**: The program listens to the MQTT topic `pc/image/(file name)` with payload containing the URL of the web page to be screenshot.
2. **Generating the file name**: The PNG file name is generated based on the MQTT topic.
3. **Taking the screenshot**: A Python script uses a browser automation library (e.g., Selenium) to capture the screenshot of the web page.
4. **Serving the screenshot**: The screenshots are saved in a directory served by an HTTP server running in the Docker container, making them accessible via the container's local IP address.

## Usage with Home Assistant
The "Screenshotter" program can be used with Home Assistant to send messages with the screenshot image. By configuring an MQTT integration in Home Assistant, you can automate the process of taking screenshots based on various triggers and conditions.

# Screenshotter

## Opis
Program "Screenshotter" jest narzędziem do automatycznego wykonywania zrzutów ekranu stron internetowych. Działa w środowisku Docker, co zapewnia izolację i łatwą skalowalność. Program pobiera URL strony internetowej z payloadu MQTT, generuje zrzut ekranu, a następnie udostępnia wynikowy plik PNG przez lokalny serwer HTTP w kontenerze Docker.

## Funkcje
1. **Odbieranie URL poprzez MQTT**: Program nasłuchuje na temat MQTT `pc/image/(nazwa pliku)` z payload zawierającym URL strony internetowej do zrzutu ekranu.
2. **Generowanie nazwy pliku**: Nazwa pliku PNG jest generowana na podstawie tematu MQTT.
3. **Tworzenie zrzutu ekranu**: Skrypt w python korzysta z biblioteki do automatyzacji przeglądarek (np. Selenium) do wykonania zrzutu ekranu strony internetowej.
4. **Udostępnianie zrzutu ekranu**: Zrzuty ekranu są zapisywane w katalogu udostępnianym przez serwer HTTP działający w kontenerze Docker, dzięki czemu są dostępne za pośrednictwem lokalnego adresu IP kontenera.

## Użycie z Home Assistant
Program "Screenshotter" może być używany z Home Assistant do wysyłania wiadomości ze zdjęciem zrzutu ekranu. Poprzez konfigurację integracji MQTT w Home Assistant, można zautomatyzować proces wykonywania zrzutów ekranu na podstawie różnych wyzwalaczy i warunków.
