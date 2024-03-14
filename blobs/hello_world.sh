#!/bin/bash
. ~/.bashrc

source /SFS/product/Modules/default/init/bash
source ${SGE_ROOT}/${SGE_CLUSTER_NAME}/common/settings.sh
module load R/3.4.1

#R -e 'helloWorldfunct <- function(){     myHelloString <- "Hello world"     print ( myHelloString)  }  helloWorldfunct()'

R -e 'print("myHelloString")'
