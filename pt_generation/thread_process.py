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
def execCmd(cmd):
    try:
        print("COMMAND -- %s -- BEGINS -- %s -- " % (cmd, datetime.datetime.now()))
        os.system(cmd)
        print("COMMAND -- %s -- ENDS -- %s -- " % (cmd, datetime.datetime.now()))
    except:
        print("Failed -- %s -- " % cmd)


# 如果只是路径变了的话，就改这3个地方
# Don't forget the last '/' in those paths!!!!
# Carefully check!!!

wav_root = "/data1/zdm/T60_500HZ_Data_wav/val/hybl/"  #
save_pt_root = "/data1/zdm/T60_500Hz_Data_pt/NoNoise/T60_500Hz_nonoise_val_pt/hybl/"
csv_path_root = "/data1/zdm/T60_500HZ_Data_wav/val/hybl/"  # 新传上去了

wav_list = []
save_list = []
csv_list = []

for folder_name in os.listdir(wav_root):
    if os.path.isdir(os.path.join(wav_root,folder_name)):
        wav_list.append(os.path.join(wav_root,folder_name))
        save_list.append(os.path.join(save_pt_root,folder_name))
        csv_list.append(os.path.join(csv_path_root,folder_name,"results.csv"))

if __name__ == "__main__":
    commands = ["python OurData_GenPT.py --dir_str " + wav_list[i] + " --save_dir " + save_list[i] + " --csv_file " + csv_list[i] for i in range(len(wav_list))]
    threads = []
    for cmd in commands:
        th = threading.Thread(target=execCmd, args=(cmd,))
        th.start()
        threads.append(th)
    # 等待线程运行完毕
    for th in threads:
        th.join()

