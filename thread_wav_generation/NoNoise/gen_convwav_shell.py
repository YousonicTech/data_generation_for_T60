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

def excel_to_csv(file):
    if file.endswith(".xls"):
        resultsFileName = file.replace(".xls", '.csv')  # "02_06_val_data.csv"
    if file.endswith(".xlsx"):
        resultsFileName = file.replace(".xlsx", '.csv')  # "02_06_val_data.csv"
    resultsFileName = os.path.join(args.output_dir, resultsFileName.split("/")[-1])
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    resultsHandle = open(resultsFileName, "w", newline="")
    csv_writer = csv.writer(resultsHandle)
    headLine = ["Test ID:", "Ver:", "fs:", "Room:", "Room Config:", "Session ID:", "Mic Pos:",
                "Source Pos:", "Config:", "Rec Type:", "RIR:", "Freq band:", "Centre freq:",
                "Channel:", "DRR:", "DRR Mean (Ch):", "T60 AHM:", "T30 ISO:", "T20 ISO:",
                "T60 AHM Mean (Ch):", "T30 ISO Mean (Ch):", "T20 ISO Mean (Ch):", "ISO AHM Ints:", "FB DRR :",
                "FB DRR Mean (Ch):",
                "FB T60 AHM:", "FB T30 ISO:", "FB T20 ISO:", "FB T60 AHM Mean (Ch):", "FB T30 ISO Mean (Ch):",
                "FB T20 ISO Mean (Ch):",
                "DRR direct +:", "DRR direct -:"]
    # headLine = ["Test ID:", "Ver:", "fs:", "Room:",  "Session ID:", "Mic Pos:",
    #             "Source Pos:", "Config:", "Rec Type:", "RIR:", "Freq band:", "Centre freq:",
    #             "Channel:", "DRR:", "DRR Mean (Ch):", "T60 AHM:", "T30 ISO:", "T20 ISO:",
    #             "T60 AHM Mean (Ch):", "T30 ISO Mean (Ch):", "T20 ISO Mean (Ch):", "ISO AHM Ints:", "FB DRR :",
    #             "FB DRR Mean (Ch):",
    #             "FB T60 AHM:", "FB T30 ISO:", "FB T20 ISO:", "FB T60 AHM Mean (Ch):", "FB T30 ISO Mean (Ch):",
    #             "FB T20 ISO Mean (Ch):",
    #             "DRR direct +:", "DRR direct -:"]

    csv_writer.writerow(headLine)

    book = xlrd.open_workbook(file)

    sheet1 = book.sheets()[0]
    # 数据总行数
    nrows = sheet1.nrows
    # 数据总列数
    ncols = sheet1.ncols

    # 获取表中第三行的数据
    x = sheet1.row_values(2)
    # 获取表中第二列的数据
    y = sheet1.col_values(1)
    # 获取第五列中的第二个数据
    z = sheet1.col_values(4)[1]

    test_id = 0
    for i in range(1, nrows):
        values = sheet1.row_values(i)
        room = values[1]
        config = values[0]
        channel = values[4]
        fre_band = 0

        for j in range(len(values)):

            if j < 10:
                continue
            else:
                if j % 5 == 0:
                    info = []
                    # resultsHandle = open(resultsFileName, "a", newline="")
                    # csv_writer = csv.writer(resultsHandle)
                    fre_band += 1
                    test_id += 1
                    t60 = values[j]
                    info.append(test_id)  # 序号
                    info.append(1)
                    info.append(48000)
                    info.append(room)
                    info.append("NAN")
                    info.append(1)
                    info.append(2)
                    info.append(config)
                    info.append("IR")
                    info.append(room)
                    info.append("NAN")
                    info.append(fre_band)  # 表示第几个频段，它没有30个频段，所有应该设置为0
                    info.append(0)  # 中心频段设置为0
                    info.append(channel)
                    info.append(0)
                    info.append(0)
                    info.append(t60)
                    # 下面内容都为0
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    copy_info = info
                    if fre_band == 30:
                        info[15] = 0
                    csv_writer.writerow(info)
            # if j==len(values)-1:
            #      copy_info[10] = copy_info[10] + 1 #中心频率设置为30
            #      copy_info[15] = 0
            #      csv_writer.writerow(copy_info)

    resultsHandle.close()
    return resultsFileName


# def convert_xls2csv(xls_file):
#     return csv
#


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
    csv_file = excel_to_csv(args.xls_file)
    remove_lst = []
    nohup_lst = []
    shell_file = open(args.gen_convwav_shell, 'w')
    for root,dirs,files in os.walk(args.rir_dir):
        for file in files:
            if file.endswith('.wav'):
                wav_file_path = os.path.join(root,file)
                room_name = root.split('/')[-1]
                shell_str = "python main.py --CORPUS_INPUT_FOLDER_ROOT %s --CORPUS_OUTPUT_FOLDER_ROOT %s --T60DRRresultsFile %s  --need_config %s --MIC_CONFIGs %s\n" % (
                    root, args.output_dir, csv_file, room_name, room_name)
                remove_lst.append(shell_str)

    temp_lists = list(set(remove_lst))

    for i in range(len(temp_lists)):
        logdir = args.log
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        log_name = temp_lists[i].split('--MIC_CONFIGs')[-1].split("\n")[0].strip() + '.log'
        log = os.path.join(logdir,log_name)
        nohup_shell =" " + temp_lists[i].split('\n')[0] + " " + "2>&1 | tee %s " % (log) + "\n"
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
    

