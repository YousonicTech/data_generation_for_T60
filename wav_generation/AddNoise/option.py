import argparse

'''
--CORPUS_INPUT_FOLDER_ROOT： rir文件的路径

--CORPUS_OUTPUT_FOLDER_ROOT: 生成数据的路径

--need_config：场景名称

--MIC_CONFIGs：场景名称

备注： need_config 和 MIC_CONFIGs  需要一致 

--noise_dir 噪音文件的路径

--timit_root 干净的人声的路径

--Speaker_txt  干净的人声文件的 txt

'''

parser = argparse.ArgumentParser(description='load these files')
parser.add_argument('--CORPUS_INPUT_FOLDER_ROOT', default='/data1/zdm/T60data/RIR/HYBL_RIR/eight-five', type=str,help='load rir root')
parser.add_argument('--CORPUS_OUTPUT_FOLDER_ROOT', default='/data1/zdm/T60_500Hz_Data_wav/val/hybl_20noise/eight-five', type=str)
parser.add_argument('--T60DRRresultsFile', default='/data1/zdm/T60_500Hz_Data_wav/val/hybl_20noise/hybl_total.csv', type=str)
#为了加速训练，必需按照config分开才行
parser.add_argument('--need_config', default='eight-five', type=str)
parser.add_argument('--MIC_CONFIGs', default="eight-five", type=str)
#parser.add_argument('--MIC_CONFIGs', default="Nature,Miscellaneous,Recreation,Stairwells,Underground,Underpasses,Venues", type=str)

parser.add_argument('--SNR',default=[0,10,20],nargs='+')
parser.add_argument('--noise_dir', default="/data1/zdm/Noise/15NoiseScenes_txt/", type=str)
parser.add_argument('--Speaker_root', default='/data1/zdm/sti_datasets/TIMIT/catTIMIT/', type=str)
parser.add_argument('--Speaker_txt', default='/data1/zdm/sti_datasets/TIMIT/catTIMIT.txt', type=str)
args = parser.parse_args()

