#include <stdlib.h>
#include <stdio.h>
#include <string.h>


void f(char *s)
{
    int i = atoi(s);
    if(i > 0 && i < 10) {
        printf("print i\n");
        printf("i: %d\n", i);
    } else if (i >= 10 && i < 20) {
        printf("user-controlled format string\n");
        printf(s, i);
    } else if (i >= 20 && i < 30) {
        printf("malloc buffer overflow, buf size: %d strlen(s): %ld\n", 30, strlen(s));
        char *buf = malloc(30);
        if(buf) {
            strcpy(buf, s);
            printf("%s\n", buf);
            free(buf);
        }
    } else if (i >= 30 && i < 40) {
        printf("calloc buffer overflow, buf size: %d strlen(s): %ld\n", 10*2, strlen(s));
        char *buf = calloc(10, 2);
        if(buf) {
            strcpy(buf, s);
            printf("%s\n", buf);
            free(buf);
        }
    } else if (i >= 40 && i < 50) {
        printf("realloc buffer overflow, buf size: %d strlen(s): %ld\n", 20, strlen(s));
        char *buf = realloc(NULL, strlen(s) + 1);
        if(buf) {
            strcpy(buf, s);
            printf("buf0: %s\n", buf);
            buf = realloc(buf, 20);
            if(buf) {
                strcpy(buf, s);
                printf("buf1: %s\n", buf);
                free(buf);
            }
        }
    } else if (i >= 50 && i < 60) {
        printf("realloc to double free, buf size: %d strlen(s): %ld\n", 20, strlen(s));
        char *buf = realloc(NULL, strlen(s) + 1);
        if(buf) {
            strcpy(buf, s);
            printf("buf0: %s\n", buf);
            buf = realloc(buf, strlen(s) + 1);
            if(buf) {
                strcpy(buf, s);
                printf("buf1: %s\n", buf);
                free(buf);
            }
            free(buf);
        }
    } else {
        char buf[20];
        printf("stack buffer overflow buf size: %ld strlen(s): %ld\n", sizeof(buf), strlen(s));
        strcpy(buf, s);
        printf("%s\n", buf);
    }
}

int main(int argc, char **argv)
{
    char s[128];
    if(argc == 1) {
        fgets(s, sizeof(s), stdin);
    } else {
        FILE * f = fopen(argv[1], "rb");
        if(f) {
            fgets(s, sizeof(s), f);
            fclose(f);
        } else {
            return 1;
        }
    }

    f(s);
    return 0;
}
