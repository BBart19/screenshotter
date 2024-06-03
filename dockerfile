# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.12-slim

# Ustawienie zmiennych środowiskowych
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalacja zależności systemowych
RUN apt-get update && \
    apt-get install -y wget gnupg2 ca-certificates procps libxss1 \
    libappindicator1  libasound2 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libgtk-3-0 libpango-1.0-0 libcairo2 \
    libatspi2.0-0 libatk-bridge2.0-0 libxkbcommon0 cgroup-tools fonts-liberation \
    libappindicator3-1 libatk1.0-0 libcups2 libdrm2 libdbus-1-3 libxshmfence1 && \
    apt-get clean

# Dodanie Chrome do źródeł APT
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Instalacja Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable && apt-get clean

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Kopiowanie plików projektu do kontenera
COPY . /app

# Instalacja zależności Pythona
RUN pip install --no-cache-dir pyppeteer paho-mqtt

# Uruchomienie skryptu przy starcie kontenera
CMD ["python", "obraz.py"]
