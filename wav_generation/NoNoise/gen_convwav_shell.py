import os
import csv
import argparse
import shutil
import xlrd

import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("--xls_file", default="/data1/zdm/code/gen_test/HYBL_test_RIR/hybl_total.xls", type=str)
parser.add_argument('--rir_dir', default="/data1/zdm/code/gen_test/HYBL_test_RIR/", type=str)
parser.add_argument("--output_dir", default="/data1/zdm/code/gen_test/Output/", type=str)
parser.add_argument("--gen_convwav_shell", default='/data1/zdm/code/gen_test/sh/test.sh', type=str)

# 创建解析器
# ArgumentParser 对象包含将命令行解析成 Python 数据类型所需的全部信息。
# path = r"C:\Users\17579\Desktop\新建文件夹\TAE_Train\Data_Aug\Step_1\test_1.csv"

def excel_to_csv(file):
    resultsFileName = file.replace(".xls", '.csv')  # "02_06_val_data.csv"
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

if __name__ == "__main__":
    args = parser.parse_args()
    # xls_file = args.xls_file
    # file = "./new_val_data.xls"
    # csv_file = args.csv_file
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
    for x in remove_lst:
        print(x)

    temp_lists = list(set(remove_lst))
    for i in range(len(temp_lists)):
        log_name = temp_lists[i].split('--MIC_CONFIGs')[-1].split("\n")[0].strip() + '.log'
        nohup_shell = "nohup" + " " + temp_lists[i].split('\n')[0] + " " + ">%s 2>&1 &" % (log_name) + "\n"
        nohup_lst.append(nohup_shell)


    for i in nohup_lst:
        shell_file.write(i)
    shell_file.close()
    print('finished!!!')
