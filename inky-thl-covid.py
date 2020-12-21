#
# inky-thl-covid.py
#
#
# Dimentsions can be found here:
#
#  * https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.dimensions.json
#
# THL Open Data API
#
# * https://thl.fi/fi/tilastot-ja-data/aineistot-ja-palvelut/avoin-data/varmistetut-koronatapaukset-suomessa-covid-19-
#
# This code is based on:
#
# * https://github.com/steichten/inky-covid.git
#
# License:
#
# * GPL-3
#

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image, ImageDraw, ImageFont
import argparse, io
from datetime import datetime, timedelta
from matplotlib import font_manager
from inkyphat import RED, BLACK, text, set_image, set_rotation, show
import inkyphat
from urllib.request import Request, urlopen  

# Create the parser
my_parser = argparse.ArgumentParser(description='inky-pHAT dashboard of weekly COVID-19 positives in Finland')

# Add the arguments
my_parser.add_argument('--area',
                       metavar='area',
                       type=str,
                       help='area code (eg. 445171 is Helsinki)')

my_parser.add_argument('--flip',
                       dest='flip',
                       action='store_true',
                       help='flip the display 180 degrees')
# Default to Flip
my_parser.set_defaults(flip=True)
# Defaults to Helsinki 
my_parser.set_defaults(area="445171")
my_parser.add_argument("--output", help="save plot as png")
# Execute the parse_args() method
args = my_parser.parse_args()


def GrabData(area):
	# We need to adjust user agent
	url = 'https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.csv?row=hcdmunicipality2020-{}.&column=dateweek2020010120201231-443686&filter=measure-444833'.format(area)
	req = Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
	content = urlopen(req)
	# API call
	df = pd.read_csv(content,sep=';')
	# File read (for development cycles)
	# df = pd.read_csv('test',sep=';')
	# Take totals and area name
	bottom = df.tail(1)
	total = bottom.iloc[0]['val']
	area = bottom.iloc[0]['Alue']
	# FIX THIS:
	df = df[:-3]
	return df, total, area

df,total,areaname=GrabData(args.area.lower())
df['val'] = df['val'].fillna(0)
df['val'].replace("..", 0, inplace=True)
x = df["Aika"]
y = df["val"]

myFmt = mdates.DateFormatter('%m-%d')
fig, ax = plt.subplots()
ax.plot(x,y)
ax.xaxis.set_major_formatter(myFmt)

# define inky-pHAT resolutiom
w, h = (212, 104)
dpi = 144
fig, ax = plt.subplots(figsize=(212/dpi, 104/dpi), dpi=dpi)

fig.subplots_adjust(top=1, bottom=0, left=0.45, right=.95)

ticks_font = font_manager.FontProperties(fname='font1.TTF', size=4)
plt.rcParams['text.antialiased'] = False
for label in ax.get_yticklabels() :
    label.set_fontproperties(ticks_font)
ax.yaxis.set_tick_params(pad=1, width=1)
ax.xaxis.set_ticks([])
ax.set_frame_on(False)
ax.plot(x,y) #,marker="o",markersize=2)
ax.xaxis.set_major_formatter(myFmt)
fig.autofmt_xdate()
ax.autoscale_view()

ymin, ymax = ax.get_ylim()

font = ImageFont.truetype('Cantarell-Bold.ttf', 14)
inkyphat.set_colour('red')

with io.BytesIO() as f:
    fig.savefig(f, dpi=dpi, pad_inches=0)
    f.seek(0)
    i = Image.open(f)#.convert('P', palette=(0,1,2))
    d = ImageDraw.Draw(i)

    set_image(i)
    if args.flip:
        set_rotation(180)

    text((0, 0), "Weekly", BLACK, font)
    text((0,15), "cases", BLACK, font)
    text((0,30),areaname,RED, font)
    text((0,45),'Total:',BLACK, font)
    text((0,60),'{}'.format(total), RED, font)
    text((0,85),'Source: THL',BLACK, font)

    show()

