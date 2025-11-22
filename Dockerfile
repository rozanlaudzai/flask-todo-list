FROM python:3.12-slim-trixie

WORKDIR /flask-todo-list

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD ["python3", "app.py"]
