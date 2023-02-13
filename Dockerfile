FROM debian:10
RUN apt-get update -y
RUN apt-get install --no-install-recommends -y python3.7 python3-dateutil python3-pip
RUN pip3 install --upgrade setuptools
RUN pip3 install django mongoengine python-memcached==1.59 gunicorn pytest pytest-django requests && \
mkdir -p /var/log/rss -m 0775 
RUN mkdir -p /opt/web/rss/
WORKDIR /opt/web/rss/ 
COPY . .
RUN ln -s /usr/bin/python3 /usr/bin/python
EXPOSE 80
RUN cd /opt/web/rss/ 
CMD ["gunicorn", "wsgi:application", "-b", "0.0.0.0:80", "-w", "10"]
