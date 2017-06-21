#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define FIFO_NAME "american_maid"

int main(void)
{
        char s[300];
            int num1, num2, num3, fd;

                mkfifo(FIFO_NAME, S_IFIFO | 0666);

                    printf("waiting for readers...\n");
                        fd = open(FIFO_NAME, O_WRONLY);
                            printf("got a reader--type some stuff\n");

                                while (gets(s), !feof(stdin)) {
                                            if ((num1 = write(fd, s, strlen(s))) == -1 || (num2 = write(fd, s, strlen(s))) == -1 || (num3 = write(fd, s, strlen(s))) == -1)
                                                            perror("write");
                                                    else
                                                                    printf("speak: wrote %d bytes\n", num1);
                                                                    printf("speak: wrote %d bytes\n", num2);
                                                                    printf("speak: wrote %d bytes\n", num3);
                                                        }

                                    return 0;
}
