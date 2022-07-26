FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN mkdir /stock_service

COPY ./stock_service /stock_service
COPY ./requirements.txt /stock_service
WORKDIR /stock_service
RUN pip install -r requirements.txt
EXPOSE 8001
CMD python manage.py runserver 8001