import time

def wait_seconds_hzs(seconds):
    time.sleep(seconds)

def start_timer_hzs():
    return time.time()

def get_elapsed_hzs(start_time):
    return round(time.time() - start_time, 2)