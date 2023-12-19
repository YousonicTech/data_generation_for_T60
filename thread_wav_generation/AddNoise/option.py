import argparse


parser = argparse.ArgumentParser(description='load these files')
# 需要修改
parser.add_argument("--xls_file", default="/data1/zdm/RIR/1K/HYBL_1K_RIR_bu/HYBL_1K_RIR_bu.xls", type=str)
parser.add_argument('--rir_dir', default="/data1/zdm/RIR/1K/HYBL_1K_RIR_bu/", type=str)
parser.add_argument("--output_dir", default="/data1/zdm/clap/wav/with_direct/1K/AddNoise/30Noise/HYBL_1K", type=str)
parser.add_argument('--SNR',default=[30],nargs='+')
parser.add_argument('--noise_choose_num',default=None) # default=None，全部选择
parser.add_argument('--speaker_choose_num',default=None) # default=None，全部选择

# 扰动
parser.add_argument('--time_disturb',default=False) # default=False 用于设置rir与speech卷积时是否将rir在时间上进行扰动
parser.add_argument('--time_disturb_percent',default=0.2) # default=False 用于设置rir与speech卷积将rir在时间上进行扰动的百分比
parser.add_argument('--time_disturb_amplitude_percent',default=0.2) # default=False 用于设置rir与speech卷积将rir在时间上进行扰动的幅值变化
parser.add_argument('--time_disturb_window_len',default=16000) # 窗口长度，以采样点为单位

# 直达声切除
parser.add_argument('--cut_direct',default=False) # 是否切除直达声

# 配置一次即可
parser.add_argument('--noise_dir', default="/data1/zdm/Noise/15NoiseScenes_txt/", type=str)
parser.add_argument('--speaker_root', default='/data1/zdm/clap/clap_data/clap_cut_with_direct/', type=str)
parser.add_argument('--speaker_txt', default='/data1/zdm/clap/clap.txt', type=str)

# 可以配置
parser.add_argument("--spl_window", default=1, type=str)
parser.add_argument("--shell_path", default='./test.sh', type=str)
parser.add_argument("--log",default="./log/",type=str)

# 无需修改，自动生成
parser.add_argument('--CORPUS_INPUT_FOLDER_ROOT', default='/data1/zdm/T60data/RIR/HYBL_RIR/eight-five/', type=str,help='load rir root')
parser.add_argument('--CORPUS_OUTPUT_FOLDER_ROOT', default='/data1/zdm/test/', type=str) # output_dir
parser.add_argument('--T60DRRresultsFile', default='/data1/zdm/test/HYBL_total.csv', type=str) # output_dir + xxx.csv
#为了加速训练，必需按照config分开才行
parser.add_argument('--need_config', default='eight-five', type=str)
parser.add_argument('--MIC_CONFIGs', default="eight-five", type=str) # xls中的Mic config
#parser.add_argument('--MIC_CONFIGs', default="Nature,Miscellaneous,Recreation,Stairwells,Underground,Underpasses,Venues", type=str)

args = parser.parse_args()

