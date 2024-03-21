FROM python:3.12.0-slim-bookworm

WORKDIR /usr/src/app/

COPY . .
RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

