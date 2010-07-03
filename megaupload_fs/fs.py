#!/usr/bin/env python

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time

from fuse import FUSE, Operations, LoggingMixIn

from mega import *

class Memory(LoggingMixIn, Operations):
    """Example memory filesystem. Supports only one level of files."""
    
    def __init__(self):
        self.__mega = MegaUpload('your_account', 'your_pass')
        self.__mega.login()

        self.files = {}
        self.data = defaultdict(str)
        self.fd = 0
        now = time()
        self.files['/'] = dict(st_mode=(S_IFDIR | 0755), st_ctime=now,
            st_mtime=now, st_atime=now, st_nlink=2)
        
    def chmod(self, path, mode):
        return 0

    def chown(self, path, uid, gid):
        pass

    def create(self, path, mode):
        self.files[path] = dict(st_mode=(S_IFREG | mode), st_nlink=1,
            st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time())
        self.fd += 1
        return self.fd
    
    def getattr(self, path, fh=None):
        now = time()
        if path == "/":
            return dict(st_mode=(S_IFDIR | 0755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
        files = self.__mega.getFiles()
        parent_remote_id = '0'
        rem_file = None
        for p_elem in path.split("/")[1:]:
            rem_file = None
            for f in files.keys():
                if files[f]['parent_id'] == parent_remote_id.split("_")[0] and files[f]['name'] == p_elem:
                    parent_remote_id = f
                    rem_file = f
            if rem_file is None:
                break
        if rem_file is None:
            raise OSError(ENOENT, '')
        if files[rem_file]['type'] == 'folder':
            return dict(st_mode=(S_IFDIR | 0755), st_ctime=now,
                    st_mtime=now, st_atime=now, st_nlink=2)
        return dict(st_mode=(S_IFREG | 0755), st_ctime=now,
                    st_mtime=now, st_atime=now, st_nlink=2)
    
    def getxattr(self, path, name, position=0):
        return ''
        attrs = self.files[path].get('attrs', {})
        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR
    
    def listxattr(self, path):
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()
    
    def mkdir(self, path, mode):
        self.files[path] = dict(st_mode=(S_IFDIR | mode), st_nlink=2,
                st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time())
        self.files['/']['st_nlink'] += 1
    
    def open(self, path, flags):
        self.fd += 1
        return self.fd
    
    def read(self, path, size, offset, fh):
        return self.data[path][offset:offset + size]
    
    def readdir(self, path, fh):
        files = self.__mega.getFiles()
        parent_remote_id = '0'
        rem_file = '0'
        for p_elem in path.split("/")[1:]:
            if p_elem != "":
                rem_file = None
                for f in files.keys():
                    if files[f]['parent_id'] == parent_remote_id.split("_")[0] and files[f]['name'] == p_elem:
                        parent_remote_id = f
                        rem_file = f
            if rem_file is None:
                break
        rem_files = []
        for f in files.keys():
            if files[f]['parent_id'] == parent_remote_id.split("_")[0]:
                rem_files.append(files[f]['name'])
        return ['.', '..'] + rem_files
    
    def readlink(self, path):
        return self.data[path]
    
    def removexattr(self, path, name):
        attrs = self.files[path].get('attrs', {})
        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR
    
    def rename(self, old, new):
        self.files[new] = self.files.pop(old)
    
    def rmdir(self, path):
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1
    
    def setxattr(self, path, name, value, options, position=0):
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value
    
    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)
    
    def symlink(self, target, source):
        self.files[target] = dict(st_mode=(S_IFLNK | 0777), st_nlink=1,
            st_size=len(source))
        self.data[target] = source
    
    def truncate(self, path, length, fh=None):
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length
    
    def unlink(self, path):
        self.files.pop(path)
    
    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime
    
    def write(self, path, data, offset, fh):
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)


if __name__ == "__main__":
    if len(argv) != 2:
        print 'usage: %s <mountpoint>' % argv[0]
        exit(1)
    fuse = FUSE(Memory(), argv[1], foreground=True)
