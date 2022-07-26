FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN mkdir /api_service

COPY ./api_service /api_service
COPY ./requirements.txt /api_service
WORKDIR /api_service
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py shell < create_admin.py
EXPOSE 8000
CMD python manage.py runserver