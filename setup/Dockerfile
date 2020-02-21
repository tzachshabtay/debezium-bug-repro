FROM python:3.8-buster

RUN pip3 install requests psycopg2-binary

### waitforit
RUN wget -q -O /usr/local/bin/waitforit https://github.com/maxcnunes/waitforit/releases/download/v2.4.1/waitforit-linux_amd64 && chmod +x /usr/local/bin/waitforit

COPY ./bin/* /usr/local/bin/
