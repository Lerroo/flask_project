FROM ubuntu:latest
RUN apt-get update -y
# RUN apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev
COPY . /app
WORKDIR /app 
RUN pip3 install -r requirements.txt
ENTRYPOINT ['python']
CMD ['run.py']