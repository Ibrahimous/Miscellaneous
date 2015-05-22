#/bin/bash

#Retrieves the latest (compressed) archive containing Python source code. We will target --version $VERSION.
VERSION="2.7.9"
wget http://www.python.org/ftp/python/$VERSION/Python-$VERSION.tar.xz

#Install xz if not the case
sudo yum install xz-libs

# Let's decode (-d) the XZ encoded tar archive:
xz -d Python-$VERSION.tar.xz
# Now we can perform the extraction:
tar -xvf Python-$VERSION.tar

# Enter the file directory:
cd Python-$VERSION

# Start the configuration (setting the installation directory)
# By default files are installed in /usr/local.
# You can modify the --prefix to modify it (e.g. for $HOME).

echo "Time to configure"
./configure --prefix=/usr/local  

NUMPROC=`cat /proc/cpuinfo | grep processor | wc -l`

# Let's build (compile) the source
# This procedure can take awhile (~a few minutes)
make -j $NUMPROC

#Normally, one would use “make install”; however, in order not to override system defaults - replacing the Python already used by the system - we will use make altinstall.

# After building everything:
make -j $NUMPROC altinstall

# Then create an alias in order to use python 2.7 without breaking everything
echo "alias python=/usr/local/bin/python2.7" >> ~/.bashrc