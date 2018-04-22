
CC      = mipsel-linux-gnu-gcc
CFLAGS   += -W -Wall -Wextra

all:
	$(CC) main.c -o vuln -z execstack -static -fno-stack-protector

clean:
	rm vuln
