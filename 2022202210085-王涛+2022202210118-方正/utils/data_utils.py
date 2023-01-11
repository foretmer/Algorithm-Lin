from Common import *
import os
from random import random
from typing import List,Tuple

from Bin import Bin
from Container import Container
import utils.log_utils

LOGGER = utils.log_utils.SingleLogger().get_logger()

def generate_bins(bin_num:int, container:Container) -> List[Bin]:
    bin_list = []
    for idx in range(bin_num):
        l = container.ml * random() / 4 + 10 ** (-container.precision)
        h = container.mh * random() / 4 + 10 ** (-container.precision)
        w = container.mw * random() / 4 + 10 ** (-container.precision)
        new_bin = Bin(l, h, w, container.precision)
        bin_list.append(new_bin)
    LOGGER.info("{} bin(s) generated.".format(bin_num))
    return bin_list
    
def read_task(read_path:str, bin_types:int, pick_num:int=None, precision:int=PRECISION) -> Tuple[Container, List[Bin]]:
    bins_list = []
    abs_path = os.path.abspath(read_path)
    if not os.path.exists(abs_path):
        LOGGER.critical("Task File does not exist!")
    LOGGER.info(f'Read from: "{abs_path}"')
    read_file = open(abs_path, "r", encoding = 'utf-8')
    lines = read_file.readlines()
    lines = [line.strip() for line in lines]
    lines = ["" if line.startswith("/") else line for line in lines]
    lines = ["" if line.startswith("\n") else line for line in lines]
    valid_lines = []
    for line in lines:
        if line != "":
            valid_lines.append(line)
    container_list = []
    bins_list = []
    types_list = []
    for line in valid_lines:
        if line.startswith("C"):
            ml, mw, mh = line.split("(")[1].split(")")[0].split(" ")
            ml, mw, mh = int(ml), int(mw), int(mh)
            new_container = Container(ml, mw, mh, precision)
            container_list.append(new_container)
        elif line.startswith("B"):
            str_bins = line.split("[")[1].split("]")[0].split(",")
            str_bins = [str_bin.strip() for str_bin in str_bins]
            bin_type = len(str_bins)
            bin_list = []
            for str_bin in str_bins:
                l, w, h, n = str_bin.split("(")[1].split(")")[0].split(" ")
                l, w, h, n = int(l), int(w), int(h), int(n)
                for i in range(n):
                    new_bin = Bin(l, w, h, precision)
                    bin_list.append(new_bin)
            bins_list.append(bin_list)
            types_list.append(bin_type)
    assert len(container_list) == len(bins_list)
    valid_idies = []
    for idx, (container, bins, bin_type) in enumerate(zip(container_list, bins_list, types_list)):
        if bin_type == bin_types:
            valid_idies.append(idx)
    random_choice = int(random() * len(valid_idies)) if ((pick_num == None) or (pick_num == 0)) else pick_num - 1
    valid_idx = valid_idies[random_choice]
    LOGGER.info(f"{len(container_list)} task(s) in total, {len(valid_idies)} valid task(s), {valid_idx+1}nd/{random_choice+1}nd picked.")
    return container_list[valid_idx], bins_list[valid_idx]
            