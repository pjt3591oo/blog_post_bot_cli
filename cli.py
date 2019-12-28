#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "JeongTae Park"
__copyright__ = "Copyright 2019, First Last"
__version__ = "1.0.0"
__maintainer__ = "JeongTae Park"
__email__ = "pjt3591oo@gmail.com"
__status__ = "development"

from logzero import logger
import argparse
from controller import Controller

def show_args(args):
    msg = "arg=%s, file_path=%s, account_set=%s, resource_dir=%s, verbose=%s, web_driver=%s"%(
        kwargs.arg,
        kwargs.file_path,
        kwargs.account_set,
        kwargs.resource_dir,
        kwargs.verbose,
        kwargs.web_driver
    )
    logger.info(msg)
    
    controller = Controller(kwargs.file_path, kwargs.account_set, kwargs.web_driver, kwargs.resource_dir, debug=True)
    controller()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("arg", help="Required positional argument")

    PARSER.add_argument("-a", "--account-set", action="store")   # 계정정보 파일

    PARSER.add_argument("-w", "--web-driver", action="store")    # 크롬 드라이버 경로
    PARSER.add_argument("-f", "--file-path", action="store")     # 파일 경로
    PARSER.add_argument("-r", "--resource-dir", action="store") # 리소스 파일 경로

    PARSER.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    PARSER.add_argument(
        "--version",
        action="version",
        version="{prog} (version {version})".format(prog="BLOG POSTING BOT", version=__version__))

    kwargs = PARSER.parse_args()

    show_args(kwargs)