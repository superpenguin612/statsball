FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python2-dev build-essential
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py; python2 get-pip.py
COPY . /app
WORKDIR /app
RUN python2 -m pip install -r requirements.txt
CMD ["gunicorn", "--reload", "app:app"]