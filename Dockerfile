# syntax=docker/dockerfile:1
# Gibt an von was ein Image erstellt werden soll
FROM python:3 
#Arbeitsordner auf unseren viruellen Maschinen (Arbeitsordner)
WORKDIR /usr/src/app
# kopiert die requiremetns.txt Datei in das Image
COPY requirements_lin.txt ./
# der RUN Befehl führt Linux Befehle aus
RUN /usr/local/bin/python -m pip install --upgrade pip
# installiert die requirements_lin.txt
RUN pip install --no-cache-dir -r requirements_lin.txt
RUN apt-get -y update

# setup ffmpeg
RUN apt-get install -y ffmpeg
RUN pip uninstall -y ffmpeg-python
RUN pip install ffmpeg-python

# setup redis server
RUN apt-get install -y redis-server
RUN sed -i "s/^# requirepass.*/requirepass foobared/" /etc/redis/redis.conf
# copiert alles von unserem Arbeitsordner (Windows) in unseren Arbeitsordner der viruellen Maschine (WORKDIR)
COPY . . 
RUN chmod +x start.sh
# 
CMD ["./start.sh"]
