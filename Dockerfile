FROM python:3.8.2-buster
COPY src/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY src/ /app
WORKDIR /app
CMD python3 main.py