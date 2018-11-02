FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN addgroup -S app && adduser -S -G app app

COPY --chown=app ./ /

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add --no-cache postgresql-dev bash && \
    pip install --no-cache-dir -r requirements.pip && \
    apk del build-deps gcc && \
    chmod +x /entrypoint.sh

USER app

WORKDIR /migrations

ENTRYPOINT ["/entrypoint.sh"]