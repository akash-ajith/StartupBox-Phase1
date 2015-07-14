#!/usr/bin/env python
print('Content-type: text/html\r\n\r') 
print('<head> <title>Image Similarity Checker</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script> <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script> </head> <body> <nav class="navbar navbar-default"> <div class="container-fluid"> <div class="navbar-header"> <a class="navbar-brand" href="#">StartupBox Project</a> </div> </div> </nav> <div class="container"> <div class="jumbotron"> <h1>Compare Images</h1> <p>Compare two images and display the scale of similarity</p> </div>')
from math import sqrt
from urllib import urlretrieve
import os, re, string, sys
from PIL import Image, ImageChops
import cgitb
import cgi

cgitb.enable()
inputs = cgi.FieldStorage()

def get_ext(url):
    match = re.search(r'.[A-Za-z]+$', url)
    if match:
        return match.group()
    else:
        return ''

def rms(list):
    sum = 0

    for item in list:
        sum += item * item

    mean = sum/len(list)
    return sqrt(mean)

def size_adj(im1, im2):
    if im1.size > im2.size:
        im2 = im2.resize(im1.size, Image.BICUBIC)
    elif im2 > im1:
        im1 = im1.resize(im2.size, Image.BICUBIC)

    return im1, im2

def main():

    url1 = inputs['img1'].value
    url2 = inputs['img2'].value

    ext1 = get_ext(url1)
    ext2 = get_ext(url2)

    #print ext1
    #print ext2

    file1 = '/usr/lib/test/im1' + ext1
    file2 = '/usr/lib/test/im2' + ext2

    if string.upper(ext1) != string.upper(ext2):
        if (string.upper(ext1) == ".JPEG" or string.upper(ext1) == ".JPG"):

             urlretrieve(url1, file1)
             urlretrieve(url2, file2)
             im = Image.open(file1)
             file1 = '/usr/lib/test/im1' + '.png'
             im.save(file1)
        elif (string.upper(ext2) == ".JPEG" or string.upper(ext2) == ".JPG"):

             urlretrieve(url1, file1)
             urlretrieve(url2, file2)
             im = Image.open(file2)
             file2 = '/usr/lib/test/im2' + '.png'
             im.save(file2)

    else:

        urlretrieve(url1, file1)
        urlretrieve(url2, file2)


    diff_perc = []

    im1 = Image.open(file1)
    im2 = Image.open(file2)
 
    
    im1, im2 = size_adj(im1, im2) 
    difference = ImageChops.difference(im1, im2)
    print '<h2>Image 1</h2> <img src="' + url1 + '" alt="Image1" height="100" width="150" style="padding:1px;border:thin solid black;">'
    print '<br><h2>Image 2</h2> <img src="' + url2 + '" alt="Image2" height="100" width="150" style="padding:1px;border:thin solid black;">'
    if difference.getbbox() is None:
        print 'Same Image..! The images are 100% similar. Similarity Scale Rank - 100'
    else:
        pixels = difference.getdata() 


        pixel_rms = map(rms, pixels)
        for item in pixel_rms:
            diff_perc.append(item/255*100)
        avg_diff = sum(diff_perc)/len(diff_perc)
        similarity = 100 - avg_diff

        if avg_diff == 100:
            print '<h3>The images are completely different. Similarity Scale Rank - 0</h3>'
        else:
            print '<h3>The images are %.2f%% similar. Similarity Scale Rank - %.2f </h3>' %(similarity, similarity)
    os.system('rm ' + file1 + ' ' + file2)

main()
