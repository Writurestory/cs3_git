#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUMBER_OF_THREADS 10

void *print_hello_world(void *tid)
{
  /* prints the thread's identifier, then exits.*/
  printf ("Thread %ld: Hello World!\n", (long)tid);
  pthread_exit(NULL);
}

int main(int argc, char *argv[])
{
  pthread_t threads[NUMBER_OF_THREADS];
  int status;
  long i;
  for (i=0; i<NUMBER_OF_THREADS; i++)
    {
      status = pthread_create(&threads[i], NULL, print_hello_world, (void *)i);
      printf ("Main: creating thread %ld\n",i);
      /* printf("thread id: %d\n",threads[i]); */

      if(status != 0){
        printf ("Oops. pthread_create returned error code %d\n",status);
        exit(-1);
      }
      if(pthread_join(threads[i], NULL)){
        printf("error joining thread.");
        abort() ;
      }
 }
  exit(0);
}
