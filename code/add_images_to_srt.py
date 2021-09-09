# coding: utf-8
from pprint import pprint

my_file = open("1.en.srt")
srt_content = my_file.read()
my_file.close()

srt_segment_list = [segment for segment in srt_content.split("\n") if segment]
srt_segments = list(zip(srt_segment_list[0::3],srt_segment_list[1::3],(srt_segment_list[2::3])))
srt_segments = [list(segment) for segment in srt_segments]

def list_of_tuples(a, b):
    return list(map(lambda x, y:(x,y), a, b))

def time_to_seconds(time):
    time = time.split(":")
    hour_seconds = int(time[0])*60*60
    minute_seconds = int(time[1])*60
    seconds = float(time[2].replace(',', '.'))
    seconds = hour_seconds + minute_seconds + seconds
    return seconds

images = get_ipython().getoutput('ls -1 *.jpg')

[time.strip() for time in srt_segments[3][1].split("-->")]

splits = [segment[1].split("-->") for segment in srt_segments][-1][-1].strip()

image_times = [file[:7] for file in images]


for index, segment in enumerate(srt_segments):
    for image_index, image in enumerate(images):
        times = [time.strip() for time in segment[1].split("-->")]
        times = [time_to_seconds(time) for time in times]
        if times[0] < float(image[0:-4]) < times[1]:
            image_string = '![]({} "image alt text")'.format(image)
            srt_segments[index][2] = "{} \n{} \n ".format(segment[2],image_string)

f = open("1.en.md","w")
f.writelines(["{}\n".format(segment[2]) for segment in srt_segments])
f.close()

#for num in nums
#for i, j in zip(my_list,my_list[1:])
# if i<image[:7] <j

#markdown image format
#![image title](/imagepath "image alt text")

#Save history in ipyhthon
#%save add_images_to_srt.py 1-99999


