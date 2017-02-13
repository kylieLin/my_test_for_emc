#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import string
import time

class lun(object):
    def __init__(self, array_id):
        '''
        init a lun
        '''
        self.id = str(int(time.time()*1000)) + '_'\
                      + ''.join(random.sample(string.digits, 4))
        self.array = array_id
        self.size = 0
        self.flag = '0'

    def assign_lun_space(self, size):
        '''
        set the lun size and return lun id
        '''
        if self.array.array_available_size < size:
            raise Exception, "there's no enought space"
        else:
            self.size = size
            if self.array.assign_space(self.id, size):  #分配存储空间
                return True
            else:
                return None
        
    def resize_lun(self, size):
        '''
        resize a lun size
        '''
        try:
            if not self.array.free_space(self.id):  
                print "free_space error when resize_lun"
                return None
            if not self.array.assign_space(self.id, size): 
                print "assigne_space error when resize_lun"
            self.size = size  
            return True
        except Exception, e:
            print e
            return None
            

    def get_lun_size(self):
        '''
        get lun size
        '''
        return self.size

    def get_lun_flag(self):
        '''
        return lun status
        '''
        return self.flag

    def set_lun_flag(self, flag):
        '''
        set lun status
        '''
        self.flag= flag
        return self.flag

    def free_lun_space(self):
        '''
        delete the lun
        '''
        if not self.array.free_space(self.id):
            print "free_lun_space error"
            return None
        else:
            return True
        


class array(object):
    '''
    array type
    '''
    def __init__(self, size):
        '''
        initilize a array
        '''
        self.array_size = size
        self.array_available_size = self.array_size
        self.array_available_unit = {self.array_size:0} #{space_lenth: start_index}
        self.array = [0 for i in xrange(self.array_size)]
        self.array_lun_info = {} #{id:(start_index, lenth)}
        self.array_luns = {}  #{id:object_lun}


    def assign_space(self, lunID, size):
        '''
        assign space to lun
        
        array_available_unit:it include the available space segment
        the key is segment lenth, value is start_index
        
        1.check if available_size < size, no enought space
        2.available_size > size
        a. get available segment
        b. sort these segment by lenth
        c. find the minimal segment that meet requirement_size
        d. assign space,update array_available_size info
        f. if the minimal segment left space,input the left space toarray_available_unit 
        
        '''
        size = int(size)
        
        if self.array_available_size < size:
            print "there is no enought space"
            return None
        else:
            available_spaces = sorted(self.array_available_unit.keys())
            
            if available_spaces[-1]  > size: #max available space < need size
                for item in available_spaces:
                    print "item:", item
                    if size <= item: 
                        self.array_lun_info[lunID]=(self.array_available_unit[item], size)  
                        #修改可用空间大小
                        self.array_available_size -= size
                        
                        #修改可用空间信息
                        if size < item: 
                            left_space = item - size
                            left_space_index = self.array_available_unit[item] + size
                            self.array_available_unit[left_space] = left_space_index
                        del(self.array_available_unit[item]) 
                        break
                return True
            
            else: 
                print "no enought space, please check"
                return None

            
    def free_space(self, lunID):
        '''
        free lun space to array
        '''
        if not lunID in self.array_lun_info:
            print "array_lun_info %s" % self.array_lun_info
            print "this lun not in array"
            return None

        free_index = self.array_lun_info[lunID][0]
        free_size = self.array_lun_info[lunID][1]
        

        #查找是否可将该空间合并
        k = 0
        for i in self.array_available_unit:
            if i + self.array_available_unit[i] == free_index:
                self.array_available_unit[i] += free_size
                break
            
            elif free_index + free_size == self.array_available_unit[i]:
                self.array_available_unit[free_size + i] = free_index #添加新元素
                del(self.array_available_unit[i]) #删除合并前的空间
                break

            k += 1 #遍历计数
            
        if k == len(self.array_available_unit): 
            #遍历所有元素，没有找到可合并元素
            self.array_available_unit[free_size] = free_index

        self.array_available_size +=  free_size  #增加可用空间计数   
        del(self.array_lun_info[lunID]) #删除lun信息
        return True

##if __name__ =='__main__':
##    my_array = array(20)
##    print my_array.array_size, my_array.array_available_size, \
##          my_array.array_available_unit,my_array.array_lun_info
##    my_lun1 = lun(my_array)
##    my_lun1.assign_lun_space(2)
##    print my_lun1.id,my_lun1.flag, my_lun1.size
##    print my_array.array_size, my_array.array_available_size, \
##          my_array.array_available_unit,my_array.array_lun_info
##    my_array.free_space(my_lun1.id)
##    print my_array.array_size, my_array.array_available_size, \
##          my_array.array_available_unit,my_array.array_lun_info
    
                    
                    
            
            
                        
                        
            
