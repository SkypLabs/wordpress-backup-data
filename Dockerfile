FROM python:2-onbuild
MAINTAINER Paul-Emmanuel Raoul <skyper@skyplabs.net>

RUN mkdir /backups

WORKDIR /usr/src/app
ENTRYPOINT ["python", "wp-backup-data"]
CMD ["-d", "/backups"]
