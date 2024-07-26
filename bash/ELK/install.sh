#!/bin/bash

#### Elasticsearch ####

#Download and install the Public Signing Key
wget -qO - https://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -

#Add the following to your /etc/apt/sources.list to enable the repository
sudo add-apt-repository "deb http://packages.elasticsearch.org/elasticsearch/1.4/debian stable main"

#Run apt-get update and the repository is ready for use. You can install it with :
sudo apt-get update && sudo aptitude install elasticsearch -ry

#Configure Elasticsearch to automatically start during bootup :
#sudo update-rc.d elasticsearch defaults 95 10

#Démarrer le service
sudo /etc/init.d/elasticsearch start

#### Logstash ####

curl -O https://download.elasticsearch.org/logstash/logstash/logstash-1.4.2.tar.gz
tar zxvf logstash-1.4.2.tar.gz
cd logstash-1.4.2

