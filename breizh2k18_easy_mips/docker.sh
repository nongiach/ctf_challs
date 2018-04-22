#!/bin/sh
docker kill ctf
docker build -t ctf .
echo start ctf docker
docker run -p 4242:4242/tcp -d --name ctf --rm -it ctf bash -i /chall/start_arm_now_mips.sh
# docker run -v $PWD/chall:/chall -p 4242:4242/tcp -d --name ctf --rm -it ctf bash -i /chall/start_arm_now_mips.sh
# docker kill ctf
