dd if=/dev/urandom bs=32 count=1 | md5sum | cut -d ' ' -f 1 > chall/flag
