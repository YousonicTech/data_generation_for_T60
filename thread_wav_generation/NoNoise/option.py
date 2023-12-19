import argparse


parser = argparse.ArgumentParser(description="load these files")
# 需要修改
parser.add_argument("--xls_file", default="/data1/zdm/RIR/250/ZGC_250_RIR_bu/ZGC_250_RIR_bu.xls", type=str)
parser.add_argument('--rir_dir', default="/data1/zdm/RIR/250/ZGCFX_250_RIR_bu/", type=str)
parser.add_argument("--output_dir", default="/data1/zdm/clap/wav/with_direct/250/NoNoise/ZGCFX_250", type=str)
parser.add_argument('--speaker_choose_num',default=None) # default=None，全部选择

# 扰动
parser.add_argument('--time_disturb',default=False) # default=False 用于设置rir与speech卷积时是否将rir在时间上进行扰动
parser.add_argument('--time_disturb_percent',default=0.3) # default=False 用于设置rir与speech卷积将rir在时间上进行扰动的百分比
parser.add_argument('--time_disturb_amplitude_percent',default=0.3) # default=False 用于设置rir与speech卷积将rir在时间上进行扰动的幅值变化
parser.add_argument('--time_disturb_window_len',default=16000) # 窗口长度，以采样点为单位

# 直达声切除
parser.add_argument('--cut_direct',default=False) # 是否切除直达声

#可以配置
parser.add_argument("--gen_convwav_shell", default='./test.sh', type=str)
parser.add_argument("--log",default="./log/",type=str)

# 配置一次即可
parser.add_argument("--speaker_root", default="/data1/zdm/clap/clap_data/clap_cut_with_direct/", type=str)
parser.add_argument("--speaker_txt", default="/data1/zdm/clap/clap.txt", type=str)

# 无需修改，自动生成
parser.add_argument("--CORPUS_INPUT_FOLDER_ROOT",default="/data1/zdm/T60data/RIR/ZGCFX_RIR/ZGCFX-4-7 ",type=str,help="load rir root")
parser.add_argument("--CORPUS_OUTPUT_FOLDER_ROOT",default="/data1/zdm/code/test/ZGCFX_NoNoise/",type=str)
parser.add_argument("--T60DRRresultsFile",default="/data1/zdm/code/test/ZGCFX_NoNoise/ZGCFX_total.csv",type=str)
# 为了加速训练，必需按照config分开才行
parser.add_argument("--need_config", default="ZGCFX-4-7", type=str)
parser.add_argument("--MIC_CONFIGs", default="ZGCFX-4-7", type=str) # xls中的Mic config


args = parser.parse_args()
