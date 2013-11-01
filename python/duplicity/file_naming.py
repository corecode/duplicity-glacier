# monkey patch duplicity's file naming for glacier-friendly names

import sys, os

sys.path.remove(os.path.abspath(os.path.join(__file__, '../../')))
sys.modules.pop('duplicity')
sys.modules.pop('duplicity.file_naming')
import duplicity
from duplicity import file_naming

import re
from duplicity import globals

orig_get = file_naming.get
orig_parse = file_naming.parse
def get(type, volume_number = None, manifest = False,
        encrypted = False, gzipped = False, partial = False):
    n = orig_get(type, volume_number, manifest, encrypted, gzipped, partial)
    if not type in ['full-sig', 'new-sig'] and volume_number:
        m = re.search('^(' + globals.file_prefix + ')(?!data-)(.*)', n)
        if m:
            n = m.group(1) + 'data-' + m.group(2)
    return n

def parse(filename):
    # We simply strip away the "data-" prefix that signals difftars
    m = re.search('^(' + globals.file_prefix + ')(?:data-)?(.*)', filename)
    if m:
        filename = "%s%s" % (m.group(1), m.group(2))
    return orig_parse(filename)

file_naming.get = get
file_naming.parse = parse
