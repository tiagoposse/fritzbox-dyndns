FROM arm64v8/python:3.9-alpine

RUN apk update && apk add bind-tools

COPY main.py requirements.txt /app/
COPY providers/ /app/providers

RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "/app/main.py" ]
