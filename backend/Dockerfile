FROM python:3.8

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .
ENV FLASK_ENV production

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app"]