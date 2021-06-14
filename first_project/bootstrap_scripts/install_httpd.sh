#!/bin/bash

#
# Manually install SSM Agent on Amazon Linux 2 instances.
# Reference: https://docs.aws.amazon.com/systems-manager/latest/userguide/agent-install-al2.html
#
sudo yum install -y https://s3.us-east-1.amazonaws.com/amazon-ssm-us-east-1/latest/linux_arm64/amazon-ssm-agent.rpm

# install Httpd server
yum install -y httpd
sudo chkconfig httpd on
sudo service httpd start