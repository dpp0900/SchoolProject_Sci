FROM python:3.8-slim

COPY ./app ./app

RUN pip3 install --upgrade pip
RUN pip3 install opencv-python Flask Werkzeug Pillow requests

WORKDIR /app

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]