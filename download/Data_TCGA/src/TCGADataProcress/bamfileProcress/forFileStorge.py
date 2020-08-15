#=============================================================================
# Project : TCGADataProcress
# Py Name: forFileStorge
# Author : 
# Date : 18-11-10
# Email : pengjia@stu.xjtu.edu.cn 
# Description : ''
#=============================================================================
import json
import pandas as pd
dir_root_data="/mnt/project/DataProcress/Data_TCGA/data/"

def getCaseInfo():
    newCASEINFO=pd.DataFrame()
    newBAMINFO=pd.DataFrame()
    data = json.load(open(dir_root_data + "TCGA_MSI.json", "r"))
    for file in data:
        filename = file['file_name']
        md5 = file["md5sum"]
        # barcode = file['associated_entities'][0]['entity_submitter_id']
        newBAMINFO.loc[filename,"md5"]=md5


    DATA_info=json.load(open(dir_root_data+"data.json","r"))
    # print(len(DATA_info))
    DataStructure={}
    for case in DATA_info:
        # print(DATA_info[case])
        caseTumor=DATA_info[case]["cancer_type"]
        if caseTumor not in DataStructure:
            DataStructure[caseTumor]={}
        if case not in DataStructure[caseTumor]:
            DataStructure[caseTumor][case]={}


        newCASEINFO.loc[case,"tumor"]=caseTumor
        newCASEINFO.loc[case, "MSI"]=DATA_info[case]["MSI"]
        if "N" in DATA_info[case]:
            for NBam in DATA_info[case]["N"]:
                # print(NBam)
                id=NBam["filename"]
                newBAMINFO.loc[id, "case"]=case
                newBAMINFO.loc[id,"tumor"]=caseTumor
                newBAMINFO.loc[id, "MSI"]=DATA_info[case]["MSI"]
                newBAMINFO.loc[id,"NT"]="N"
                newBAMINFO.loc[id, "bamname"] = NBam["filename"]
                newBAMINFO.loc[id, "barcode"] = NBam["barcode"]
                newBAMINFO.loc[id, "bampath"] = "/home/TCGA/TCGA_BAM/"+"/".join([caseTumor,case,NBam["barcode"],NBam["filename"]])
                newBAMINFO.loc[id,"fileexist"]=False
                newBAMINFO.loc[id, "checkMd5"] = False

                DataStructure[caseTumor][case][NBam["barcode"]]=""


        if "T" in DATA_info[case]:
            for NBam in DATA_info[case]["T"]:
                id = NBam["filename"]
                newBAMINFO.loc[id, "case"] = case
                newBAMINFO.loc[id, "tumor"] = caseTumor
                newBAMINFO.loc[id, "MSI"] = DATA_info[case]["MSI"]
                newBAMINFO.loc[id, "NT"] = "T"
                newBAMINFO.loc[id, "bamname"] = NBam["filename"]
                newBAMINFO.loc[id,"barcode"]=NBam["barcode"]
                newBAMINFO.loc[id, "bampath"] = "/home/TCGA/TCGA_BAM/"+"/".join([caseTumor,case,NBam["barcode"],NBam["filename"]])
                newBAMINFO.loc[id, "fileexist"] = False
                newBAMINFO.loc[id, "checkMd5"] = False

                DataStructure[caseTumor][case][NBam["barcode"]] = ""
    file = open(dir_root_data + "DataStructure.json", "w")
    file.write(json.dumps(DataStructure))
    file.close()
    # DataStructure.
    print(newCASEINFO)
    # print(newBAMINFO)
    newBAMINFO.to_csv(dir_root_data+"BAMINFO.csv")
    newCASEINFO.to_csv(dir_root_data+"CaseINFO1114.csv")
def fileMvScript():
    originbam={}
    newbam={}
    newBAMINFO=pd.read_csv(dir_root_data + "BAMINFO.csv",index_col=0)
    file=open(dir_root_data+"FileMV.sh","w")
    for line in open(dir_root_data+"orginBam"):
        bam=line[:-1].split("/")[-1]
        originbam[bam]=line[:-1]
    for line in open(dir_root_data + "newbam"):
        bam = line[:-1].split("/")[-1]
        newbam[bam]=line[:-1]
    # print(line)
    for i in newbam:
        if i in originbam:
            print(i)
        else:
            file.write(
                "mv "+newbam[i][:-1] +"i "+ newBAMINFO.loc[i,"bampath"][:-1]+"i\n"
            )
    file.close()
