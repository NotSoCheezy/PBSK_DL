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
        ep_title = item['title'].replace('/', '; ')
        print(show_name)
        print(air_date)
        print(ep_title)
        
        if not os.path.isdir(show_name):
            os.makedirs(show_name)
            
        if not os.path.isdir(os.path.join(show_name, collection)):
            os.makedirs(os.path.join(show_name, collection))
        
        str_dir = os.path.join(show_name, collection, f"{show_name} {air_date} - {ep_title}")
        
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
                if cap['format'] == 'SRT':
                    cc = cap['URI']
                    good_cc = True
                    break
            if not good_cc: raise LookupError
            print(cc)
            urllib.request.urlretrieve(cc, f"{str_dir}.srt")
        except:
            print("No valid srt!")
            raise
        
        print('\n')

###### DOWNLOAD JSON

print("Please type the name of the show in lowercase, replacing spaces with '-' and removing punctuation:")
print("Examples: 'cyberchase', 'lets-go-luna'")
show_name = input()

contents = urllib.request.urlopen(f"https://content.services.pbskids.org/v2/kidspbsorg/programs/{show_name}").read()
jcontent = json.loads(contents)

###### DOWNLOAD VIDEOS

do_clips = yes_no("Also download clips?")

jdownload(jcontent, 'episodes')
if do_clips: jdownload(jcontent, 'clips')
