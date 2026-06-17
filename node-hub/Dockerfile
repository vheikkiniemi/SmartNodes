FROM iegomez/mosquitto-go-auth

USER root

RUN apt-get update \
    && apt-get install -y gettext-base \
    && rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]