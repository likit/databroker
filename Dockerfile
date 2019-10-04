FROM python:3.7

RUN mkdir -p /datatube/service
COPY /service/requirements.txt /datatube/service
WORKDIR /datatube/service
RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "5", "--threads", "12", "service.main:app"]