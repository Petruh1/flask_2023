
FROM python:3.11

WORKDIR /new_code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .




