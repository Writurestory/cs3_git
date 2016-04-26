
/*
** mmapdemo.c -- demonstrates memory mapped files lamely.
*/

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <errno.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

/**************** This is a semphore ***************/

/*
**-- demonstrates semaphore use as a file locking mechanism
*/

#define MAX_RETRIES 10

union semun {
	int val;
	struct semid_ds *buf;
	ushort *array;
};

/*
** initsem() -- more-than-inspired by W. Richard Stevens' UNIX Network
** Programming 2nd edition, volume 2, lockvsem.c, page 295.
*/
int initsem(key_t key, int nsems)  /* key from ftok() */
{
	int i;
	union semun arg;
	struct semid_ds buf;
	struct sembuf sb;
	int semid;

	semid = semget(key, nsems, IPC_CREAT | IPC_EXCL | 0666);

	if (semid >= 0) { /* we got it first */
		sb.sem_op = 1; sb.sem_flg = 0;
		arg.val = 1;

		printf("press return\n"); getchar();

		for(sb.sem_num = 0; sb.sem_num < nsems; sb.sem_num++) { 
			/* do a semop() to "free" the semaphores. */
			/* this sets the sem_otime field, as needed below. */
			if (semop(semid, &sb, 1) == -1) {
				int e = errno;
				semctl(semid, 0, IPC_RMID); /* clean up */
				errno = e;
				return -1; /* error, check errno */
			}
		}

	} else if (errno == EEXIST) { /* someone else got it first */
		int ready = 0;

		semid = semget(key, nsems, 0); /* get the id */
		if (semid < 0) return semid; /* error, check errno */

		/* wait for other process to initialize the semaphore: */
		arg.buf = &buf;
		for(i = 0; i < MAX_RETRIES && !ready; i++) {
			semctl(semid, nsems-1, IPC_STAT, arg);
			if (arg.buf->sem_otime != 0) {
				ready = 1;
			} else {
				sleep(1);
			}
		}
		if (!ready) {
			errno = ETIME;
			return -1;
		}
	} else {
		return semid; /* error, check errno */
	}

	return semid;
}

int main(int argc, char *argv[])
{
	key_t key;
	int semid;
	struct sembuf sb;
	
	sb.sem_num = 0;
	sb.sem_op = -1;  /* set to allocate resource */
	sb.sem_flg = SEM_UNDO;

	if ((key = ftok("semdemo.c", 'J')) == -1) {
		perror("ftok");
		exit(1);
	}

	/* grab the semaphore set created by seminit.c: */
	if ((semid = initsem(key, 1)) == -1) {
		perror("initsem");
		exit(1);
	}

	printf("Press return to lock: ");
	getchar();
	printf("Trying to lock...\n");

	if (semop(semid, &sb, 1) == -1) {
		perror("semop");
		exit(1);
	}

    
	printf("Locked.\n");
	printf("Press return to unlock: ");
	getchar();

	sb.sem_op = 1; /* free resource */
	if (semop(semid, &sb, 1) == -1) {
		perror("semop");
		exit(1);
	}

	printf("Unlocked\n");

    /********************** This is mmap ******************/
	int fd, offset;
	char *data;
	struct stat sbuf;

	if (argc != 2) {
		fprintf(stderr, "usage: mmapdemo offset\n");
		exit(1);
	}

	if ((fd = open("mmapdemo.c", O_RDONLY)) == -1) {
		perror("open");
		exit(1);
	}

	if (stat("mmapdemo.c", &sbuf) == -1) {
		perror("stat");
		exit(1);
	}

	offset = atoi(argv[1]);
	if (offset < 0 || offset > sbuf.st_size-1) {
		fprintf(stderr, "mmapdemo: offset must be in the range 0-%d\n", sbuf.st_size-1);
		exit(1);
	}
	
	if ((data = mmap((caddr_t)0, sbuf.st_size, PROT_READ, MAP_SHARED, fd, 0)) == (caddr_t)(-1)) {
		perror("mmap");
		exit(1);
	}

	printf("byte at offset %d is '%c'\n", offset, data[offset]);

	return 0;

    /***************** end of mmap ***************************/
}
