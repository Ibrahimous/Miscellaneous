FROM centos

VOLUME /var/lib/mysql

RUN yum -y install wget
RUN wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
RUN rpm -ivh mysql-community-release-el7-5.noarch.rpm

RUN yum -y install mysql-server
RUN touch /etc/sysconfig/network

EXPOSE 3306
