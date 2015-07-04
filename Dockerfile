FROM python:2-onbuild
MAINTAINER skyper@skyplabs.net

RUN mkdir /backups

WORKDIR /usr/src/app
ENTRYPOINT ["python", "wp_backup_data.py"]
CMD ["-d", "/backups"]
