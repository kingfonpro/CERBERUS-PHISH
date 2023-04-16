# Dockerfile

# Author       : KING
# Github       : https://github.com/kingfonpro
# Telegram    : https://t.me/king_fon
# Email        : githubking777@gmail.com
# Date         : 08-09-2022
# Main Language: Python

# Download and import main images

# Operating system
FROM debian:latest
# Main package
FROM python:3

# Author info
LABEL MAINTAINER="https://github.com/kingfonpro/CERBERUS-PHISH"

# Working directory
WORKDIR CERBERUS PHISH/
# Add files
ADD . /'CERBERUS-PHISH'

# Installing other packages
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install php openssh-client -y
RUN pip3 install requests bs4
RUN apt-get clean

# Main command
CMD ["python3", "cerberusphish.py", "--noupdate"]
