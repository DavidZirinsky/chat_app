FROM python:3.7.0-slim-stretch

ENV HOME=/chat_app
ENV PYTHONUNBUFFERED=0

WORKDIR /chat_app
COPY *.py ./
COPY requirements.txt .

RUN pip3 install -r requirements.txt
EXPOSE 5000:5000
CMD ["python", "app.py"]