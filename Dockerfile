FROM python:3.8

WORKDIR /code
COPY /. .

RUN apt update && apt install wkhtmltopdf -y
RUN pip install --upgrade pip && pip install -r requirements.txt
