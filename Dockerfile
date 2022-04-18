FROM python:3.9
COPY . /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt