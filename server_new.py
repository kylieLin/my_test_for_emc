#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging
import bottle
from bottle import route, run, request, abort, response

from test3 import lun, array


logging.basicConfig(level=logging.INFO, \
                    format='%(asctime)s  %(name)s  %(levelname)s  %(message)s', \
                    filename='my_service.log')
logger = logging.getLogger()


my_array = array(20)


@bottle.route('/create_lun', method='POST')
def create_lun():
    '''
    create one or multiple lun
    '''
    
    postValue = request.POST.decode('utf-8') #read params
    size = int(request.POST.get('size'))
    number = int(request.POST.get('number')) or 1
    
    ids = {}
    for i in xrange(number): 
        my_lun = lun(my_array)
        if not my_lun.assign_lun_space(size): #assign space for a lun
            logger.info("create a lun error")
            return json.dumps([ids, {-4:"assign lun space error"}])
        
        else:
            my_array.array_luns[my_lun.id] = my_lun #update array info
            ids[my_lun.id] = my_lun.size
            logger.info("create lun success, lun id %s" %my_lun.id)
            
    return json.dumps([ids, {0: "success"}])


@bottle.route('/resize_lun', method='POST')
def resize_lun():
    '''
    update the size of a lun
    '''
    postValue = request.POST.decode('utf-8')
    lunID = request.POST.get('lunID')
    size = int(request.POST.get('size'))

    #check lun not in array
    if not lunID in my_array.array_luns:
        logger.info("argument error, my array don'thave the lun %s" %lunID)
        return json.dumps([{},{-1:"lun not exist"}])
    
    #lun in array
    else:
        lun = my_array.array_luns[lunID]
        if not lun.flag == '0':
            return json.dumps([{}, {-3:"the lun a in use"}])
        else:
            lun.set_lun_flag('1')
            try:
                lun.resize_lun(size)
                lun.set_lun_flag('0')
                return json.dumps([{lun.id: lun.size},{0: "success"}])
            except Exception,e:
                lun.set_lun_flag('0')
                logger.error("%s" % e)
                return json.dumps([{},{-5,"resize failed"}])
            

@bottle.route('/remove_lun', method='POST')
def remove_lun():
    '''
    delete a lun, free the lun space and remove the lun from array
    '''
    #get params
    postValue = request.POST.decode('utf-8')
    lunID = request.POST.get('lunID')

    #check lun not in array
    if not lunID in my_array.array_luns:
        logger.info("the lun %s not exist" % lunID)
        return json.dumps([{},{-1, 'lun not exist'}])

    #un in array
    else:
        lun = my_array.array_luns[lunID]
        if not lun.flag == '0':
            return json.dumps([{},{-3:'the lun is using'}])
        elif lun.free_lun_space():
            del(my_array.array_luns[lunID])
            return json.dumps([{0: 'success'}])
        else:
            logger.info("free_lun_space error")
            return json.dumps([{-5: "remove lun error"}])


@bottle.route('/retrieve_lun_size', method='GET')
def retrieve_lun_size():
    '''
    get size of a lun
    '''
    lunID = request.query.lunID

    #lun not in array                          
    if not lunID in my_array.array_luns:
        logger.info("the lun %s not exist" % lunID)
        return json.dumps([{},{-1: 'lun not exist'}])

    #lun in array                          
    else:
        lun = my_array.array_luns[lunID]                      
        if not lun.flag == '0':
            return json.dumps([{},{-3:'the lun is using'}])                     
        else:
            lun.set_lun_flag('1')
            lun_size = lun.get_lun_size()
            lun.set_lun_flag('0')
            return json.dumps([{'size':lun_size}, {0: 'success'}])

        
@bottle.route('/persistece', method='GET')
def persistece():
    '''
    write the array info to files
    '''
    array_luns = json.dumps(my_array.array_luns)
    array_lun_info = json.dumps(my_array.array_lun_info)
    try:
        f1 = open('array_luns.txt', 'w')
        f1.write(array_luns)
        f1.close()
    except Exception,e:
        logger.info(e)
    try:
        f2 = open('array_lun_info.txt', 'w')
        f2.write(array_lun_info)
        f2.close()
    except Exception,e:
        logger.info(e)
    return json.dumps({'0':'success'})



run(host='127.0.0.1', port=8080)
