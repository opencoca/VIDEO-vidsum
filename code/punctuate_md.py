# coding: utf-8
import requests
import re

# Define regular expression to detect sentances
p = re.compile(r'(?<=[\.\?!]\s)(\w+)')

from pprint import pprint

#set punctuation API url for use with requests
punctuate_api_endpoint = "http://bark.phon.ioc.ee/punctuator"

#Open the markdown file so we can punctuate it
my_file = open("1.en.md")
content = my_file.read()
my_file.close()

#Seperate the markdown doc into a list of lists
seperator = "![]"
result = [seperator+item for item in content.split(seperator)]
#remove leading seperators
block_list = [" ".join(block.split("\n")).split("    ") for block in result]
# Add null image for frist block in block_list
block_list[0]=[None] + block_list[0]
#convert block list into list of dictionaries

block_list = [{"image": block[0], "text": block[1]} for block in block_list]

# Python code to merge dict using update() method
def merge(dict1, dict2):
    return(dict1.update(dict2))

def punctuate(text, url= punctuate_api_endpoint ):
    data = {"text": text}
    punctuated_text = requests.post(url, data=data).text
    if punctuated_text[-2] == ".":
        return {"punctuated_text" : punctuated_text}
    else:
        #as the text doesn't end in a period we should split the sentance stubb off
        fragment = punctuated_text.split(".")[-1]
        punctuated_text = ".".join([text for text in  punctuated_text.split(".")[0:-1]])
        return {"punctuated_text": punctuated_text +"." , "fragment": fragment}

def cap(match):
    return(match.group().capitalize())

def defragment_text(blocks):
    for item in range(len(blocks)):
        next_item = item+1
        merge(blocks[item], punctuate(blocks[item]['text']))
        if('fragment' in blocks[item] and next_item < len(blocks)):
            blocks[next_item]['text'] = "{} {}".format(blocks[item]['fragment'], blocks[next_item]['text'])
        else:
            blocks[item]['punctuated_text'] = p.sub(cap, blocks[item]['punctuated_text'])
        if next_item == len(blocks):
            break

# Defragment and punctuate the blocks of text
defragment_text(block_list)

block_list[0] = {
    'image': '',
    'text': block_list[0]['text'],
    'punctuated_text': p.sub(cap, block_list[0]['punctuated_text'][4:].capitalize())
}

formated_text = ["{}\n\n{}\n\n".format(block['image'], block['punctuated_text']) for block in block_list]
formated_text = [block.replace(" i "," I ") for block in formated_text]
formated_text = [block.replace(" i'm "," I'm ") for block in formated_text]
formated_text = [block.replace(" I'De"," I'de") for block in formated_text]
formated_text = [block.replace("\'S ","\'s ") for block in formated_text]
formated_text = [block.replace("\'Ve ","\'ve ") for block in formated_text]
formated_text = [block.replace("\'Re","\'re") for block in formated_text]
formated_text = [block.replace(" tor "," Tor ") for block in formated_text]
formated_text = [block.replace("\n.\n","\n\n") for block in formated_text]


f = open("1.final.en.md","w")
f.writelines( formated_text )
f.close()




#markdown image format
#![image title](/imagepath "image alt text")

#Save history in ipyhthon
#%save add_images_to_srt.py 1-99999


