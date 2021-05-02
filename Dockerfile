FROM python:3.8.2-buster
RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx tesseract-ocr libtesseract-dev
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY ./ /app
WORKDIR /app/src/
ENV TESSDATA_PREFIX="/app/tessdata"
ENTRYPOINT python3 main.py

