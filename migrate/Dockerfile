FROM frolvlad/alpine-glibc as downloader

ENV VERSION 3.0.1
ENV DOWNLOAD_URL https://github.com/mattes/migrate/releases/download/v$VERSION/migrate.linux-amd64.tar.gz

RUN apk add --no-cache ca-certificates openssl

RUN set -xe \
    && wget $DOWNLOAD_URL \
    && tar xvfz migrate.linux-amd64.tar.gz -C /tmp


FROM frolvlad/alpine-glibc

COPY [0-9]*.sql /migrations/
COPY --from=downloader /tmp/migrate.linux-amd64 /migrate-orig
COPY docker-entrypoint.sh /migrate
RUN chmod u+x /migrate

ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=root
ENV TIMEOUT=30

ENTRYPOINT ["/migrate"]
CMD ["--help"]
