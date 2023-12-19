import os
import numpy as np
import time
#from .extraLib import resample
from extraLib import strcmp,judgeList,v_addnoise
import wave
import scipy.signal as sg
from  getACECorpusData import getACECorpusData
from  readInT60DRRSubband import readInT60DRRSubband
from  genCorpusStdOut import genCorpusStdOut
import librosa
import csv
from scipy import signal
import soundfile as sf
import datetime
import csv
import glob
import random
from option import args

def genACECorpusDataset(params):
    ACECorpusData = getACECorpusData(params.readFromServer)
    #funciton logic
    nRoomMicDists = len(params.roomMicDistRange)
    
    nMicConfigs = params.micConfigRange

    nSNRs = len(params.snrRange)
    nNoises = len(params.noiseRange)
    nTalkers = len(params.talkerRange)
    nUtterTypes = len(params.utterRange)

    #T60DRRresultsFile = "/data2/cql/code/augu_data/test_icothief/test_icothief.csv"

    T60DRRresultsFile = args.T60DRRresultsFile


    # REVIEW  读取T60_file

    T60DRRData = readInT60DRRSubband(T60DRRresultsFile)


    freqBands = np.unique(T60DRRData["freqBand"])

    nFreqBands = len(freqBands)

    a = params.corpusOutputFolderRoot
    b = params.datasetName
    c = ACECorpusData.ACE_DATA_EXT_SPEECH
    # corpusFolder = os.path.join(params.corpusOutputFolderRoot,params.datasetName,ACECorpusData.ACE_DATA_EXT_SPEECH)
    #corpusFolder = params.corpusOutputFolderRoot+params.datasetName+'/'+ACECorpusData.ACE_DATA_EXT_SPEECH
    corpusFolder = params.corpusOutputFolderRoot
    if not os.path.exists(corpusFolder):

        os.makedirs(corpusFolder)

    #Do the convolving of the files
    results = {} #是为test_id创建一个字典

    for micConfigInd in range(params.micConfigRange):
        #Load the mic config parameters
        
        params.corpusMicConfig = ACECorpusData.MIC_CONFIGs[micConfigInd]
        if "_" in params.corpusMicConfig:
            raise ValueError("命名不允许包含下划线")
        
        if params.corpusMicConfig != args.need_config:
            continue
        if params.corpusMicConfig == ACECorpusData.REC_CONFIG_SINGLE:
            # DO nothing
            params.micConfigGT = params.singleMicConfigGT #赋予它Linch的设备
        else:
            params.micConfigGT = params.corpusMicConfig
        #Generate the output folder mic config name
        micConfigCorpusFolder = os.path.join(corpusFolder , params.corpusMicConfig)

        if not os.path.exists(micConfigCorpusFolder):
            os.makedirs(micConfigCorpusFolder)
            # raise  ValueError('Corpus mic config root folder %s does not exist.  Creating.', micConfigCorpusFolder)


        #Open the output file containing the meta data for each data set
        #还不清楚它为什么要创建一个这样的列表
        #表明测试了多少次吧
        results["testID"]= 1
        #Open an output file.  Deal with the condition where the job is being
        #restarted
        if params.startOffset == 0:
            #time.strftime("%d:%m:%Y")
            #resultsFileName = micConfigCorpusFolder+'_'+params.testName +'_results.txt'
            dt = datetime.datetime.now()
            resultsFileName = os.path.join(micConfigCorpusFolder,"results.csv")
            print("resultFilename:",resultsFileName)
            resultsHandle = open(resultsFileName, "a",newline="")
            csv_writer = csv.writer(resultsHandle)

                #resultsHandle = csv.writer(csvfile)
        else:
            if strcmp(params.startOffsetDate, ''):
                print('Timestamp for existing file to append not specified.  Should be in format yyyymmddThhmmss')
                # raise ValueEroor('Timestamp for existing file to append not specified.  Should be in format yyyymmddThhmmss')
            resultsFileName = os.path.join(micConfigCorpusFolder,"results.csv")
            print("resultFilename:",resultsFileName)

            resultsHandle = open(resultsFileName, "w",newline="")
            csv_writer = csv.writer(resultsHandle)
            results["testID"] = results["testID"] + params.startOffset
        params.rowsTotal = nRoomMicDists * nMicConfigs * nTalkers * nUtterTypes * nNoises * nSNRs

        rirFolder = str(params.corpusInputFolderRoot)
        #rirFolder = os.path.join(str(params.corpusInputFolderRoot),str(params.corpusMicConfig))
        #print("rirFolder:",rirFolder)
        time_rir = time.time()
        
        for sourceRIRFileName in glob.glob(rirFolder+"/*.wav"):

            params.Room = (sourceRIRFileName.split("/")[-1]).split(".")[0]
            h, rir_sr = librosa.load(sourceRIRFileName, sr = params.fs,mono=False)
            h = librosa.util.normalize(h)
            h = h.T
            print("加载一条rir的时间是:{}".format(time.time()-time_rir))

            #提取不同场景下相应的rir
            source_wav = (sourceRIRFileName.split("/")[-1]).split(".")[0]
            utterCsvFileName = "Unknown" + "_" +params.corpusMicConfig+ "_" + source_wav+"_<talker>_<utter>_<noise>_<SNR>dB.wav"
            #Get the T60 and DRR information
            if h.ndim == 1:
                params.nChannels = 1
            else:

                _, params.nChannels = h.shape
            #-------------------------------------------------------这里插入噪音信号-----------------------------------------------------
            dict_noise = {}
            
            time_noise = time.time()
            line1 = []
            print(line1)

            print("读取15条语音的时间是:{}".format(time.time() - time_noise))
            #for chanInd in range(0,params.nChannels):
            #升到只有1到9
            if h.ndim != 1:
                nChannels = h.shape[1]
            else:
                nChannels = 1
            for chanInd in range(1,nChannels+1):
                #% Use the original channel from the appropriate mic config from
                # the ground truth data
                # if strcmp(params.corpusMicConfig, ACECorpusData.REC_CONFIG_SINGLE):
                if params.corpusMicConfig == ACECorpusData.REC_CONFIG_SINGLE:
                    channelGT = params.singleMicConfigGTChan

                else:
                    channelGT = chanInd
                    #nChannels = h.shape[1]
                #T60DRRData是从表格读出来的数据
                #TODO 这里需要确认是否要对rowIndex等相应参数进行+-1操作,row_Index是逻辑值二维的，不能用于对list使用，这个还没考虑清楚

                for freqBandInd in range(nFreqBands):
                    #因为matlab可以直接判断[1,2,3]==1 -> [1,0,0],而python却不能，所以这里也要做相应的处理

                    # rowIndex = T60DRRData.channel == channelGT & T60DRRData.sessionID == params.sessionID & \
                    #            strcmp(T60DRRData.config, params.micConfigGT) &\
                    #            strcmp(T60DRRData.freqBand, num2str(freqBandInd))
                    judge1 = T60DRRData["channel"]==np.array([channelGT])

                    judge2 = T60DRRData["room"]==np.array(params.Room)
                    judge3 = np.array([T60DRRData["config"][i]==params.micConfigGT for i in range(len(T60DRRData["config"]))])#T60DRRData["config"]== np.array(params.micConfigGT)
                    judge4 = T60DRRData["freqBand"] == np.array([freqBandInd+1])

                    rowIndex = judge1 & judge3 & judge4 & judge2

                    if sum(rowIndex) == 0:
                        print("HEAT")
                        if sum(judge1) == 0:
                            print("HEAT judge1")
                        if sum(judge2) ==0 :
                            print("HEAT judge2")
                        if sum(judge3) == 0:
                            print("HEAT judge3")
                        if sum(judge4) == 0:
                            print("HEAT judge4")
                        continue
                    else:
                        print("PASS")
                    #results.testID already assigned
                    results["channel"] = chanInd
                    #str2double because it is saved as a silly string by mistake
                    # a = T60DRRData["freqBand"]
                    # b = a[rowIndex]
                    print("T60DRRData:",T60DRRData)

                    results["freqBand"] = T60DRRData["freqBand"][rowIndex]# 11
                    print("freqBand:",results["freqBand"],"rowindex:",rowIndex)


                    results["centreFreq"] = T60DRRData["centreFreq"][rowIndex]#12
                    results["DRR"] = T60DRRData["DRR"][rowIndex]# 14
                    results["DRRMean"] = T60DRRData["DRRMean"][rowIndex]#15
                    results["T60"] = T60DRRData["T60AHM"][rowIndex]#16
                    results["T60Mean"] = T60DRRData["T60AHMMean"][rowIndex]# 19
                    #Fullband for this channel
                    results["DRRFullband"] = T60DRRData["DRRFullband"][rowIndex]# 22
                    results["T60Fullband"] = T60DRRData["T60AHMFullband"][rowIndex]#24
                    #If single channel, then the fullband mean across all channels is the same
                    # as for this channel
                    if strcmp(params.corpusMicConfig, ACECorpusData.REC_CONFIG_SINGLE):
                        results["DRRFullbandMean"] = T60DRRData["DRRFullband"][rowIndex]#23
                        results["T60FullbandMean"] = T60DRRData["T60AHMFullband"][rowIndex]#27
                    else:

                        results["DRRFullbandMean"] = T60DRRData["DRRFullbandMean"][rowIndex]#23
                        results["T60FullbandMean"] = T60DRRData["T60AHMFullbandMean"][rowIndex]#27
                    results["fileName"] = utterCsvFileName
                    
                    
                    params.roomCodeName =  params.Room
                    if "_" in params.roomCodeName:
                        raise ValueError("wav文件命名不允许包含下划线")
                    
                    params.roomConfig = params.corpusMicConfig
                    Head,outputLine = genCorpusStdOut(results, params)
                    if Head is not None:
                        csv_writer.writerow(Head)
                    if outputLine is not None:
                        csv_writer.writerow(outputLine)
                    print('%s'%outputLine)
                    print(resultsHandle, '%s'%outputLine)
                    results["testID"] = results["testID"] + 1
            #我将TIMIT数据保存为了一个train.txt/test.txt，我只需遍历这个文件就行了啊！
            #print("asdfasdf",ACECorpusData.TIMIT_TRAIN_TXT)
            with open(ACECorpusData.TIMIT_TRAIN_TXT,encoding = 'gb2312') as read:
                line2 = [lines for lines in read.readlines()]

            for f2 in line2:
                time_timit = time.time()
                wave_file = f2.split("\n")[0]
                
                speaker_root = args.Speaker_root
                wave_file = os.path.join(speaker_root, wave_file)
                
                y, sr = librosa.load(wave_file, sr = params.fs,mono=False)
                y = librosa.util.normalize(y)
                print("加载timit时间{}".format(time.time()-time_timit))
                
                if h.ndim != 1:
                    revUtter = np.zeros([y.shape[0], h.shape[1]])
                    for i in range(h.shape[1]):
                        hh = h[:, i]
                        data = np.convolve(y, hh)
                        revUtter[:, i] = data[:y.shape[0]]
                else:
                    
                    revUtter = np.convolve(y, h,"valid")

                    revUtter = np.expand_dims(revUtter, axis=1)
                save_name_list = wave_file.split("/")[-1]
                save_name = save_name_list.split(".")[0]
                
                
                params.talkerCodeName = save_name
                if "_" in params.talkerCodeName:
                        raise ValueError("speech命名不允许包含下划线")
                
                results["fullUtterOutFileName"] = os.path.join(micConfigCorpusFolder, '%s_%s_%s_N_NdB.wav'%(
                        params.corpusMicConfig,
                        params.roomCodeName,
                        params.talkerCodeName,
                        ))
                time_write = time.time()
                sf.write(results["fullUtterOutFileName"],revUtter,params.fs)
                print("写入文件用时：{}".format(time.time()-time_write))
                
        resultsHandle.close()

    print("finishing saving")

