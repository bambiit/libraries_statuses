FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3 python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip install python-dotenv && pip install Django && pip install psycopg2-binary && pip install django-connection-url

WORKDIR /var/www/html
ADD . /var/www/html
RUN chown -R www-data:www-data /var/www/html

CMD python manage.py migrate && python manage.py crawl && python manage.py runserver 0.0.0.0:$PORT
