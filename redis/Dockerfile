FROM redis:4.0

MAINTAINER Stanislav WEB "stanisov@gmail.com"

#################################################
# Redis is designed to be accessed by trusted clients inside trusted environments.
# This means that usually it is not a good idea
# to expose the Redis instance directly to the internet or, in general,
# to an environment where untrusted clients can directly mod_registration the Redis TCP port
# or UNIX socket.
#################################################

ARG ENVMODE

COPY ./config/redis-$ENVMODE.conf /usr/local/etc/redis/redis.conf
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf"]