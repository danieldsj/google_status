FROM python:3.7-alpine

ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir pipenv \
 && pipenv install -r requirements.txt \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py install

CMD ["pipenv", "run", "python3", "-m", "google_status"]
