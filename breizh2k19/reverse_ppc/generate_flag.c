#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

typedef unsigned long int  u4;
typedef struct ranctx { u4 a; u4 b; u4 c; u4 d; } ranctx;

#define rot(x,k) (((x)<<(k))|((x)>>(32-(k))))
u4 ranval( ranctx *x ) {
    u4 e = x->a - rot(x->b, 27);
    x->a = x->b ^ rot(x->c, 17);
    x->b = x->c + x->d;
    x->c = x->d + e;
    x->d = e + x->a;
    return x->d;
}

void raninit( ranctx *x, u4 seed ) {
    u4 i;
    x->a = 0xf1ea5eec, x->b = x->c = x->d = seed;
    for (i=0; i<20; ++i) {
        (void)ranval(x);
    }
}


unsigned int init_transpose(ranctx *state, unsigned int *transpose, unsigned int *ntranspose) {
	for (unsigned int i = 0; i < 256; i++) {
		transpose[i] = i;
		ntranspose[i] = i;
	}
	for (unsigned int i = 0; i < 256; i++) {
		unsigned int v = ranval(state) % 256;
		transpose[i] = transpose[i] ^ transpose[v];
		transpose[v] = transpose[i] ^ transpose[v];
		transpose[i] = transpose[i] ^ transpose[v];
	}
	for (unsigned int i = 0; i < 256; i++) {
		ntranspose[transpose[i]] = i;
	}
}

void do_transpose(unsigned char *s, unsigned int *transpose) {
	for (unsigned int i = 0; s[i]; i++) {
		/* printf("%u => %u, %c => %c\n", */
		/* 		s[i], transpose[s[i]], */
		/* 		s[i], transpose[s[i]]); */
		s[i] = transpose[s[i]];
	}
}

void do_print(unsigned char *s) {
	/* printf("%s\n", s); */
	for (unsigned int i = 0; s[i]; i++) {
		printf("%u,", s[i]);
	}
	printf("0");
	printf("\n");
}

int main(int ac, char **av) {
 // apt install gcc-7-powerpc64-linux-gnu
 // powerpc64-linux-gnu-gcc-7 main.c -o ppc
 	if (ac == 1) {
		printf("Usage: ./generate_flag flag\n");
		exit(1);
	}
	ranctx state;
	raninit(&state, 0x378687);

	unsigned int transpose[256] = {0};
	unsigned int r_transpose[256] = {0};
	init_transpose(&state, transpose, r_transpose);

	/* unsigned char flag[] = "Br{ThisIsTheFuckingFlag}"; */
	unsigned char *flag = av[1];
	/* unsigned char flag[] = {219,135,32,124,200,124,219,135,62,142,118,69,74,32,149,37,142,44,157,37, 0}; */
	/* unsigned char input[256]; */
	/* write(1, "Password: ", 10); */
	/* int read_ret = read(0, input, 256); */
	/* input[read_ret - 1] = 0; */
	do_transpose(flag, transpose);
	do_print(flag);
	/* if (strcmp(input, flag) == 0) { */
	/* 	printf("Good job, @chaignc is proud of you\n"); */
	/* } else { */
	/* 	printf("Bad password\n"); */
	/* } */
	return 0;
}
