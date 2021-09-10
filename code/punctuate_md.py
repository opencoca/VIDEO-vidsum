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

f = open("1.final.en.md","w")
f.writelines(["{}\n \n {}".format(block['image'], block['punctuated_text']) for block in block_list])
f.close()




#markdown image format
#![image title](/imagepath "image alt text")

#Save history in ipyhthon
#%save add_images_to_srt.py 1-99999


