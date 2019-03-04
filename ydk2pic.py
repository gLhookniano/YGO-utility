#!/usr/bin/python
#coding:utf-8

import re
import glob
import os
from io import BytesIO
from lxml import etree
from PIL import Image
import requests


headers={
	'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4',
	'Referer' : 'https://www.bing.com/',
	'Accept' : '*/*'
    }
picture_loc = r'./Pictures/'
url0 = 'http://www.orenoturn.com/?mode=srh&cid=&keyword='
url1_xapth = r"//div[@class='name']//@href"
url_img_xpath = r"//img[@class='main_img']/@src"
resize_cm = (5.75, 8.45)
loc_ygopro=r'C:\Users\admin\AppData\Roaming\MyCardLibrary\ygopro'


def parse_ydk(file_ydk):
    """ 
    Read .ydk file, to get deck list

    Return:
        dict : key is card number in ygopro, value is the present in this .ydk file. (the number in the deck)
    """
    d_card_num={}
    card_num=0
    with open(file_ydk, 'r') as fp:
        l=fp.readlines()
        l.sort()
        for i in l:
            j=re.search(r'[0-9]*', i).group()
            if not j:
                continue
            if j != card_num:
                d_card_num[j]=1
                card_num=j
            elif j==card_num:
                d_card_num[j]+=1
    return d_card_num
    
def get_xpath(content, xpath, encode='utf-8', flag_local=None):
    """
    Use lxml with xpath parse html.
    """
    if not flag_local:
        content.encoding = encode
        selector = etree.HTML(content.text)
    if flag_local:
        selector = etree.HTML(content.read())
    
    elem = selector.xpath(xpath)
    return elem

def get_image(d_card_num, pic_loc=picture_loc):
    """
    Get image from orenoturn.com, if not fund, then use local ygopro image.
    """
    l_noPict=[]
    for i in d_card_num.keys():
        r = requests.get(url0+i, headers=headers)
        url1 = get_xpath(r, url1_xapth)
        if len(url1)<1:#if not picture
            print('not found :', i, 'num :', d_card_num[i])
            l_noPict.append((i,d_card_num[i]))
            continue
        if type(url1)==list:#get scd paper
            r1 = requests.get('http://www.orenoturn.com'+url1[0], headers=headers)
        else:
            r1 = requests.get('http://www.orenoturn.com'+url1, headers=headers)
        url_im = get_xpath(r1, url_img_xpath)
        if type(url_im)==list:#normally img_url
            url_im = 'http://' + re.search(r'img.*', url_im[0]).group()
        else:
            url_im = 'http://' + re.search(r'img.*', url_im).group()
        r2 = requests.get(url_im, headers=headers)
        
        im = Image.open(BytesIO(r2.content))
        dpi = cov_cm2dpi(resize_cm, ogi_px=im.size)
        num=d_card_num[i]
        while num>0:
            out=pic_loc+i+'_'+str(num)+".jpg"
            im.save(out, dpi=dpi)
            num-=1
    return l_noPict
    
def deal_noPict(l_noPict, pic_loc):
    """
    If not fund image on internet, then, use ygopro local picture.
    """
    loc_ygopro_pic = loc_ygopro + r'\pics/'
    for i in l_noPict:
        num=i[1]
        while num>0:
            resize_pic(loc_ygopro_pic+i[0]+'_'+str(num)+".jpg", pic_loc)
            num-=1
    
def cov_cm2dpi(resize_cm, ogi_px, i2cm=2.54):
    """
    Convert download image from inch to cm.
    """
    w_cm = resize_cm[0]
    h_cm = resize_cm[1]
    w_dpi = int(ogi_px[0]*i2cm/w_cm)
    h_dpi = int(ogi_px[1]*i2cm/h_cm)
    return (w_dpi, h_dpi)
    
def resize_pic(pic_src_loc, pic_dst_loc=None, resize_cm=8.54, i2cm=2.54):
    im = Image.open(pic_src_loc)
    dpi = cov_cm2dpi(resize_cm, ogi_px=im.size, i2cm=i2cm)
    if not pic_dst_loc:
        pic_dst_loc=pic_src_loc
    im.save(pic_dst_loc, dpi=dpi)
    
def chydk():
    '''
    change all current path .ydk file to picture in ydk-file-name document
    '''
    l_ydk = glob.glob("./*.ydk")
    l_noPict_card_num=[]
    
    for obj in l_ydk:
        pic_loc = picture_loc + re.match(r'(.*)[.]ydk', obj).group(1) +'/'
        if not os.path.isdir(pic_loc):
            os.mkdir(pic_loc)
            
        l_card_num = parse_ydk(obj)
        l_noPict_card_num = get_image(l_card_num, pic_loc=pic_loc)
        deal_noPict(l_noPict_card_num, pic_loc=pic_loc)
    

def chjpg(resize_cm=resize_cm):
    '''
    change all current path jpg size(cm)
    '''
    l_jpg = glob.glob("./*.jpg")
    for obj in l_jpg:
        resize_pic(obj, None, resize_cm)
        
if __name__ == '__main__':
    chydk()
    #chjpg()
    
    
    