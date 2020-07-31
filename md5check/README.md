# md5 check
#### Author: Peng Jia  
#### Email: pengjia$@stu.xjtu.edu.cn  
#### Description: This script is used for md5 check with many file.  
  
---
### Usage: 
 

#### 1. Configuration

   change the file path, working space and some basic information in checkmd5.smk
#### 2. Run

   check md5 by snakemake 
    
      snakemake -j {jobs} -s path/to/checkmd5.smk 
       
   you can check also debug using 
    
      snakemake  -s path/to/checkmd5.smk -n
  
#### 3. Manual check

   check the result in working space 
   

       
