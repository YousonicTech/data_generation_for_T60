<div align="center">

# T60 Data Generation

</div>
## 更新日志
2023-6-10 增加现场录音pt文件生成，增加线程控制防止占满cpu资源，调整工程结构

2023-6-8 wav_generation去除Dev/Specch路径生成，合成的wav直接输出到output_dir中

2023-6-7 AddNoise模块option.py添加参数SNR指定信噪比

2023-6-2 优化log日志记录，优化pt生成


## 工程结构

```
├── pt_generation
│   ├── LiveRecord
│   ├── Synthetic
│   ├── __init__.py
│   ├── splweighting.py
│   └── gen_specgram.py
└── wav_generation
    ├── AddNoise
    └── NoNoise
```

## 命名规范

注意：所有文件及文件夹名中请勿出现字符"_"，如要使用请用字符"-"替换，或采用驼峰命名法

RIR及现场录音文件目录格式如下

```
RIR(LiveRecord)
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
## 合成数据
### 不含噪数据生成

#### 1. 生成wav文件

对应`wav_generation/NoNoise`

1.1 修改`gen_convwav_shell.py`的参数：

```
    xls_file：            RIR对应的xls文件
    rir_dir：             RIR路径地址
    output_dir：          wav文件输出路径
    gen_convwav_shell：   生成的sh文件
    log：                 使用nohup进行后台运行的log记录路径，默认为"./log"
 ```

2. 如要修改干语料，修改option.py下的参数：

```
    Speaker_root：  干语料路径
    Speaker_txt：   干语料txt（gb2312格式）
```

1.2 运行`python gen_convwav_shell.py`，会在output_dir下生成csv文件，并生成sh文件

1.3 随后运行生成的sh文件（即1.1中的参数gen_convwav_shell），会在output_dir文件夹下生成RIR\*speech的wav文件{room}/*.wav

1. 生成的WAV文件命名格式： {room}\_{wav_name}\_{speech}_N_NdB.wav

    room为房间名，如room1，room2

    rir_wav_name为具体的wav文件名，如room1-ch1、 room1-ch2

    speech为干语料

#### 2. 生成pt文件

**！！！pt文件包含的t60为30维！！！**

对应`pt_generation/Synthetic`

2. 修改**`thread_process.py`** 28-30行的参数

```
wav_root：      第1步生成的{output_dir}/Dev/Speech/
save_pt_root：  要保存的pt文件路径
csv_path_root： 第1步生成的{output_dir}/Dev/Speech/
```

读取wav_root下所有房间文件夹名称，在save_pt_root下生成对应的pt，生成的pt文件格式与wav一致，后面-0表示通道

### 含噪数据生成

#### 1. 生成wav文件

对应`wav_generation/AddNoise`

1.1 修改**`gen_convwav_shell.py`**的参数：

```
xls_file：          RIR对应的xls文件
rir_dir：           RIR路径地址
output_dir：        wav文件输出路径
gen_convwav_shell： 生成的sh文件
log：               使用nohup进行后台运行的log记录路径，默认为"./log"
```

1. 如要**修改干语料**，修改option.py下的参数：

```
Speaker_root：  干语料路径
Speaker_txt：   干语料txt（gb2312格式）
```

2. 如要**修改信噪比**，修改option.py下的参数：

```
SNR：信噪比列表
```

3. 如要**修改噪音**，修改option.py下的参数：

```
noise_dir：noise的txt目录
```

1.2 运行`python gen_convwav_shell.py`，会在output_dir下生成csv文件，并生成sh文件

1.3 随后运行生成的sh文件（即1.1中的参数gen_convwav_shell），会在output_dir文件夹下生成RIR\*speech的wav文件{room}/*.wav



4. 生成的WAV文件命名格式：{room}\_{wav_name}\_{speech}\_{noise}\_{SNR}dB.wav

    room：房间名，如room1，room2

    rir_wav_name：具体的wav文件名，如room1-ch1、 room1-ch2

    speech：干语料

    noise：噪音

    SNR：信噪比

#### 2. 生成pt文件

**！！！pt文件包含的t60为30维！！！**

对应`pt_generation/Synthetic`

修改**`thread_process.py`** 28-30行的参数

```
wav_root：      第1步生成的{output_dir}/Dev/Speech/
save_pt_root：  要保存的pt文件路径
csv_path_root： 第1步生成的{output_dir}/Dev/Speech/
```

读取wav_root下所有房间文件夹名称，在save_pt_root下生成对应的pt，生成的pt文件格式与wav一致，后面-0表示通道

## 现场录音
对应`pt_generation/LiveRecord`
1.运行`gen_csv.py`，参数如下：

```
xls_file：      现场录音的xls文件，如果你没有，与RIR的xls一致，文件及文件夹命名也需与RIR的相同
output_dir：    csv输出路径，建议与pt输出路径一致
```

2.运行`thread_process.py`

```
wav_root：      现场录音wav根目录
save_pt_root：  pt输出目录
csv_path：      第1步输出的csv地址
```

## TODO
LiveRecordAddNoise