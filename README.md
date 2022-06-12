# Nani Monitoring
Small monitoring script in python for nani-games using statuspage.io automation email routes

## Installation
```bash
git clone https://github.com/david-prv/nani-monitoring.git monitor && cd monitor
pip install -r requirements.txt
cp example.env .env
rm example.env
```
Open and edit ``.env``. Update environment variables with your credentials/routes/settings:
```bash
# for Ubuntu
nano .env
```

## Commandline Args
> ``--repetitive`` or ``-r``:  
> Run the script in an endless loop (daemons)

> ``--suppress-emails`` or ``-s``:  
> Prevent update emails to be sent (useful for development)

> ``--turnus <seconds>`` or ``-t <seconds>``:  
> Specifiy turnus in seconds, if repetitive mode is enabled (overrides env variable)
  
> ``--help`` or ``-h`` (Alias: ``--manual`` or ``-m``):  
> Shows script usage and quits

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
# * * * * * /path/to/monitor/app.py [options] 
```

## Screenshots
<details>
  <summary>Help message / Manual</summary>
  ![image](https://user-images.githubusercontent.com/66866223/173252187-30fea965-08b9-4e43-9c2b-456d841ce59c.png)
</details>
<details>
  <summary>Coloured activity log</summary>
  ![image](https://user-images.githubusercontent.com/66866223/173231420-4565f77b-7665-42af-b16a-66b7f20643cf.png)
</details>
<details>
  <summary>Suppressed activitiy log</summary>
  ![image](https://user-images.githubusercontent.com/66866223/173252249-11aaeb0c-7d11-4392-b9a2-5c17beaeb10c.png)
</details>

