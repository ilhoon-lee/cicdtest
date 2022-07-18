FROM python:3.8
WORKDIR usr/src/flask_app
COPY requirements.txt .
RUN apt-get update 
RUN pip install --upgrade pip
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT gunicorn -w 1 -b 0.0.0.0:8000 wsgi:server
COPY . .
