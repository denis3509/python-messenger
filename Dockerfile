FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app


RUN apk update
RUN apk add mc
EXPOSE $PORT
CMD [ "python" ,"code/server.py"]
