#!/bin/bash
cd /tmp
wget https://dl.google.com/go/go1.14.1.linux-amd64.tar.gz
tar xvzf go1.14.1.linux-amd64.tar.gz
mv go /usr/local/
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
go get github.com/OJ/gobuster
go get github.com/tomnomnom/assetfinder
go get github.com/tomnomnom/html-tool
go get github.com/tomnomnom/httprobe
go get github.com/tomnomnom/meg
go get github.com/tomnomnom/waybackurls