def mkdirScript():
    DataStructure=json.load(open(dir_root_data+"DataStructure.json","r"))
    # print(DataStructure)
    file=open(dir_root_data+"bam_mkdir","w")
    head="/home/TCGA/TCGA_BAM/"
    for tumor in DataStructure:
        # print(tumor)
        file.write(
            "if [ ! -d "+head+tumor+" ];then mkdir "+head+tumor+" ; fi\n"

        )
        for case in DataStructure[tumor]:
            file.write(
                "if [ ! -d "+head+tumor+"/"+case+" ];then mkdir "+head+tumor+"/"+case+" ; fi\n"

            )
            # print(case)
            for barcode in DataStructure[tumor][case]:
                file.write(
                    "if [ ! -d " + head + tumor + "/" + case + "/" + barcode + " ];then mkdir " + head + tumor + "/" + case +"/" + barcode +" ; fi\n"

                )
                # print(barcode)
    file.close()

def md5check():
    newBAMINFO = pd.read_csv(dir_root_data + "BAMINFO.csv", index_col=0)
    for line in open(dir_root_data+"result.md5","r"):
        bam=line[:-1].split("/")[-1]
        if bam in newBAMINFO.index:

            md5=line.split(" ")[0]
            if md5== newBAMINFO.loc[bam,"md5"]:
                # print(bam)
                newBAMINFO.loc[bam,"checkMd5"]=True
                newBAMINFO.loc[bam, "fileexist"] = True
            else:
                print()
                # print("mv ./"+bam[:-1]+"* "+"/".join(line[:-1].split(" ")[-1].split("/")[:-1])+"/")
    num=0
    newMd5list=[]
    for line in open(dir_root_data+'newbamname',"r"):
        bam=line[:-1].split("/")[-1]
        if bam in newBAMINFO.index:
            newBAMINFO.loc[bam, "fileexist"] = True
            if newBAMINFO.loc[bam,"checkMd5"]==False:
                if num%100 ==0:
                    file = open(dir_root_data + "needMd5checkList"+str(num//100), "w")
                    file.write("md5result=needMd5checkList"+str(num//100)+".md5\n")

                file.write("md5sum "+newBAMINFO.loc[bam,"bampath"]+" >>$md5result"+"\n")
                newMd5list.append(bam)
                if num%100 ==99:
                    file.close()
                num+=1
    file.close()
    file=open(dir_root_data+"md5_error20181113check","w")
    for line in open(dir_root_data + "result20181113.md5", "r"):
        bam = line[:-1].split("/")[-1]
        if bam in newBAMINFO.index:
            md5 = line.split(" ")[0]
            if md5 == newBAMINFO.loc[bam, "md5"]:
                # print(bam)
                newBAMINFO.loc[bam, "checkMd5"] = True
            else:
                print(newBAMINFO.loc[bam, "md5"],newBAMINFO.loc[bam, "bampath"])
                # print("mv "+bam[:-1]+"* "+"/".join(newBAMINFO.loc[bam,"bampath"].split("/")[:-1])+"/")
                # file.write(bam+"\n")
                file.write("md5sum "+newBAMINFO.loc[bam,"bampath"]+" >>md520171113result13"+"\n")

    file.close()
    for line in open(dir_root_data + "md520171113result13", "r"):
        bam = line[:-1].split("/")[-1]
        if bam in newBAMINFO.index:
            md5 = line.split(" ")[0]
            if md5 == newBAMINFO.loc[bam, "md5"]:
                # print(bam)
                newBAMINFO.loc[bam, "checkMd5"] = True
            else:
                print("kdk")
    # print(len(newBAMINFO.index))
    newBAMINFO.to_csv(dir_root_data+"bamINFO.csv")



                # print(line[:-1].split(" ")[2])

if __name__ == "__main__":
    # jsonProcress()
    getCaseInfo()
    # fileMvScript()
    # mkdirScript()
    # fileMvScript()
    # md5check()
    print()

