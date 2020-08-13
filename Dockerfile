FROM python:3

WORKDIR /app

COPY requirements.txt ./
COPY cmd_docker.sh ./

RUN pip install -r requirements.txt


COPY . .

EXPOSE 5000

CMD ["cmd_docker.sh"]
