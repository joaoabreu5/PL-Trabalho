def verify_NOT(t):
    r = None
    if t == 'any' or t == 'boolean':
        r = 'boolean'
    return r

def verify_UNARY_NUM_OP(t):
    r = None
    if t == 'any' or t == 'num':
        r = 'num'
    return r

def verify_BIN_NUM_OP(t1, t2):
    r = None
    if (t1 == 'any' or t1 == 'num') and (t2 == 'any' or t2 == 'num'):
        r = 'num'
    return r

def verify_COLON(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')
    
    if t2 == 'list':
        r = 'list_' + t1
        
    elif t2_list_count == t1_list_count + 1:
        t1_list_type = t1[t1_list_count*5:]
        t2_list_type = t2[t2_list_count*5:]
        
        if t1_list_type == t2_list_type:
            r = t1_list_type
        
        elif t1_list_type == 'any':
            r = t2_list_type
        
        elif t2_list_type == 'any':
            r = t1_list_type
            
    return r
                        
def verify_CONCAT(t1, t2):
    pass
        