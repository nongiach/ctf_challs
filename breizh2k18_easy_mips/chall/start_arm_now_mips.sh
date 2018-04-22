#!/bin/bash -i

arm_now start mips32el --sync --redir tcp:4242::4242

# while [ true ]
# for i in {0..10}
# do
#   kill -s $(pgrep qemu-system-mipsel)
#   rm -rf arm_now
#   cp /clean arm_now -a
#   timeout 1m arm_now start mips32el --sync --redir tcp:4242::4242
#   reset
#   stty intr ^c
#   sleep 10s
# done
