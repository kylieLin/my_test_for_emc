# -*- coding:  utf-8 -*-
#!/usr/bin/python

import urllib, urllib2
import json
import logging

logging.basicConfig(level=logging.INFO, \
                    format='%(asctime)s  %(name)s  %(levelname)s  %(message)s', \
                    filename='testcase.log')
logger = logging.getLogger()

exist_lun = [] #the luns exist in array

    
def check_api_function():
    '''
    procedure-oriented
    1. create two lun with size=2
    2. create one lun with size = 3
    3. resize the last lun set size = 4
    4. retieve last lun size assert size == 4
    5. remove the last lun
    6. retrieve the last lun assert the lun not exist
    '''
    init_size1 = 2
    init_size2 = 3
    init_num =2
    re_size = 4

    check_api_create(init_size1, init_num) #step1
    logger.info("step1 complete.")
    check_api_create(init_size2) #step2
    logger.info("step2 complete.")

    check_api_resize(re_size) #step3
    logger.info("step3 complete.")

    check_api_retrive(re_size) #step4
    logger.info("step4 complete.")

    check_api_remove() #step5
    logger.info("step5 complete.")

    check_api_retrive(0) #step6
    logger.info("step6 complete.")
    


def check_api_create(init_size, init_num=1):
    '''
    complete step1 and step2
    '''
    global exist_lun 
    url_create = "http://localhost:8080/create_lun"
    create_data = {'size':init_size, 'number':init_num}
    create_resp = json.loads(post_req(url_create, create_data))
    
    logger.info('create lun resp %s' % create_resp)
    assert int(create_resp[1].keys()[0]) == 0 

    exist_lun += create_resp[0].keys()

    
def check_api_resize(re_size):
    '''
    complete step3
    '''
    global exist_lun 
    url_resize = "http://localhost:8080/resize_lun"
    resize_data = {'lunID':exist_lun[-1], 'size':re_size}
    resize_resps = json.loads(post_req(url_resize, resize_data))

    logger.info('resize lun resp %s' % resize_resps)
    assert int(resize_resps[1].keys()[0]) == 0


def check_api_retrive(size):
    '''
    complete step4
    '''
    global exist_lun 
    url_retrieve = "http://localhost:8080/retrieve_lun_size?lunID=%s" % exist_lun[-1]
    retrive_resp = json.loads(get_req(url_retrieve))

    logger.info('retrive lun resp %s' % retrive_resp)
    if size != 0:
        assert int(retrive_resp[0].values()[0]) == size
    else:
        assert retrive_resp[0] == {}

def check_api_remove():
    '''
    complete step5
    '''
    global exist_lun 
    url_remove = "http://localhost:8080/remove_lun"
    remove_data = {'lunID': exist_lun[-1]}
    remove_resp = json.loads(post_req(url_remove, remove_data))

    logger.info('remove lun resp %s' % remove_resp)
    assert int(remove_resp[0].keys()[0]) == 0
    
       
#POST
def post_req(url,data):
    test_data = data
    test_data_urlencode = urllib.urlencode(test_data)
    requrl = url
    req = urllib2.Request(url = requrl,data =test_data_urlencode)
    resp_data =urllib2.urlopen(req)
    return resp_data.read()


#GET
def get_req(url):
    req = urllib2.Request(url)
    resps = urllib2.urlopen(req)
    return resps.read() 

if __name__=="__main__":
    check_api_function()

