FROM python:3



RUN pip3 install --upgrade pip
RUN pip3 install opencv-python Flask Werkzeug Pilow requests

