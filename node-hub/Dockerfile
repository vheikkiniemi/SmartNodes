FROM eclipse-mosquitto:alpine

USER root

COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY init-dynsec.sh /init-dynsec.sh

RUN chmod +x /docker-entrypoint.sh \
    && chmod +x /init-dynsec.sh

ENTRYPOINT ["/docker-entrypoint.sh"]