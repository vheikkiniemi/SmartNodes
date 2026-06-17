FROM iegomez/mosquitto-go-auth

USER root

RUN apk add --no-cache gettext

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]