#/bin/bash

# Python version we want to build
VERSION="2.7.9"

# Retrieve the latest (compressed) archive containing Python $VERSION source code.
wget http://www.python.org/ftp/python/$VERSION/Python-$VERSION.tar.xz

#Install xz if it's not installed yet
sudo yum install xz-libs

# Extract !
xz -d Python-$VERSION.tar.xz && tar -xvf Python-$VERSION.tar

# Configure the compilation - type "./configure --help" to get all the options
# By default files are installed in /usr/local, use --prefix to modify that (e.g. for $HOME).
cd Python-$VERSION
echo "Time to configure"
./configure --prefix=/usr/local  

# We can optimize the compilation process
NUMPROC=`cat /proc/cpuinfo | grep processor | wc -l`

# Compile the source
# Option -j is here to use $NUMPROC jobs, one on each processor (hence the previous command)
make -j $NUMPROC

# Normally, one would use “make install”;
# HOWEVER, in order NOT to override system defaults - replacing the Python already used by the system - we will use make altinstall.
make -j $NUMPROC altinstall

# Then create an alias in order to use python 2.7 for the current user, in order NOT to break everything
echo "alias python=/usr/local/bin/python2.7" >> ~/.bashrc