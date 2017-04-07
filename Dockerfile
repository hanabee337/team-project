FROM        eb-base
MAINTAINER  hanabee337@gmail.com

#RUN         apt-get -y update
#RUN         apt-get -y install python3
#RUN         apt-get -y install python3-pip
#RUN         apt-get -y install nginx

#WORKDIR     /srv
#RUN         mkdir app
#WORKDIR     /srv/app

COPY        . /srv/app
WORKDIR     /srv/app

RUN         pip3 install -r requirements.txt
RUN         pip3 install uwsgi
#WORKDIR     /srv/app/django_app
#CMD         ["python3", "manage.py", "runserver", "0:8080"]

COPY        .conf/uwsgi-app.ini         /etc/uwsgi/sites/app.ini
COPY        .conf/nginx.conf            /etc/nginx/nginx.conf
COPY        .conf/nginx-app.conf        /etc/nginx/sites-available/app.conf
#COPY        .conf/supervisor-app.conf   /etc/supervisor/conf.d/
RUN         ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/app.conf
#
#EXPOSE      4040
#CMD         supervisord -n