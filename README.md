# 数据生成

## 更新日志
2023-6-2 优化log日志记录，优化pt生成


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

1.1 修改**`gen_convwav_shell.py`**的参数：

&emsp;&emsp; xls_file：RIR对应的xls文件

&emsp;&emsp; rir_dir：RIR路径地址

&emsp;&emsp; output_dir：wav文件输出路径

&emsp;&emsp; gen_convwav_shell：生成的sh文件

&emsp;&emsp; log：使用nohup进行后台运行的log记录路径，默认为"./log"

&emsp;如要修改干语料，修改option.py下的参数：

&emsp;&emsp; Speaker_root：干语料路径

&emsp;&emsp; Speaker_txt：干语料txt

1.2 运行`python gen_convwav_shell.py`，会在output_dir下生成csv文件，并生成sh文件

1.3 随后运行生成的sh文件（即1.1中的参数gen_convwav_shell），会在output_dir文件夹下生成RIR\*speech的wav文件Dev/Speech/{room}/*.wav



&emsp;生成的WAV文件命名如下：

&emsp;{room}\_{wav_name}\_{speech}_N_NdB.wav

&emsp;&emsp; room为房间名，如room1，room2

&emsp;&emsp; rir_wav_name为具体的wav文件名，如room1-ch1、 room1-ch2

&emsp;&emsp; speech为干语料

### 2. 生成pt文件

**！！！pt文件包含的t60为30维！！！**

对应`pt_generation`

&emsp;修改**`thread_process.py`** 28-30行的参数

&emsp;&emsp; wav_root：第1步生成的{output_dir}/Dev/Speech/

&emsp;&emsp; save_pt_root：要保存的pt文件路径

&emsp;&emsp; csv_path_root：第1步生成的{output_dir}/Dev/Speech/

读取wav_root下所有房间文件夹名称，在save_pt_root下生成对应的pt

生成的pt文件格式与wav一致，后面-0表示通道

## 含噪数据生成

### 1. 生成wav文件

对应`wav_generation/AddNoise`

1.1 修改**`gen_convwav_shell.py`**的参数：

&emsp;&emsp;xls_file：RIR对应的xls文件

&emsp;&emsp;rir_dir：RIR路径地址

&emsp;&emsp;output_dir：wav文件输出路径

&emsp;&emsp;gen_convwav_shell：生成的sh文件

&emsp;&emsp; log：使用nohup进行后台运行的log记录路径，默认为"./log"

&emsp;如要**修改干语料**，修改option.py下的参数：

&emsp;&emsp;Speaker_root：干语料路径

&emsp;&emsp;Speaker_txt：干语料txt

&emsp;如要**修改噪音**，修改option.py下的参数：

&emsp;&emsp;noise_dir：noise的txt目录

1.2 运行`python gen_convwav_shell.py`，会在output_dir下生成csv文件，并生成sh文件

1.3 随后运行生成的sh文件（即1.1中的参数gen_convwav_shell），会在output_dir文件夹下生成RIR\*speech的wav文件Dev/Speech/{room}/*.wav



&emsp;生成的WAV文件命名如下：

&emsp;{room}\_{wav_name}\_{speech}\_{noise}_{SNR}dB.wav

&emsp;&emsp;room：房间名，如room1，room2

&emsp;&emsp;rir_wav_name：具体的wav文件名，如room1-ch1、 room1-ch2

&emsp;&emsp;speech：干语料

&emsp;&emsp;noise：噪音

&emsp;&emsp;SNR：信噪比

### 2. 生成pt文件

**！！！pt文件包含的t60为30维！！！**

对应`pt_generation`

&emsp;修改**`thread_process.py`** 28-30行的参数

&emsp;&emsp;wav_root：第1步生成的{output_dir}/Dev/Speech/

&emsp;&emsp;save_pt_root：要保存的pt文件路径

&emsp;&emsp;csv_path_root：第1步生成的{output_dir}/Dev/Speech/

读取wav_root下所有房间文件夹名称，在save_pt_root下生成对应的pt

生成的pt文件格式与wav一致，后面-0表示通道
