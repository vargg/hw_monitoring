from datetime import datetime

import GPUtil
import psutil

DATE_FORMAT = '%m:%d:%H:%M:%S'


def get_current_date():
    return datetime.now().strftime(DATE_FORMAT)


def get_current_cpu_usage():
    return psutil.cpu_percent(interval=0.1)


def get_current_gpu_usage():
    try:
        gpu = GPUtil.getGPUs()[0]
    except IndexError:
        return None
    return round(100 * gpu.memoryFree / gpu.memoryTotal, 1)


def get_current_memory_usage():
    total_memory = psutil.virtual_memory().total
    used_memory = total_memory - psutil.virtual_memory().available

    return round(100 * used_memory / total_memory, 1)
