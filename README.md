# 数据生成

## 工程结构

```
T60_data_generation
├── pt_generation
└── wav_generation
    ├── AddNoise
    └── NoNoise
```

## 命名规范

注意：所有文件及文件夹名中请勿出现字符"_"，如要使用请用字符"-"替换，或采用驼峰命名法

RIR文件目录格式如下

```
RIR
├── YanQiHu
│   ├── room1
│   │   ├── room1-ch1.wav
│   │   └── room1-ch2.wav
│   └── room2
│   │   ├── room1-ch1.wav
│   │   └── room1-ch2.wav
├── HYBL
│   ├── room1
│   │   ├── room1-ch1.wav
│   │   └── room1-ch2.wav
└── └── room2
        ├── room1-ch1.wav
        └── room1-ch2.wav
```

## 不含噪数据生成

### 1. 生成wav文件

对应`wav_generation/NoNoise`

1.1 修改`gen_convwav_shell.py`的参数：
xls_file：RIR对应的xls文件
rir_dir：RIR路径地址
output_dir：wav文件输出路径
gen_convwav_shell：生成的sh文件
如要修改干语料，修改option.py下的参数：
Speaker_root：干语料路径
Speaker_txt：干语料txt
1.2 运行`python gen_convwav_shell.py`，会在output_dir下生成csv文件
1.3 随后运行生成的sh文件（即1.1中的参数gen_convwav_shell），会在output_dir文件夹下生成RIR\*speech的wav文件Dev/Speech/{room}/*.wav

生成的WAV文件命名如下：
{room}\_{wav_name}\_{speech}_N_NdB.wav
  room为房间名，如room1，room2
  rir_wav_name为具体的wav文件名，如room1-ch1、 room1-ch2
  speech为干语料

### 2. 生成pt文件

**！！！pt文件包含的t60为30维！！！**

对应`pt_generation`

修改**`thread_process.py`** 28-30行的参数
  dir_str_head：第1步生成的{output_dir}/Dev/Speech/
  ave_dir_head：要保存的pt文件路径
  csv_path_head：第1步生成的{output_dir}/Dev/Speech/

修改
  dir_str、save_dir+各个房间
  csv_dir+各个房间+路径下的csv文件

例子：

```
# thread_process.py
dir_str_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_wav/Dev/Speech/"

save_dir_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_pt/"

csv_path_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_wav/Dev/Speech/" 

dir_str = [ 
	dir_str_head + "eight-four",
]

save_dir = [
 save_dir_head + "eight-four",
]


csv_dir = [
	csv_path_head + "eight-four"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
]
```

生成的pt文件格式与wav一致

## 含噪数据生成

### 生成wav文件

对应`wav_generation/AddNoise`

1.1 修改`gen_convwav_shell.py`的参数：
&emsp;xls_file：RIR对应的xls文件
  rir_dir：RIR路径地址
  output_dir：wav文件输出路径
  gen_convwav_shell：生成的sh文件
  如要**修改干语料**，修改option.py下的参数：
  Speaker_root：干语料路径
  Speaker_txt：干语料txt
  如要**修改噪音**，修改option.py下的参数：
  noise_dir：noise的txt目录
1.2 运行`python gen_convwav_shell.py`，会在output_dir下生成csv文件，生成sh文件
1.3 随后运行生成的sh文件（即1.1中的参数gen_convwav_shell），会在output_dir文件夹下生成RIR\*speech的wav文件Dev/Speech/{room}/*.wav

生成的WAV文件命名如下：

{room}\_{wav_name}\_{speech}\_{noise}_{SNR}dB.wav
room：房间名，如room1，room2
rir_wav_name：具体的wav文件名，如room1-ch1、 room1-ch2
speech：干语料
noise：噪音
SNR：信噪比

### 生成pt文件

**！！！pt文件包含的t60为30维！！！**

对应`pt_generation`

修改**`thread_process.py`** 28-30行的参数
dir_str_head：第1步生成的{output_dir}/Dev/Speech/
save_dir_head：要保存的pt文件路径

​	csv_path_head：第1步生成的{output_dir}/Dev/Speech/

修改

​	dir_str、save_dir+各个房间

​	csv_dir+各个房间+路径下的csv文件

例子：

```
dir_str_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_wav/Dev/Speech/"

save_dir_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_pt/"

csv_path_head = "/data1/zdm/code/hybl_T60_experiment/chinese_cat_HYBL_wav/Dev/Speech/" 

dir_str = [ 
	dir_str_head + "eight-four",
]

save_dir = [
 save_dir_head + "eight-four",
]


csv_dir = [
	csv_path_head + "eight-four"+"/20230527T093347_test_gen_corpus_dataset_results.csv",
]
```

生成的pt文件格式与wav一致

