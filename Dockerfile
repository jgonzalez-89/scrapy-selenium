FROM python:3.9-slim

# Instalar dependencias del sistema y Firefox
RUN apt-get update && \
    apt-get install -y wget libx11-6 libx11-xcb1 libdbus-glib-1-2 libxt6 && \
    wget -q --show-progress --no-check-certificate --content-disposition "https://download-installer.cdn.mozilla.net/pub/firefox/releases/98.0.2/linux-x86_64/en-US/firefox-98.0.2.tar.bz2" && \
    tar -xjf firefox-*.tar.bz2 && \
    mv firefox /usr/local/lib/ && \
    ln -s /usr/local/lib/firefox/firefox /usr/local/bin/firefox

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/launcher.py"]