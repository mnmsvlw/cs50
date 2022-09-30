FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip build-essential

WORKDIR /app 
COPY . /app

RUN pip install -r /app/requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

EXPOSE 8000

VOLUME [ "/app/data" ] 

CMD [ "python3" , "manage.py" , "runserver", "0.0.0.0:8000"]