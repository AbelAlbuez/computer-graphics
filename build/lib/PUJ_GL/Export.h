
#ifndef PUJ_GL_EXPORT_H
#define PUJ_GL_EXPORT_H

#ifdef PUJ_GL_STATIC_DEFINE
#  define PUJ_GL_EXPORT
#  define PUJ_GL_NO_EXPORT
#else
#  ifndef PUJ_GL_EXPORT
#    ifdef PUJ_GL_EXPORTS
        /* We are building this library */
#      define PUJ_GL_EXPORT 
#    else
        /* We are using this library */
#      define PUJ_GL_EXPORT 
#    endif
#  endif

#  ifndef PUJ_GL_NO_EXPORT
#    define PUJ_GL_NO_EXPORT 
#  endif
#endif

#ifndef PUJ_GL_DEPRECATED
#  define PUJ_GL_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef PUJ_GL_DEPRECATED_EXPORT
#  define PUJ_GL_DEPRECATED_EXPORT PUJ_GL_EXPORT PUJ_GL_DEPRECATED
#endif

#ifndef PUJ_GL_DEPRECATED_NO_EXPORT
#  define PUJ_GL_DEPRECATED_NO_EXPORT PUJ_GL_NO_EXPORT PUJ_GL_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef PUJ_GL_NO_DEPRECATED
#    define PUJ_GL_NO_DEPRECATED
#  endif
#endif

#endif /* PUJ_GL_EXPORT_H */
