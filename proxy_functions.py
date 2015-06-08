import re
from wand.image import Image
import urllib
import io
import requests
import os, random
import sys
from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless
import StringIO
from bs4 import BeautifulSoup,Tag
import linecache
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
def getsizes(image_data):
    p = Image.frombytes(image_data)
    return p.image.size
def resizeImg(sourceFile, width, height):                                                                                                                                                                                                                                       
    img = Image(filename=sourceFile)
    if width > height:
        img.transform(resize="%d" % (width))
    else:
        img.transform(resize="x%d" % (height))  
    wd = img.width - width
    hd = img.height - height
    img.crop(wd/2,0,width=width, height=height)
    img.format = 'jpeg'                                                                                                                                                                                                    
    return img
def replaceImage(flow):
    attrs = dict((x.lower(),y) for x, y in flow.response.headers)
    if "content-type" in attrs:
        if "image" in attrs['content-type'] and not "svg" in attrs['content-type']:
            if flow.response.code == 304:
                content = flow.response.content
            else:
                content = requests.get(flow.request.url).content
            if len(content) == 0:
                return flow
            try:
                img = Image(file=io.BytesIO(content))
                size = img.size
                if size[0] > 80 and size[1] > 80:
                    filename = random.choice(os.listdir("images"))
                    img = resizeImg("images/"+filename,size[0],size[1])
                    content = img.make_blob()
                    responseHeaders = ODictCaseless([('Content-Length',len(content))])
                    responseHeaders['Content-Type'] = ["image/jpg"]
                    resp = HTTPResponse([1,1], 200, 'OK', responseHeaders, content)
                    flow.response = resp

            except:
                PrintException()
    return flow
def censorText(flow, expressions,stylesheet,flags):
    stat = {"type":"statistic", "changes":[]}
    stat['url'] = flow.request.url
    attrs = dict((x.lower(),y) for x, y in flow.response.headers)
    if 'content-type' in attrs:
        if ('text/html' in attrs['content-type']):
            flow.response.headers['content-type'] = ["text/html"]
            if 'content-encoding' in flow.response.headers.keys():
                flow.response.content = flow.response.get_decoded_content()
                del flow.response.headers['content-encoding']
            page = BeautifulSoup(flow.response.get_decoded_content())
            for key,value in expressions:
                value_rand = "(neulandeuphonie)"+random.choice(value)+"(/neulandeuphonie)"
                for tag in page.findAll(text=re.compile(key, flags=flags)):
                    replace_data = replaceText(key,value_rand,unicode(tag.string),flags)
                    tag.string.replace_with(replace_data[0])
                    stat['changes'].append(replace_data[1])
            if page.head != None:
                new_tag = page.new_tag("style", type="text/css")
                new_tag.string = stylesheet
                page.head.append(new_tag)
            flow.response.content = str(page)
            flow.response.replace("\\(neulandeuphonie\\)","<span class=\"neulandeuphonie\">")
            flow.response.replace("\\(/neulandeuphonie\\)","</span>")
            #req = session.post("http://couchdb.pajowu.de/neulandeuphonie",data=json.dumps(stat),headers={'Content-type': 'application/json'})
    return flow
def replaceText(key, value, text, flags):
        subn_res = re.subn(key,value,text,flags=flags)
        text = subn_res[0]
        change_dict = None
        #print(subn_res)
        #replaces = flow.response.replace(key,value_rand, flags=re.IGNORECASE)
        if subn_res[1] > 0:
            words = re.findall(key,text,flags=flags)
            changes = {}
            for word in words:
                if word in changes:
                    changes[word] += 1
                else:
                    changes[word] = 1
            for change in changes:
                change_dict = {"word":"", "replaced_by":"", "count":"1"}
                change_dict['word'] = str(change)
                change_dict['replaced_by'] = str(value)
                change_dict['count'] = str(changes[change])
        return (text, change_dict)