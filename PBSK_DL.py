"""
    PBSK_DL by NotSoCheezyTech
    Copyright (C) 2021  Cassandra Leo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import urllib.request
import json
import os

###### FUNCTIONS

def yes_no(question):
    while(True):
        resp = input(f"{question} (y/n): ")
        if resp == 'y': return True
        elif resp == 'n': return False

def jdownload(jcontent, collection):
    for item in jcontent['collections'][collection]['content']:
        print("Downloading...")
        show_name = item['program']['title']
        air_date = item['air_date'][0:10]
        ep_title = item['title'].replace('/', '; ').replace(': ', '_').replace('?', '').replace('\\', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
        print(show_name)
        print(air_date)
        print(ep_title)
        
        if not os.path.isdir(show_name):
            os.makedirs(show_name)
            
        if not os.path.isdir(os.path.join(show_name, collection)):
            os.makedirs(os.path.join(show_name, collection))
        
        str_dir = os.path.join(show_name, collection, f"{air_date} - {ep_title}")
        
        print("from:")
        try:
            mp4 = item['mp4']
            print(mp4)
            urllib.request.urlretrieve(mp4, f"{str_dir}.mp4")
        except:
            print("No valid mp4!")
            raise
        
        try:
            good_cc = False
            for cap in item['closedCaptions']:
                if cap['format'] == 'WebVTT':
                    cc = cap['URI']
                    good_cc = True
                    break
            if not good_cc: raise LookupError
            print(cc)
            urllib.request.urlretrieve(cc, f"{str_dir}.vtt")
        except:
            print("No valid vtt!")
            raise
        
        print('\n')

###### DOWNLOAD JSON

print("PBSK_DL  Copyright (C) 2021  NotSoCheezyTech\nThis program comes with ABSOLUTELY NO WARRANTY; for details see license.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; see license for details.")
print("Please type the name of the show in lowercase, replacing spaces with '-' and removing punctuation:")
print("Examples: 'cyberchase', 'lets-go-luna'")
show_name = input()

contents = urllib.request.urlopen(f"https://content.services.pbskids.org/v2/kidspbsorg/programs/{show_name}").read()
jcontent = json.loads(contents)

###### DOWNLOAD VIDEOS

if yes_no("Also download clips?"):
    jdownload(jcontent, 'clips')

jdownload(jcontent, 'episodes')
