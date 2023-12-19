"""不生成CSV文件，只生成wav文件"""

import os
import csv
import xlrd
from option import args
import random
import threading
import datetime
# 创建解析器
# ArgumentParser 对象包含将命令行解析成 Python 数据类型所需的全部信息。
# path = r"C:\Users\17579\Desktop\新建文件夹\TAE_Train\Data_Aug\Step_1\test_1.csv"

def execCmd(cmd):
    try:
        semaphore.acquire()  # 获取 semaphore
        print("COMMAND -- %s -- BEGINS -- %s -- " % (cmd, datetime.datetime.now()))
        os.system(cmd)
        # os.system(cmd)
        print("COMMAND -- %s -- ENDS -- %s -- " % (cmd, datetime.datetime.now()))
    except:
        print("Failed -- %s -- " % cmd)
    finally:
        semaphore.release()  # 释放 semaphore
        
if __name__ == "__main__":
    MAX_THREADS = 4  # 设置最大的并行线程数
    semaphore = threading.Semaphore(MAX_THREADS)
    random.seed(1234)
    remove_lst = []
    nohup_lst = []
    shell_file = open(args.gen_convwav_shell, 'w')
    for root,dirs,files in os.walk(args.rir_dir):
        for file in files:
            if file.endswith('.wav'):
                wav_file_path = os.path.join(root,file)
                room_name = root.split('/')[-1]
                shell_str = "python main_only_conv.py --CORPUS_INPUT_FOLDER_ROOT %s --CORPUS_OUTPUT_FOLDER_ROOT %s  --need_config %s --MIC_CONFIGs %s\n" % (
                    root, args.output_dir, room_name, room_name)
                remove_lst.append(shell_str)
        
    
        
    temp_lists = list(set(remove_lst))
    for x in temp_lists:
        print(x)
    for i in range(len(temp_lists)):
        logdir = args.log
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        log_name = temp_lists[i].split('--MIC_CONFIGs')[-1].split("\n")[0].strip() + '.log'
        log = os.path.join(logdir,log_name)
        nohup_shell =" " + temp_lists[i].split('\n')[0] + " " + ">%s " % (log) + "\n"
        nohup_lst.append(nohup_shell)

    for i in nohup_lst:
        shell_file.write(i)
    shell_file.close()
    
    temp_lists = list(set(remove_lst))
    threads = []
    for cmd in nohup_lst:
        th = threading.Thread(target=execCmd, args=(cmd,))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    
    print('finished!!!')
    

