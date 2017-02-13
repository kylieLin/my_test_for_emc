#coding:utf-8

##Test 1
##
## 
##
##Write a program to reverse every k nodes of a linked list.
##
##If the list size is not a multiple of k, then leave the remainder nodes as is.
##
## 
##
##Example:
##
##Inputs:  1->2->3->4->5->6->7->8->NULL and k = 3 
##
##Output:  3->2->1->6->5->4->7->8->NULL

def reverse_list(my_list, k):
    '''
    reverse every k nodes of my_list
    k > 0 and must be an int
    '''
    
    if not isinstance(k,int):
        print 'k must be an int'
        return None
    elif k <= 0:
        print 'k must bigger than 0.'
        return None
    elif k == 1:
        return my_list

    list_lenth = len(my_list)
    if list_lenth < k:
        return my_list
    quotient = list_lenth // k
    remainder = list_lenth % k
    new_list = []
    for i in range(quotient):
        tmp_list = my_list[i*k : (i+1) * k]
        tmp_list.reverse()
        new_list = new_list + tmp_list
    if remainder != 0:
        new_list = new_list + my_list[quotient*k ::]
    return new_list


a_list = [i for i in range(1,10)]
print a_list
assert reverse_list(a_list, 1.1) == None
assert reverse_list(a_list, -2) == None
assert reverse_list(a_list, 1) == [i for i in range(1,10)]
assert reverse_list(a_list, 2) == [2,1,4,3,6,5,8,7,9]
