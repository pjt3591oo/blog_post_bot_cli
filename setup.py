import os
import sys

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

script = (sys.platform == "win32" and "lib\\bpb.py" or "bin/bpb")
setup(
    name="bpb",
    version=1.0,
    maintainer="Mung",
    maintainer_email="pjt3591oo@gmail.com",
    author="Mung",
    author_email="pjt3591oo@gmail.com",
    url="https://github.com/pjt3591oo/blog_post_bot_cli",
    license="MIT",
    platforms=["any"],
    install_requires = [ "selenium", "bs4", "lxml", "markdown2", "logger"],
    scripts=['bpb/bpb.py'],
    entry_points={
        'console_scripts': [
          'bpb = bpb:execute'
        ]
    },
    packages=find_packages(),
    description="Naver Blog Auto Posting Bot From Read Markdown File  ",
    classifiers      = [
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6'
    ],
    long_description_content_type = "text/markdown",
    long_description = long_description,
)