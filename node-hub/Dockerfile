FROM eclipse-mosquitto:alpine

RUN apk add --no-cache gettext

# Copy mosquitto-go-auth plugin here
COPY go-auth.so /mosquitto/go-auth.so

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]