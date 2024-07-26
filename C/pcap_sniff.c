#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h> //for in_addr
#include <netinet/in.h>
#include <arpa/inet.h> //inet_ntoa

#include <pcap/pcap.h>

#include "hacking.h"

#define ADDRESS_SIZE 15
#define DEVICE_SIZE 30

//void fatal()

int main(void)
{
	/*char dev[DEVICE_SIZE]; //Name of the device to use
	char net[ADDRESS_SIZE]; //Dot notation of the network
	char mask[ADDRESS_SIZE]; //OK*/
	
	struct pcap_pkthdr header;
	
	const u_char* packet;
	pcap_t *pcap_handle; //= (pcap_t*)malloc(sizeof(struct pcap_t));
	
	char* dev = "";
	char* net = ""; //Dot notation of the network
	char* mask = "";
	int r=0; //return code
	char errbuf[PCAP_ERRBUF_SIZE];
	
	bpf_u_int32 netp; //ip
	bpf_u_int32 maskp; //subnet mask
	//struct in_addr* addr = (struct in_addr*)sizeof(struct in_addr);
	struct in_addr addr ;
	

	//ask pcap to look for a device to sniff on
	if((dev = pcap_lookupdev(errbuf)) == NULL) fatal(errbuf);
	else {
		//print out device name
		printf("DEV: %s\n", dev);
	}

	/*
	pcap_open_live(char *device, int snaplen, int promisc, int to_ms, char *errbuf)
	to_ms <-> temporization value
	returns a pcap_t * on success and NULL on failure
	*/
	
	if((pcap_handle = pcap_open_live(dev, 4096, 1, 0, errbuf)) == NULL) fatal(errbuf);
	else {
		//printf("Opened packet capture device: %s\n", );
		int i = 0;
		for (i = 0; i < 3; i++)
		{
			packet = pcap_next(pcap_handle, &header); //define packet & header
			printf("Got a %d byte(s) packet\n", header.len);
			dump(packet, header.len);
		}
		pcap_close(pcap_handle);
	}

	//ask pcap for the network address & mask of the device
	if((r = pcap_lookupnet(dev, &netp, &maskp, errbuf)) == -1) {printf("r==-1\n"); fatal(errbuf);}
	else {
		//printf("r!=-1\n");
		//get the network address in a human readable form
		//addr->s_addr = netp;
		addr.s_addr = netp;
		if((net = inet_ntoa(addr)) == NULL) fatal("inet_ntoa");
		else printf("NET: %s\n", net);

		//do the same for the device's mask
		addr.s_addr = maskp;
		if((mask = inet_ntoa(addr)) == NULL) fatal("inet_ntoa");
		else printf("MASK: %s\n", mask);
	}

	//free(pcap_handle);

	return 0;
}