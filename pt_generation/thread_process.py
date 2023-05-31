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

dir_str_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_wav/Dev/Speech/"  #
save_dir_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_pt/"
csv_path_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_wav/Dev/Speech/"  # 新传上去了

dir_str = [ 
            dir_str_head + "eight-four",
            dir_str_head + "eight-two",
            dir_str_head + "five-eleven",
            dir_str_head + "five-one",
            dir_str_head + "five-twelve",
            dir_str_head + "five-two",
            dir_str_head + "six-eight",
            dir_str_head + "six-one",
            dir_str_head + "z-3",
            dir_str_head + "z-4",
            dir_str_head + "z-5"
        ]

save_dir = [
            save_dir_head + "eight-four",
            save_dir_head + "eight-two",
            save_dir_head + "five-eleven",
            save_dir_head + "five-one",
            save_dir_head + "five-twelve",
            save_dir_head + "five-two",
            save_dir_head + "six-eight",
            save_dir_head + "six-one",
            save_dir_head + "z-3",
            save_dir_head + "z-4",
            save_dir_head + "z-5"
            
            ]

csv_dir = [
            
            csv_path_head + "eight-four"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "eight-two"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "five-eleven"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "five-one"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "five-twelve"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "five-two"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "six-eight"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "six-one"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "z-3"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "z-4"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
            csv_path_head + "z-5"+"/20230530T184512_results.csv",
        
        ]
if __name__ == "__main__":
    commands = ["python OurData_GenPT.py --dir_str " + dir_str[i] + " --save_dir " + save_dir[i] + " --csv_file " + csv_dir[i] for i in range(len(dir_str))]
    threads = []
    for cmd in commands:
        th = threading.Thread(target=execCmd, args=(cmd,))
        th.start()
        threads.append(th)
    # 等待线程运行完毕
    for th in threads:
        th.join()

