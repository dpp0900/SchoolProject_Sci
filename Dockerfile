FROM python:3.8-slim

COPY ./app ./app

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0

RUN pip3 install --upgrade pip
RUN pip3 install opencv-python Flask Werkzeug Pillow requests

WORKDIR /app

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]