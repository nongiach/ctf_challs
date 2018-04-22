# ctf_challs
name: easy_mips
desc: A basic stack buffer overflow on mips cpu. you are given the binary, the source code and the host:port.
point: 400 and pwn 4 times
ctf: breizhctf.com

You can easily deploy the challenge by starting ./docker.sh, it will setup everything using docker.

wait 30 secondes and you can connect to the port 4242.

```sh
mipsel_breizh2k18 $ nc 127.0.0.1 4242
BabyHttp brought to you by @chaign_c
```

tips: use arm_now tool to debug a mips programm https://github.com/nongiach/arm_now

Writeups:

| Credit | link |
| --- | --- |
| [Aperikube](https://twitter.com/AperiKube) | http://www.aperikube.fr/docs/breizhctf_2018_mips/ |
| [gov](https://twitter.com/govlog) | https://0bin.net/paste/TAOFEXebo71Lq6Es#VsAR6+5aqycYxg3C4YgQ1K5BjoUfUPayhEltlLWiBqi | 
