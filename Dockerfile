ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

EXPOSE 8000

ENTRYPOINT [ "python", "./rich_menus/rich_menus_sdk.py" ]

CMD [ "gunicorn", "--bind", ":8000", "--workers", "2", "Linebot.wsgi" ]
