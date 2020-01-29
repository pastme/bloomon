FROM python:3.7.5

RUN mkdir -p /code
WORKDIR /code
ADD bouquets_from_flowers.py /code/bouquets_from_flowers.py
ADD stream.txt /code/stream.txt

CMD [ "python", "./bouquets_from_flowers.py" ]