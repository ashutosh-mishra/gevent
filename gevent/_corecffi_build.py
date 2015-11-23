# pylint: disable=too-many-lines, protected-access, redefined-outer-name

# This module is only used to create and compile the gevent._corecffi module;
# nothing should be directly imported from it except `ffi`, which should only be
# used for `ffi.compile()`; programs should import gevent._corecfffi.
# However, because we are using "out-of-line" mode, it is necessary to examine
# this file to know what functions are created and available on the generated
# module.
from __future__ import absolute_import, print_function
import sys
import os
import struct

__all__ = []


def system_bits():
    return struct.calcsize('P') * 8


def st_nlink_type():
    if sys.platform == "darwin":
        return "short"
    elif system_bits() == 32:
        return "unsigned long"
    return "long long"


from cffi import FFI
ffi = FFI()
_cdef = """
#define EV_MINPRI ...
#define EV_MAXPRI ...

#define EV_VERSION_MAJOR ...
#define EV_VERSION_MINOR ...

#define EV_UNDEF ...
#define EV_NONE ...
#define EV_READ ...
#define EV_WRITE ...
#define EV__IOFDSET ...
#define EV_TIMER ...
#define EV_PERIODIC ...
#define EV_SIGNAL ...
#define EV_CHILD ...
#define EV_STAT ...
#define EV_IDLE ...
#define EV_PREPARE ...
#define EV_CHECK ...
#define EV_EMBED ...
#define EV_FORK ...
#define EV_CLEANUP ...
#define EV_ASYNC ...
#define EV_CUSTOM ...
#define EV_ERROR ...

#define EVFLAG_AUTO ...
#define EVFLAG_NOENV ...
#define EVFLAG_FORKCHECK ...
#define EVFLAG_NOINOTIFY ...
#define EVFLAG_SIGNALFD ...
#define EVFLAG_NOSIGMASK ...

#define EVBACKEND_SELECT ...
#define EVBACKEND_POLL ...
#define EVBACKEND_EPOLL ...
#define EVBACKEND_KQUEUE ...
#define EVBACKEND_DEVPOLL ...
#define EVBACKEND_PORT ...
/* #define EVBACKEND_IOCP ... */

#define EVBACKEND_ALL ...
#define EVBACKEND_MASK ...

#define EVRUN_NOWAIT ...
#define EVRUN_ONCE ...

#define EVBREAK_CANCEL ...
#define EVBREAK_ONE ...
#define EVBREAK_ALL ...

struct ev_loop {
    int backend_fd;
    int activecnt;
    ...;
};
struct ev_io {
    int fd;
    int events;
    ...;
};
struct ev_timer {
    double at;
    ...;
};
struct ev_signal {...;};
struct ev_idle  {...;};
struct ev_prepare {...;};
struct ev_check {...;};
struct ev_fork  {...;};
struct ev_async  {...;};
struct ev_child {
    int pid;
    int rpid;
    int rstatus;
    ...;
};
struct stat {
    """ + st_nlink_type() + """ st_nlink;
    ...;
};

struct ev_stat {
    struct stat attr;
    const char* path;
    struct stat prev;
    double interval;
    ...;
};

typedef double ev_tstamp;

int ev_version_major();
int ev_version_minor();

unsigned int ev_supported_backends (void);
unsigned int ev_recommended_backends (void);
unsigned int ev_embeddable_backends (void);

ev_tstamp ev_time (void);
void ev_set_syserr_cb(void *);

int ev_priority(void*);
void ev_set_priority(void*, int);

int ev_is_pending(void*);
int ev_is_active(void*);
void ev_io_init(struct ev_io*, void* callback, int fd, int events);
void ev_io_start(struct ev_loop*, struct ev_io*);
void ev_io_stop(struct ev_loop*, struct ev_io*);
void ev_feed_event(struct ev_loop*, void*, int);

void ev_timer_init(struct ev_timer*, void (*callback)(struct ev_loop *_loop, struct ev_timer *w, int revents), double, double);
void ev_timer_start(struct ev_loop*, struct ev_timer*);
void ev_timer_stop(struct ev_loop*, struct ev_timer*);
void ev_timer_again(struct ev_loop*, struct ev_timer*);

void ev_signal_init(struct ev_signal*, void* callback, int);
void ev_signal_start(struct ev_loop*, struct ev_signal*);
void ev_signal_stop(struct ev_loop*, struct ev_signal*);

void ev_idle_init(struct ev_idle*, void* callback);
void ev_idle_start(struct ev_loop*, struct ev_idle*);
void ev_idle_stop(struct ev_loop*, struct ev_idle*);

void ev_prepare_init(struct ev_prepare*, void* callback);
void ev_prepare_start(struct ev_loop*, struct ev_prepare*);
void ev_prepare_stop(struct ev_loop*, struct ev_prepare*);

void ev_check_init(struct ev_check*, void* callback);
void ev_check_start(struct ev_loop*, struct ev_check*);
void ev_check_stop(struct ev_loop*, struct ev_check*);

void ev_fork_init(struct ev_fork*, void* callback);
void ev_fork_start(struct ev_loop*, struct ev_fork*);
void ev_fork_stop(struct ev_loop*, struct ev_fork*);

void ev_async_init(struct ev_async*, void* callback);
void ev_async_start(struct ev_loop*, struct ev_async*);
void ev_async_stop(struct ev_loop*, struct ev_async*);
void ev_async_send(struct ev_loop*, struct ev_async*);
int ev_async_pending(struct ev_async*);

void ev_child_init(struct ev_child*, void* callback, int, int);
void ev_child_start(struct ev_loop*, struct ev_child*);
void ev_child_stop(struct ev_loop*, struct ev_child*);

void ev_stat_init(struct ev_stat*, void* callback, char*, double);
void ev_stat_start(struct ev_loop*, struct ev_stat*);
void ev_stat_stop(struct ev_loop*, struct ev_stat*);

struct ev_loop *ev_default_loop (unsigned int flags);
struct ev_loop* ev_loop_new(unsigned int flags);
void ev_loop_destroy(struct ev_loop*);
void ev_loop_fork(struct ev_loop*);
int ev_is_default_loop (struct ev_loop *);
unsigned int ev_iteration(struct ev_loop*);
unsigned int ev_depth(struct ev_loop*);
unsigned int ev_backend(struct ev_loop*);
void ev_verify(struct ev_loop*);
void ev_run(struct ev_loop*, int flags);

ev_tstamp ev_now (struct ev_loop *);
void ev_now_update (struct ev_loop *); /* update event loop time */
void ev_ref(struct ev_loop*);
void ev_unref(struct ev_loop*);
void ev_break(struct ev_loop*, int);
unsigned int ev_pending_count(struct ev_loop*);

struct ev_loop* gevent_ev_default_loop(unsigned int flags);
void gevent_install_sigchld_handler();

void (*gevent_noop)(struct ev_loop *_loop, struct ev_timer *w, int revents);
void ev_sleep (ev_tstamp delay); /* sleep for a while */

typedef int... vfd_socket_t;
int vfd_open(vfd_socket_t);
vfd_socket_t vfd_get(int);
void vfd_free(int);
"""

