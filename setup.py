# simpleaudiohamiltoncs Python Extension
# Copyright (C) 2015, Joe Hamilton
# MIT License (see LICENSE.txt)

from setuptools import setup, Extension
import sys
from os import path

platform_sources = []
platform_libs = []
platform_link_args = []
platform_compile_args = []

if sys.platform == 'darwin':
    platform_sources = ['c_src/simpleaudiohamiltoncs_mac.c', 'c_src/posix_mutex.c']
    platform_link_args = ['-framework', 'AudioToolbox']
    platform_compile_args = ['-mmacosx-version-min=10.6']
elif sys.platform.startswith("linux"):
    platform_sources = ['c_src/simpleaudiohamiltoncs_alsa.c', 'c_src/posix_mutex.c']
    platform_libs = ['asound']
elif sys.platform == 'win32':
    platform_sources = ['c_src/simpleaudiohamiltoncs_win.c', 'c_src/windows_mutex.c']
    platform_libs = ['Winmm', 'User32']
else:
    pass
    # define a compiler macro for unsupported ?

simpleaudiohamiltoncs_c_ext = Extension(
    'simpleaudiohamiltoncs._simpleaudiohamiltoncs',
    sources=platform_sources + ['c_src/simpleaudiohamiltoncs.c'],
    libraries=platform_libs,
    extra_compile_args=platform_compile_args,
    extra_link_args=platform_link_args,
    define_macros=[('DEBUG', '0')])

# attempt to generate the version from git tag and commit

VERSION = "1.0.8"

# Get the long description from the relevant file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'),
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='simpleaudiohamiltoncs',
    version=VERSION,
    license='MIT',
    description="Simple, asynchronous audio playback for Python 3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Joe Hamilton',
    author_email='jhamilton10@georgefox.edu',
    url='https://github.com/hamiltron/py-simple-audio',
    keywords=['audio', 'wave', 'media', 'multimedia',
              'sound', 'alsa', 'coreaudio', 'winmm', 'music'],
    classifiers=['Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11',
                 'Programming Language :: Python :: 3.12',
                 'Topic :: Multimedia :: Sound/Audio',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: MacOS :: MacOS X'],
    py_modules=["simpleaudiohamiltoncs.shiny", "simpleaudiohamiltoncs.functionchecks"],
    ext_modules=[simpleaudiohamiltoncs_c_ext],
    packages=['simpleaudiohamiltoncs'],
    package_dir={'simpleaudiohamiltoncs': 'simpleaudiohamiltoncs'},
    package_data={'simpleaudiohamiltoncs': ['test_audio/c.wav', 'test_audio/e.wav',
                                  'test_audio/g.wav',
                                  'test_audio/left_right.wav',
                                  'test_audio/notes_2_16_44.wav']},)
