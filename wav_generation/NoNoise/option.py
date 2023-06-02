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
parser.add_argument('--CORPUS_INPUT_FOLDER_ROOT', default='/data1/zdm/code/hybl_T60_experiment/HYBL_test_RIR/six-eight', type=str,help='load rir root')
parser.add_argument('--CORPUS_OUTPUT_FOLDER_ROOT', default='/data1/zdm/code/T60_data_generation/test/RIR', type=str)
parser.add_argument('--T60DRRresultsFile', default='/data1/zdm/code/T60_data_generation/test/RIR/hybl_total.csv', type=str)
#为了加速训练，必需按照config分开才行
parser.add_argument('--need_config', default='six-eight', type=str)
parser.add_argument('--MIC_CONFIGs', default="six-eight", type=str)
#parser.add_argument('--MIC_CONFIGs', default="Nature,Miscellaneous,Recreation,Stairwells,Underground,Underpasses,Venues", type=str)
#parser.add_argument('--noise_dir', default="/data1/zdm/code/T60_experiment/15NoiseScenes_txt/15NoiseScenes_txt", type=str)

parser.add_argument('--Speaker_root', default='/data1/zdm/code/gen_test/CatChinese', type=str)
parser.add_argument('--Speaker_txt', default='/data1/zdm/code/gen_test/CatChinese/CatChinese.txt', type=str)
args = parser.parse_args()


