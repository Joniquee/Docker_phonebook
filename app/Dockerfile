FROM python:alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN pip install --upgrade pip
RUN pip install flask psycopg2-binary

COPY . .

CMD ["python", "back.py"]