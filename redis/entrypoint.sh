#!/usr/bin/env bash

set -o errexit
set -o pipefail

# set -o nounset
sed -i 's/{REDIS_PASSWORD}/'"${REDIS_PASSWORD}"'/g' /usr/local/etc/redis/redis.conf

exec redis-server /usr/local/etc/redis/redis.conf
