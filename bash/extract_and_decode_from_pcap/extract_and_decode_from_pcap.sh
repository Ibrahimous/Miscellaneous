#/usr/bin/bash

## Produce a file called "base64_decoded" from a .cap.gz file 		##
## Usage example:													##
##	$ bash extract_from_pcap.sh <pcap file> <recipient of the spam> ##
##	$ dd if=base64_decoded of=malicious.zip							##
## You'll need to "sudo aptitude install tcpflow -ry"				##
## Charles Ibrahim - @Ibrahimous									##

# First you have to retrieve the .cap.gz file in the directory you're going to launch the script in
# Use extract_from_pcap.sh with a pcap file & a recipient who got spammed
if [ "$#" -ne 2 ]; then
        echo "Usage: bash extract_from_pcap.sh <pcap file> <recipient of the spam>"
        exit
else
        PCAPFILE=$1
        RECIPIENT=$2
fi

# Drop the .gz
EXTRACTEDPCAP=${PCAPFILE%.*}
echo "Extracting pcap file and writing it to $EXTRACTEDPCAP"

#TODO: add port filtering
zcat $PCAPFILE | tcpdump -qnr - -w $EXTRACTEDPCAP 

mkdir -p sessions
	cd sessions 
	tcpflow -r ../$EXTRACTEDPCAP
	SESSIONFILE=`grep $RECIPIENT * -l`
cd ..

sed -n "/filename=/,/------------------------/p" sessions/$SESSIONFILE | tail -n +3 | head -n -2 | base64 -di > base64_decoded