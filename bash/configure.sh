#!/bin/bash
set -e

script_path=$(dirname "$(realpath $0)")
project_name=$(basename $script_path)

#cmake args
declare -a args
args=(-DBUILD_TEST=ON)

#options
options=$(getopt -a -n 'parse-options' -o h \
          -l help,clean,build-only,type:,pack:,build-dir:,install-prefix:,cmake-options: \
          -- "$0" "$@")
echo $options
[ $? -eq 0 ] || {
  echo "[ERROR] failed to parse options! try --help"
  exit 1
}
eval set -- "$options"
while true; do
  case "$1" in
    -h | --help) show_help=true; break;;
    --clean) clean=true;;
    --build-only) build_only=true;;
    --type)
      shift
      case "$1" in 
        release) build_type=Release;;
        debug) build_type=Debug;;
        *) echo "[ERROR] invalid build type \"$1\"! try --help"; exit 1;;
      esac
      ;;
    --pack)
      shift
        build_package=true
      case "$1" in
        deb) args+=(-DCPACK_GENERATOR="DEB");;
        rpm) args+=(-DCPACK_GENERATOR="RPM");;
        *) echo "[ERROR] invalid pack format \"$1\"! try --help"; exit 1;;
      esac
      ;;
    --build-dir) shift; build_dir=$1;;
    --install-prefix) shift; install_prefix=$1;;
    --cmake-options) shift; args+=($1);;
    --) shift; break;;
  esac
  shift
done

args+=(-DCMAKE_BUILD_TYPE=${build_type:="Debug"})
[ ${build_type} == "Debug" ] && args+=(-DCMAKE_EXPORT_COMPILE_COMANDS=ON)

if [ -z ${OECORE_TARGET_SYSROOT:+x} ]; then
  echo "Native-platform building..."
  #os=`lsb_release -a | grep "Distributor ID" | sed 's/^.*:\s*//'`
  #os_version=`lsb_release -a | grep "Release" | sed 's/^.*:\s*//'`
  #arch=`uname -p`
  os=`sw_vers -productName | sed 's/ //g'`
  os_version=`sw_vers -productVersion`
  arch=`uname -m`
  target_info=${os}.${os_version}.${arch}.${build_type}
  install_prefix_default=$HOME/.local/${target_info}
else
  echo "Not support Cross-platform building"
  exit 1
fi

build_dir_default=$HOME/build/build.${target_info}/${project_name}
[ -z ${build_dir:+x} ] && build_dir=${build_dir_default}

if [ ${show_help:=false} == true ]; then
  echo "./cmake.sh [options]"
  echo "      --help                        show help"
  echo "      --clean                       dirscard build dir before build"
  echo "      --build-only                  build only, not install"
  echo "      --type[=TYPE]                 build type, {release, debug(default)}"
  echo "      --pack[=FORMAT]               enable packing, and set format{deb, rpm}"
  echo "      --build-dir[=DIR]             set build dir, defalut is ${build_dir_default}"
  echo "      --install-prefix[=PREFIX]     set install prefix, defalut is ${install_prefix_default}"
  echo "      --cmake-options[=OPTIONS]     append more options"
else
  mkdir -p ${build_dir}
  ${clean:=false} && rm -fr ${build_dir}/*
  cd ${build_dir}
  echo "cd $PWD"
  echo cmake "${args[@]}" "${script_path}"
  cmake "${args[@]}" "${script_path}"
  make -j
  ${build_only:=false} || make install
  ${build_package:=false} && make package

fi

exit 0

<<!
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make -j4
!

