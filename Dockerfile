FROM python:3.8-slim

COPY ./app ./app

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install unzip
RUN apt-get -y install wget
RUN apt-get -y install fontconfig

RUN wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
RUN unzip NanumFont_TTF_ALL.zip -d NanumFont
RUN rm -f NanumFont_TTF_ALL.zip
RUN mv NanumFont /usr/share/fonts/
RUN fc-cache -f -v

RUN pip3 install --upgrade pip
RUN pip3 install opencv-python Flask Werkzeug Pillow requests

WORKDIR /app

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]