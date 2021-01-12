FROM python:3.7

RUN pip install fastapi uvicorn

COPY . /code

WORKDIR /code/

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]