FROM python:3.10

MAINTAINER Anton Grigoryev <grianton535@gmail.com>

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements txt

COPY src/ .

EXPOSE 65525

CMD ["python", "main.py"]


