#!/bin/bash

yum install -y httpd
sudo chkconfig httpd on
sudo service httpd start