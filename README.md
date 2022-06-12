# Nani Monitoring
Small monitoring script in python for nani-games

## Installation
```bash
git clone https://github.com/david-prv/nani-monitoring.git monitor && cd monitor
pip install -r requirements.txt
```

## Commandline Args
> ``--repetitive`` or ``-r``:  
> Run the script in an endless loop (daemons)

> ``--suppress-emails`` or ``-s``:  
> Prevent update emails to be sent (useful for development)

## Run the Script
```bash
# in path/to/monitor/
python3 app.py [options]
```
  
We suggest using screen
```bash
screen -S monitor_runner python3 app.py -r
```
or setting up a cronjob
```bash
# for Ubuntu
sudo apt-get update && #apt-get upgrade
sudo nano /etc/crontab 

# Syntax:
# * * * * * /path/to/command arg1 arg2
# OR
# * * * * * /root/backup.sh
```

## Output
![image](https://user-images.githubusercontent.com/66866223/173231420-4565f77b-7665-42af-b16a-66b7f20643cf.png)
