# Call Flooding Discord Bot

Request by a discord user to flood scammer's call centers

# Setup for CentOS 7

1. Install dependencies to build python from source
```bash
sudo yum -y install epel-release
sudo yum -y update
sudo reboot
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel xz-devel
sudo yum -y install wget git nano
```

2. Build python from source
```bash
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
tar xvf Python-3.8.12.tgz
cd Python-3.8*/
./configure --enable-optimizations
sudo make altinstall
```

3. Check for successfull installation

- python
```
python3.8 --version
```

- pip
```
pip3.8 --version
```

4. Setting up the call flooding script

```bash
git clone https://github.com/hirusha-adi/Call-Flooding-Discord-Bot.git
cd ./Call-Flooding-Discord-Bot
pip3.8 install -r requirements.txt
```

5. Setup the discord bot token
    1. Create `token.txt`
    ```bash
    nano token.txt
    ```
    2. Paste your token
    3. Save and exit


6. (OPTIONAL) - Edit the config file to fit for your needs

7. Start the discord bot

1. Start as background process
```
python3.8 main.py &
```

2. detacth to host shell

```
disown -h
```






