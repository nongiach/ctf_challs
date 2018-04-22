#!/bin/bash -i

rm -rf arm_now
cp /arm_now . -a
e2rm ./arm_now/rootfs.ext2:/etc/inittab
e2cp -G 0 -O 0 -P 555 ./inittab ./arm_now/rootfs.ext2:/etc/inittab
arm_now start mips32el --sync --redir tcp:4242::4242
cp arm_now /clean -a

# rm -rf arm_now
# cp /clean arm_now -a
# arm_now start mips32el --sync --redir tcp:4242::4242

# while [ true ]
# do
# 	timeout 30s arm_now start mips32el --sync --redir tcp:4242::4242
# done
