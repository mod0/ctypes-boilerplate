# Sourced from /usr/lib/python2.7/ctypes/util.py
# Andreas Degert's find functions, using gcc, /sbin/ldconfig, objdump
import os, re, tempfile, errno

def _findLib_gcc(name):
    expr = r'[^\(\)\s]*lib%s\.[^\(\)\s]*' % re.escape(name)
    fdout, ccout = tempfile.mkstemp()
    os.close(fdout)
    cmd = 'if type gcc >/dev/null 2>&1; then CC=gcc; elif type cc >/dev/null 2>&1; then CC=cc;else exit 10; fi;' \
          '$CC -Wl,-t -o ' + ccout + ' 2>&1 -l' + name
    try:
        f = os.popen(cmd)
        try:
            trace = f.read()
        finally:
            rv = f.close()
    finally:
        try:
            os.unlink(ccout)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise
    if rv == 10:
        raise OSError, 'gcc or cc command not found'
    res = re.search(expr, trace)
    if not res:
        return None
    return res.group(0)


print _findLib_gcc('c') # finds C 
print _findLib_gcc('m') # finds math
print _findLib_gcc('mypythonc') # cannot find my library. I may have to put it in the loader path.

os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + """/home/username/Websites/sitename/site/codes/boilerplate-ctypes""" # May raise KeyError if you don't export the variable prior to opening python.

print _findLib_gcc('mypythonc') # Still does not find the library. I give up and will use CDLL with full path to the library.
