FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD ./client_secret.json .
ADD ./src/ .

CMD [ "python", "./run.py" ]
