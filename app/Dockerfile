FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN addgroup -S app && adduser -S -G app app

# depend on the build.sh script or volume mapping to add the core package
COPY --chown=app ./requirements.pip /app/requirements.pip

RUN apk update && \
 apk add postgresql-libs bash && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install --no-cache-dir -r /app/requirements.pip && \
 rm /app/requirements.pip && \
 apk --purge del .build-deps

COPY --chown=app ./ /app

USER app
WORKDIR /app
ENTRYPOINT ["/app/entrypoint.sh"]
CMD [""]
