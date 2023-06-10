# -*- coding: utf-8 -*-
"""
@file      :  1130_thread_gen.py
@Time      :  2022/11/30 18:48
@Software  :  PyCharm
@summary   :
@Author    :  Bajian Xiang
"""

# nohup python thread_process.py  >> /data2/hsl/thread_0323_gen_data.log 2>&1 &

import datetime
import os
import threading

MAX_THREADS = 4  # 设置最大的并行线程数为 4
wav_root = "/data1/zdm/T60data/val_LiveRecord/HYBL_LiveRecord/"
save_pt_root = "/data1/zdm/T60_500Hz_Data_pt/LiveRecord/val_hybl_LiveRecord/"
csv_path = "/data1/zdm/T60_500HZ_Data_wav/val/hybl/hybl_total.csv"  # 新传上去了
semaphore = threading.Semaphore(MAX_THREADS)
def execCmd(cmd):
    try:
        semaphore.acquire()  # 获取 semaphore
        print("COMMAND -- %s -- BEGINS -- %s -- " % (cmd, datetime.datetime.now()))
        os.system(cmd)
        print("COMMAND -- %s -- ENDS -- %s -- " % (cmd, datetime.datetime.now()))
    except:
        print("Failed -- %s -- " % cmd)
    finally:
        semaphore.release()  # 释放 semaphore


# 如果只是路径变了的话，就改这3个地方
# Don't forget the last '/' in those paths!!!!
# Carefully check!!!


wav_list = []
save_list = []

for folder_name in os.listdir(wav_root):
    if os.path.isdir(os.path.join(wav_root,folder_name)):
        wav_list.append(os.path.join(wav_root,folder_name))
        save_list.append(os.path.join(save_pt_root,folder_name))

if __name__ == "__main__":
    commands = ["python OurData_GenPT.py --dir_str " + wav_list[i] + " --save_dir " + save_list[i] + " --csv_file " + csv_path for i in range(len(wav_list))]
    threads = []
    for cmd in commands:
        th = threading.Thread(target=execCmd, args=(cmd,))
        th.start()
        threads.append(th)
    # 等待线程运行完毕
    for th in threads:
        th.join()

