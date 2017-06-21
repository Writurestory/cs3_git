/* zombie test. */
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
int main()
{
  pid_t pid;
  switch(pid = fork())
    {
    case -1:
      perror("fork failed");
      exit(1);
    case 0:
      printf(" CHILD: My PID is %d, My parent's PID is %d\n", getpid(), getppid());
	  switch(pid = fork())
	    {
	    case -1:
	      perror("fork failed");
	      exit(1);
	    case 0:
	      printf(" CHILD: My PID is %d, My parent's PID is %d\n", getpid(), getppid());
	      sleep(2);   //to ensure the first child exit before the second child
	      exit(0);
	    default:
	      printf("PARENT: My PID is %d, My child's PID is %d\n", getpid(), pid);
	      printf("PARENT: I'm now free\n");
	      wait(NULL);
	    }
	      exit(0);
    default:
      printf("PARENT: My PID is %d, My child's PID is %d\n", getpid(), pid);
      printf("PARENT: I'm waiting first child\n");
      wait(NULL);
    }
  exit(0);
}
