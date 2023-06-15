FROM python:3.10
RUN apt-get update
ENV TZ Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt 
COPY . /app
WORKDIR /app


RUN  chown nobody /app -R
USER nobody
