#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

void urldecode(char *dst, const char *src)
{
  char a, b;
  while (*src) {
    if (*src == '%') {
      a = src[1];
      b = src[2];
      if (isxdigit(a) && isxdigit(b)) {
        if (a >= 'a')
          a -= 'a'-'A';
        if (a >= 'A')
          a -= ('A' - 10);
        else
          a -= '0';
        if (b >= 'a')
          b -= 'a'-'A';
        if (b >= 'A')
          b -= ('A' - 10);
        else
          b -= '0';
        *dst++ = 16*a+b;
      }
      src+=3;
    } else if (*src == '+') {
      *dst++ = ' ';
      src++;
    } else {
      *dst++ = *src++;
    }
  }
  *dst++ = '\0';
}

char not_found[] = "<p>The requested URL <code>%s</code> was not found on this server.  <ins>That’s all we know.</ins>\n"; // sorry for the xss

void handle_client(char request[]) {
  char url[32];

  if (!strncmp(request, "GET ", 4)) {
    if (strlen(request + 4) < sizeof(url)) {
      urldecode(url, request + 4);
      printf(not_found, url);
      fflush(stdout);
    }
  }
}

void baby_http() {
  char request[1024];

  while (42) {
    int size = read(0, request, 1023);
    request[size] = 0;
    handle_client(request);
  }
}

int main()
{
  printf("BabyHttp brought to you by @chaign_c\n");
  fflush(stdout);
  baby_http();
  return 0;
}
// what is arm_now ?
