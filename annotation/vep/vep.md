# VEP annotation 
website: http://asia.ensembl.org/info/docs/tools/vep/script/index.html
---
### Installation 

* ####install by command 
  ## _Failed_ 
  
* #### docker  
  * pull the image
    
    ```bash
    docker pull ensemblorg/ensembl-vep
    docker run -ti ensemblorg/ensembl-vep ./vep  # test the pull result
    mkdir /home/vep_data
    chmod a+rwx /home/vep_data
    docker run -tiv /home/vep_data:/opt/vep/ .vep ensemblorg/ensembl-vep perl INSTALL.pl # download database cache reference and plugins      
    ```
    
  * download the required data manually
    
    * download reference and decompress 
    
    ```bash
    cd /home/vep_data 
    mkdir fasta
    cd fasta
    ID=38
    version=100
    axel -n 100 ftp://ftp.ensembl.org/pub/release-${version}/variation/VEP/homo_sapiens_vep_${version}_GRCh${ID}.fa.gz
    # if this link is unavailable, please get new link from the ftp server of ensembl
    gzip -d homo_sapiens_vep_${version}_GRCh${ID}.fa.gz  
    ```
    
    * download caches and decompress 
    ```bash
    cd /home/vep_data 
    ID=38
    version=100
    axel -n 100  ftp://ftp.ensembl.org/pub/release-${version}/variation/VEP/homo_sapiens_vep_${version}_GRCh${ID}.tar.gz
    # if this link is unavailable, please get new link from the ftp server of ensembl
    gzip -d homo_sapiens_vep_${version}_GRCh${ID}.tar.gz  
    ```
    * download plugin from github and vep [website](https://asia.ensembl.org/info/docs/tools/vep/script/vep_plugins.html)
     ```bash
    cd /home/vep_data 
    ID=38
    version=100
    git clone https://github.com/Ensembl/VEP_plugins.git
    mv VEP_plugins Plugins
    cd Plugins 
    axel -n xxx # download additional file of plugins you need
    ```
  
  
  Now, enjoy vep according docker.  
  
  
  
    
    
       
             