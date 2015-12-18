#!/usr/bin/python

print
print "checking for nltk"
try:
    import nltk
except ImportError:
    print "you should install nltk before continuing"

print "checking for numpy"
try:
    import numpy
except ImportError:
    print "you should install numpy before continuing"

print "checking for scipy"
try:
    import scipy
except:
    print "you should install scipy before continuing"

print "checking for sklearn"
try:
    import sklearn
except:
    print "you should install sklearn before continuing"

print
print "Downloading Enron Corpus..."

import os.path
old = 0
def myReportHook(count, blockSize, totalSize):
    global old
    progress = 100. * float(count) * float(blockSize) / float(totalSize)
    progress = int(progress)
    if(progress > old):
        old = progress
        print '\r[{0}] {1}%'.format('#'*(int(progress)/2), progress),

import urllib

fname = "enron_mail_20150507.tgz"
if (os.path.isfile("../" + fname)):
    print "File already exists, skipping download (delete it you don't want me to do this)"
else:
    url = "https://www.cs.cmu.edu/~./enron/" + fname
    urllib.urlretrieve(url, filename="../"+fname, reporthook=myReportHook)
    print "download complete!"

import tarfile
import io
import os

def get_file_progress_file_object_class(on_progress):
    class FileProgressFileObject(tarfile.ExFileObject):
        def read(self, size, *args):
          on_progress(self.name, self.position, self.size)
          return tarfile.ExFileObject.read(self, size, *args)
    return FileProgressFileObject

class TestFileProgressFileObject(tarfile.ExFileObject):
    def read(self, size, *args):
      on_progress(self.name, self.position, self.size)
      return tarfile.ExFileObject.read(self, size, *args)

class ProgressFileObject(io.FileIO):
    def __init__(self, path, *args, **kwargs):
        self._total_size = os.path.getsize(path)
        io.FileIO.__init__(self, path, *args, **kwargs)

    def read(self, size):
        progress = 100. * float(self.tell()) / float(self._total_size)
        print '\r[{0}] {1:.2f}%'.format('#'*(int(progress)/2), progress),
        return io.FileIO.read(self, size)

def on_progress(filename, position, total_size):
    pass

tarfile.TarFile.fileobject = get_file_progress_file_object_class(on_progress)


os.chdir("..")

print "Extracting Enron Corpus: "
tfile = tarfile.open(fileobj=ProgressFileObject(fname))
tfile.extractall()
tfile.close()

print "you're ready to go!"
