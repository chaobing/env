#! /bin/bash
echo ">> concat file in subdir"

if test $# -lt '1'; then
  echo "usage: ./doCancat.sh <case dir>"
  exit 1
fi

subdir=$1
if [ ! -d $subdir ]; then
  echo "[ERROR]: $subdir is not a valid directory"
  exit
fi

dirlists=()
filelists=()

getDirName(){
  indir=$(cd $1 && pwd)
  echo "[INFO]: Get sub dir name under "$indir
  instMax=5
  for((len=1;len<${instMax};len++))
  do
    pattern=inst_[0-9]\\{$len\\}$
    for file in $(ls $indir | grep -i "$pattern")
    do 
      if [ -d $indir/$file ]; then
        dirlists=("${dirlists[@]}" $file)
      fi
    done
  done
}

getFileName(){
  dir=$(cd $1/${dirlists[0]} && pwd)
  echo "[INFO]: Get file name form "$dir
  fstring=$(ls $dir)
  filelists=(${fstring//,/ /})
}

getDirName $subdir
echo "[INFO]: sub diretory lists:"
echo ${dirlists[@]}

getFileName $subdir
echo "[INFO]: sub file lists:"
echo ${filelists[@]}

dstdir=concat
mkdir -p $dstdir
for((fidx=0;fidx<${#filelists[@]};fidx++))
do
  fname=${filelists[fidx]}
  dst=${dstdir}/${fname}
  if [ -f $dst ]; then
    rm -rf $dst
  fi
  echo "[INFO]: concat files to "$dst
  touch $dst
  for((cidx=0;cidx<${#subdir[@]};cidx++))
  do
    dname=${subdir[cidx]}
    src=${subdir}${dname}/${fname}
    echo "  $src"
    #cat $src >> $dst
  done
done
