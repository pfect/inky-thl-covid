# inky-thl-covid

* This covid dashboard is based on: https://github.com/steichten/inky-covid

Weekly covid cases dashboard from [THL's open data](https://yhteistyotilat.fi/wiki08/display/THLKA/The+description+of+THL%27s+open+data+API) API in Finland. 

# installation

This used python 3.7 and the [inky-phat libraries](https://github.com/pimoroni/inky-phat)

```
curl https://get.pimoroni.com/inkyphat | bash
sudo apt-get install libatlas-base-dev
pip3 install -r requirements.txt
```

# usage

```
usage: inky-thl-covid.py [-h] [--area area] [--flip] [--output OUTPUT]

inky-pHAT dashboard of weekly COVID-19 positives in Finland

optional arguments:
  -h, --help       show this help message and exit
  --area area      area code (eg. 445171 is Helsinki)
  --flip           flip the display 180 degrees
  --output OUTPUT  save plot as png
```

```
python3 inky-thl-covid.py
```
# license
GPL-3

# repository

https://github.com/pfect/inky-thl-covid.git