# Note that we do not cdef the vfd_* family of functions,
# nor do we include libev_vfd.h in the _source; we'd need to get
# the correct parameter types to do so (which )

_watcher_types = [
    'ev_async',
    'ev_check',
    'ev_child',
    'ev_fork',
    'ev_idle',
    'ev_io',
    'ev_prepare',
    'ev_signal',
    'ev_stat',
    'ev_timer',
]

_source = """   // passed to the real C compiler
#define LIBEV_EMBED 1
#include "libev_vfd.h"
#include "libev.h"

static void
_gevent_noop(struct ev_loop *_loop, struct ev_timer *w, int revents) { }

void (*gevent_noop)(struct ev_loop *, struct ev_timer *, int) = &_gevent_noop;
"""

# Setup the watcher callbacks
_cbs = """
static int (*python_callback)(void* handle, int revents);
static void (*python_handle_error)(void* handle, int revents);
static void (*python_stop)(void* handle);
"""
_cdef += _cbs
_source += _cbs
_watcher_type = None

for _watcher_type in _watcher_types:
    _cdef += """
   struct gevent_%s {
        // recall that the address of a struct is the
        // same as the address of its first member, so
        // this struct is interchangable with the ev_XX
        // that is its first member.
        struct %s watcher;
        // the CFFI handle to the Python watcher object
        void* handle;
        ...;
    };
    static void _gevent_%s_callback(struct ev_loop* loop, struct %s* watcher, int revents);
    """ % (_watcher_type, _watcher_type, _watcher_type, _watcher_type)

    _source += """
    struct gevent_%s {
        struct %s watcher;
        void* handle;
    };
    """ % (_watcher_type, _watcher_type)

    _source += """
    static void _gevent_%s_callback(struct ev_loop* loop, struct %s* watcher, int revents)
    {
        // invoke self.callback()
        void* handle = ((struct gevent_%s *)watcher)->handle;
        int cb_result = python_callback(handle, revents);
        switch(cb_result) {
            case -1:
                // in case of exception, call self.loop.handle_error;
                // this function is also responsible for stopping the watcher
                // and allowing memory to be freed
                python_handle_error(handle, revents);
                break;
            case 0:
                // Code to stop the event. Note that if python_callback
                // has disposed of the last reference to the handle,
                // `watcher` could now be invalid/disposed memory!
                if (!ev_is_active(watcher)) {
                    python_stop(handle);
                }
                break;
            default:
                assert(cb_result == 1);
                // watcher is already stopped and dead, nothing to do.
        }
    }
    """ % (_watcher_type, _watcher_type, _watcher_type)

thisdir = os.path.dirname(os.path.realpath(__file__))
include_dirs = [thisdir, os.path.join(thisdir, 'libev')]
ffi.cdef(_cdef)
ffi.set_source('gevent._corecffi', _source, include_dirs=include_dirs)

if __name__ == '__main__':
    ffi.compile()
