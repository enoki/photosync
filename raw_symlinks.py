import sys
import os
import scandir
import subprocess
import getopt
import argparse

parser = argparse.ArgumentParser(description='Create a pictures dir for syncing')
parser.add_argument('-d', '--dry', dest='dryRun', action='store_true')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
parser.add_argument('srcDir', type=str, help='Source directory to get pictures from')
parser.add_argument('dstDir', type=str, help='Destination directory to put symlinks in')
args = parser.parse_args()

dryRun = args.dryRun
verbose = args.verbose

def symlink(src_, dst_):
    src = os.path.normpath(src_)
    dst = os.path.normpath(dst_)

    if sys.platform.startswith('win'):
        subprocess.call(['mklink', dst, src], shell=True)
    else:
        os.symlink(src, dst)

def mklink(srcPath, dstRoot):
    if verbose:
        print '-- mklink(%s,%s)' % (srcPath, dstRoot)
    filename = os.path.basename(srcPath)
    dstPath = '%s/%s' % (dstRoot, filename)
    if verbose:
        print dstPath

    if not os.path.exists(dstPath):
        if dryRun:
            print 'mkdir %s' % os.path.dirname(dstPath)
            print 'mklink %s %s' % (dstPath, srcPath)
        else:
            try:
                os.makedirs(os.path.dirname(dstPath))
            except Exception as e:
                pass
            symlink(srcPath, dstPath)
    else:
        print 'Skipping %s, it already exists (src %s)' % (dstPath, srcPath)

def onError(err):
    print err

srcRoot = args.srcDir
dstRoot = args.dstDir
for root, dirs, files in scandir.walk(srcRoot, onerror=onError):
    for name in files:
        if name[-3:].lower() in ('rw2',):
            mklink(root + '/' + name, dstRoot)
