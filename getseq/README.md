# getseq 

#### Author: Peng Jia  
#### Email: pengjia$@stu.xjtu.edu.cn  
#### Description: get a sequence for a bam file or a fasta file based on a bed or a region (chr1:12345-45678).
----

##Contact
If you have any questions, please contact with Peng Jia (pengjia@stu.xjtu.edu.cn).
##Requirement
* pysam
  
   
       conda install pysam
## Usage: 
    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
    
    command:
      
        fasta        Get sequence for fasta file
        bam          Get sequence for bam file
    Traceback (most recent call last):
      File "getseq.py", line 235, in <module>
        if args["command"] == "bam":
    TypeError: 'bool' object is not subscriptable
 ## command:
 
 * ### fasta
        usage: getseq.py fasta [-h] -f FASTA [regions [regions ...]]
        
        Get sequence for fasta file.
        
        positional arguments:
          regions               Regions sush as chr1:123456-235689 path of bed file
                                [required]
        
        optional arguments:
          -h, --help            show this help message and exit
          -f FASTA, --fasta FASTA
                                Input fasta with index [required]
 * ### bam
        usage: getseq.py bam [-h] -b BAM [-r {True,False}] [regions [regions ...]]
        
        Get sequence for bam file.
        
        positional arguments:
          regions               Regions sush as chr1:123456-235689 path of bed file
                                [required]
        
        optional arguments:
          -h, --help            show this help message and exit
          -b BAM, --bam BAM     Input fasta with index [required]
          -r {True,False}, --only_in {True,False}
                                True: only output sequence in a region; False: output
                                read cover a region
 


