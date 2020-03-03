# coding=utf-8
"""
@Time   : 2020/3/3  22:22 
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@scishang.com hjgao@std.uestc.edu.cn
@Sketch : 
"""

import logging
from utils.config import LOG_LEVEL

logger = logging.getLogger("TAROT LOG")
level = logging.getLevelName(LOG_LEVEL)
logger.setLevel(level)
fmt = "TAROT LOG: %(asctime)s [%(levelname)s] %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(format=fmt, datefmt=date_fmt)

if __name__ == '__main__':
    logger.info("Log configured successfully!")
