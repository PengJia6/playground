import os
os.path.exists()
print("")
linenum=0
file=open("/mnt/MyFiles/1KG/aspera_download_part11.sh","w")
for line in open("/mnt/MyFiles/1KG/aspera_download_part11.pbs"):
    linenum+=1
    if linenum>5:
        lineinfo=line[:-1].split()
        file.write(" ".join(lineinfo[:10]+["/home/sunyu/downloads/"])+"\n")
        file.write(" scp ./"+lineinfo[9].split("/")[-1]+ " $cluster/home/pengjia/1KG/part11/\n" )
        file.write(" rm ./"+lineinfo[9].split("/")[-1]+ "\n" )

    else:
        file.write(line)
file.close()

    # if
