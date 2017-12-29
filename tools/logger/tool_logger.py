# encoding:utf-8
import logging
import os

logger_name = "tool_logger"
tool_logger = logging.getLogger(logger_name)
tool_logger.setLevel(logging.INFO)

log_path = "./log/limit.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

fmt = "[Date: %(asctime)-15s][Level: %(levelname)s] %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

fh.setFormatter(formatter)
tool_logger.addHandler(fh)
