#!/usr/bin/env python

import sys
import os
import shutil
from ConfigParser import ConfigParser

def expand_template(source, dest, variables):
    source_str = open(source, 'r').read()
    dest_fh = open(dest, 'w')
    dest_fh.write(source_str % variables)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print>>sys.stderr, "Usage: %s <config-file> <src-dir> <dst-dir>"
        sys.exit(1)

    config = ConfigParser()
    config.read(sys.argv[1])

    source_dir = sys.argv[2]
    dest_dir = sys.argv[3]

    try:
        default_variables = dict(config.items('default'))

    except Exception as ex:
        print>>sys.stderr,"ERROR: %s" % str(ex)
        sys.exit(1)

    try:
        for root, dirs, files in os.walk(source_dir):
            subdir = root.replace(source_dir, "", 1)

            # override the variables if there's a matching subdirectory
            if (config.has_section(subdir)):
                variables = dict(default_variables, **dict(config.items(subdir)))
            else:
                variables = default_variables

            for f in files: 
                dest_file = dest_dir + "/" + subdir + "/" + f
                
                if f.endswith(".xml") or f.endswith(".xml.inc") or f.endswith(".sql"):
                    if not os.path.exists(dest_dir + "/" + subdir):
                        os.makedirs(dest_dir + "/" + subdir)
                    shutil.copyfile(root + "/" + f, dest_file)
                        
                if f.endswith(".xml.template") or f.endswith(".xml.inc.template"):
                    if not os.path.exists(dest_dir + "/" + subdir):
                        os.makedirs(dest_dir + "/" + subdir)
                    expand_template(root + "/" + f, dest_file.replace(".template", ""), variables)

    except KeyError as ex:
        print>>sys.stderr,"ERROR: you're missing this key from the config file: %s" % str(ex)
        sys.exit(1)


