FROM python:3.10.14

WORKDIR /code

COPY . .

RUN python -m pip --no-cache-dir install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.api:app", "--workers", "3", "--host", "0.0.0.0", "--port", "8080", "--reload"]