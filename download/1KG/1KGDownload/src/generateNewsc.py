import pandas as pd
part=3
all={}
linenum=0
for line in open("/mnt/MyFiles/1KG/aspera_download_part"+str(part)+".pbs"):
    linenum+=1
    if linenum>5:
        case=line.split(" ")[-2].split("/")[-1]
        all[case]=line
        # print(case)
download={}
for line in open("/mnt/MyFiles/1KG/downloaded_part"+str(part)):
    download[line[:-1]]=""
file=open("/mnt/MyFiles/1KG/aspera_download_part"+str(part)+"_new.sh","w")
file.write("#!/bin/bash\n"
            "ASCP=/home/zwl/.aspera/connect/bin/ascp\n"
           "ASCPSSH=/home/zwl/.aspera/connect/etc/asperaweb_id_dsa.openssh\n"
            "cluster=pengjia@192.168.20.4:\n\n")
for item in all:
    if item in download:
        # print("OK",item)
        continue
    print(item)
    line=all[item]
    lineinfo = line[:-1].split()
    file.write(" ".join(lineinfo[:10] + ["/mnt/f/download/jdlin"]) + "\n")

    # file.write(" ".join(lineinfo[:10] + ["/home/sunyu/downloads/"]) + "\n")
    # file.write(" scp ./" + lineinfo[9].split("/")[-1] + " $cluster/home/pengjia/1KG/part"+str(part)+"/\n")
    # file.write(" rm ./" + lineinfo[9].split("/")[-1] + "\n")
file.close()