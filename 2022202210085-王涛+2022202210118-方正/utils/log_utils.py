import os
import sys
import time
import logging
import verboselogs

def singleton(cls):
    _instance = {}
 
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)  # 创建一个对象,并保存到字典当中
        return _instance[cls]
 
    return _singleton

@singleton
class SingleLogger():

    run_repr = None
    log_file_path = None
    logger = None   

    def get_repr(self, task_args=None, type_args=None, method_args=None):
        if self.run_repr is None:
            time_str = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())
            repr = f"{task_args.bin_types}_{task_args.test_index}_{type_args.type}_{method_args.method}_{time_str}"
            self.run_repr = repr
        return self.run_repr

    def get_log_path(self, LOG_DIR, task_args, type_args, method_args, config_args):
        file_name = self.get_repr(task_args, type_args, method_args) + ".log"
        self.log_file_path = os.path.join(LOG_DIR,file_name) 

    def get_logger(self):
        if self.logger is not None:
            return self.logger
        logger = verboselogs.VerboseLogger("3DBP")
        logger.setLevel(logging.DEBUG)

        streamFormatter = logging.Formatter(fmt="({filename}:{lineno}) {levelname}: {message}",style="{")
        fileFormatter = logging.Formatter(fmt='[{asctime}] File "{filename}", line {lineno}, in {funcName}\n{levelname}: {message}',style="{")

        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(streamFormatter)

        fileHandler = logging.FileHandler(self.log_file_path, "w")
        fileHandler.setLevel(logging.VERBOSE)
        fileHandler.setFormatter(fileFormatter)

        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)

        self.logger = logger
        return self.logger
