""" Modified version of build_ext that handles fortran source files.
"""

import os, string
from types import *

from distutils.dep_util import newer_group, newer
from distutils.command.build_ext import *
from distutils.command.build_ext import build_ext as old_build_ext

class build_ext (old_build_ext):
            
    def run (self):
        if self.distribution.has_f_libraries():
            build_flib = self.get_finalized_command('build_flib')
            self.libraries.extend(build_flib.get_library_names() or [])
            self.library_dirs.extend(build_flib.get_library_dirs() or [])
            #self.library_dirs.extend(build_flib.get_library_dirs() or [])
            #runtime_dirs = build_flib.get_runtime_library_dirs()
            #self.runtime_library_dirs.extend(runtime_dirs or [])
            
            #?? what is this ??
            self.library_dirs.append(build_flib.build_flib)
            
        old_build_ext.run(self)

    def build_extension(self, ext):
        # support for building static fortran libraries
        if self.distribution.has_f_libraries():
            build_flib = self.get_finalized_command('build_flib')
            moreargs = build_flib.fcompiler.get_extra_link_args()
            if moreargs != []:                
                if ext.extra_link_args is None:
                    ext.extra_link_args = moreargs
                else:
                    ext.extra_link_args += moreargs
            # be sure to include fortran runtime library directory names
            runtime_dirs = build_flib.get_runtime_library_dirs()
            ext.runtime_library_dirs.extend(runtime_dirs or [])
            linker_so = build_flib.fcompiler.get_linker_so()
            if linker_so is not None:
                self.compiler.linker_so = linker_so
        # end of fortran source support
        return old_build_ext.build_extension(self,ext)

    def get_source_files (self):
        self.check_extensions_list(self.extensions)
        filenames = []

        # Get sources and any include files in the same directory.
        for ext in self.extensions:
            filenames.extend(ext.sources)
            filenames.extend(get_headers(get_directories(ext.sources)))

        return filenames
