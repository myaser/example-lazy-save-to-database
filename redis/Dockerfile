FROM redis:5-alpine
RUN apk add --no-cache bash
COPY redis.conf /usr/local/etc/redis/redis.conf
COPY maintainance/ /
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
