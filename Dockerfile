FROM python:3.10.11-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "flask" ]

CMD [ "run", "--host=0.0.0.0" ]
