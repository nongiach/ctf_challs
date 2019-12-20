FROM ctfchaignc/xenial_socat
# FROM ubuntu:xenial

RUN useradd -ms /bin/bash  ctf
# RUN apt update -y && apt install openssl

COPY ./chall /chall
COPY ./flag.txt /

COPY ./certificates /certs
RUN chown ctf -R /certs/ && chmod 600 /certs/*.*

USER ctf

EXPOSE 4242/tcp

CMD socat -d openssl-listen:4242,reuseaddr,fork,cert=/certs/server.pem,cafile=/certs/client.crt EXEC:/chall/heapme
