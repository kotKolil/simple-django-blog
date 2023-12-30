FROM python:3.8

WORKDIR /app

#this variable turn on/off debug mode 

ENV debug = False

COPY . .

RUN pip install --no-cache-dir -r r.txt

EXPOSE 80

EXPOSE 8000

CMD ["python" , "manage.py" , "runserver" , "0.0.0.0:8000"]