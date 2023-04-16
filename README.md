<h1 align="center">CERBERUS PHISH</h1>



### [√] Description :

***A python phishing script for login phishing, image phishing, video phishing and many more***

### [+] Installation

##### Install primary dependencies (git, python)

 - For Debian (Ubuntu, Kali-Linux, Parrot)
    - ```sudo apt install git python3 php openssh-client -y```
 - For Arch (Manjaro)
    - ```sudo pacman -S git python3 php openssh --noconfirm```
 - For Redhat(Fedora)
    - ```sudo dnf install git python3 php openssh -y```
 - For Termux
    - ```pkg install git python3 php openssh -y```



##### Enter the directory
 - ```cd cerberusphish```

##### Install all modules
 - ```pip3 install -r files/requirements.txt```

##### Run the tool
 - ```python3 cerberusphish.py```

#### Or, directly run
```
wget https://raw.githubusercontent.com/kingfonpro/cerberusphish/main/cerberusphish.py && python3 cerberusphish.py

```

### Pip
 - `pip3 install cerberusphish` [For Termux]
 - `sudo pip3 install cerberusphish` [For Linux]
 - `cerberusphish`

### Docker

 - `sudo docker pull kingfonpro/cerberusphish`
 - `sudo docker run --rm -it kingfonpro/cerberusphish`

#### Options

```
usage: cerberusphish.py [-h] [-p PORT] [-t TYPE] [-o OPTION] [-T TUNNELER]
                     [-r REGION] [-S SUBDOMAIN] [-d DIRECTORY] [-f FEST]
                     [-i YTID] [-u URL] [-s DURATION] [--noupdate]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  CERBERUS PHISH's server port [Default : 8080]
  -t TYPE, --type TYPE  CERBERUS PHISH's phishing type index [Default : null]
  -o OPTION, --option OPTION
                        CERBERUS PHISH's template index [Default : null]
  -T TUNNELER, --tunneler TUNNELER
                        Tunneler to be chosen while url shortening [Default :
                        Cloudflared]
  -r REGION, --region REGION
                        Region for ngrok and loclx [Default: auto]
  -S SUBDOMAIN, --subdomain SUBDOMAIN
                        Subdomain for ngrok and loclx [Pro Account] (Default:
                        null)
  -d DIRECTORY, --directory DIRECTORY
                        Directory where media files will be saved [Default :
                        /sdcard/Media]
  -f FEST, --fest FEST  Festival name for fest template [Default: Birthday]
  -i YTID, --ytid YTID  Youtube video ID for yttv template [Default :
                        6hHmkInZkMQ (NASA Video)]
  -u URL, --url URL     Redirection url for ip-tracking or login phishing
                        [Default : null]
  -s DURATION, --duration DURATION
                        Media duration while capturing [Default : 5000(ms)]
  --noupdate            Skip update checking [Default : False]
```

### Features:

 - Multi platform (Supports most linux)
 - 100+ templates
 - Concurrent 4 tunneling (Ngrok, Cloudflared and LocalXpose, LocalHostRun)
 - OTP Support
 - Credentials mailing
 - Easy to use
 - Possible error diagnoser
 - Built-in masking of URL
 - Custom masking of URL
 - URL Shadowing
 - Portable file (Can be run from any directory)
 - Get IP Address and many other details along with login credentials


### Requirements

 - `Python(3)`
   - `requests`
   - `bs4`
 - `PHP`
 - `SSH`
 - 200MB storage
 
If not found, php, ssh and python modoules will be installed on first run

#### Tested on

 - `Termux`
 - `Ubuntu`
 - `Kali-Linux`
 - `Arch`
 - `Fedora`
 - `Manjaro`

## Usage

1. Run the script
2. Choose a Website
3. Wait sometimes for setting up all
4. Send the generated link to victim
5. Wait for victim login. As soon as he/she logs in, credentials will be captured


 
## [!] Disclaimer
***This tool is developed for educational purposes. Here it demonstrates how phishing works. If anybody wants to gain unauthorized access to someones social media, he/she may try out this at his/her own risk. You have your own responsibilities and you are liable to any damage or violation of laws by this tool. The author is not responsible for any misuse of CERBERUS PHISH!***

### This repository is open source to help others. So if you wish to copy, consider giving credit!

## [~] Find Me on :

- [![Github](https://img.shields.io/badge/Github-ImranTheThirdEye-green?style=for-the-badge&logo=github)](https://github.com/kingfonpro)

- [![Gmail](https://img.shields.io/badge/Gmail-ImranTheThirdEye-green?style=for-the-badge&logo=gmail)](mailto:githubking777@gmail.com)



