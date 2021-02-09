# Copyright (c) 2021 Jisang Yoon
# All rights reserved.
#
# This source code is licensed under the Apache 2.0 license found in the
# LICENSE file in the root directory of this source tree.

# pylint: disable=no-name-in-module,logging-format-truncated
import os
import subprocess
import fire

from gensim import downloader as api
from cusim import aux, IoUtils, CuLDA

LOGGER = aux.get_logger()
DOWNLOAD_PATH = "./res"
# DATASET = "wiki-english-20171001"
DATASET = "fake-news"
DATA_PATH = f"./res/{DATASET}.stream.txt"
DATA_PATH2 = f"./res/{DATASET}-converted"
MIN_COUNT = 5

def download():
  if os.path.exists(DATA_PATH):
    LOGGER.info("%s already exists", DATA_PATH)
    return
  api.BASE_DIR = DOWNLOAD_PATH
  filepath = api.load(DATASET, return_path=True)
  LOGGER.info("filepath: %s", filepath)
  cmd = ["gunzip", "-c", filepath, ">", DATA_PATH]
  cmd = " ".join(cmd)
  LOGGER.info("cmd: %s", cmd)
  subprocess.call(cmd, shell=True)

def run_io():
  download()
  iou = IoUtils(opt={"chunk_lines": 10000, "num_threads": 8})
  iou.convert_stream_to_h5(DATA_PATH, 5, DATA_PATH2)


def run_lda():
  opt = {
    "data_dir": DATA_PATH2,
  }
  lda = CuLDA(opt)
  lda.init_model()


if __name__ == "__main__":
  fire.Fire()
