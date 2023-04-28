def verify_UNARY_BOOL_OP(t):
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

def verify_BIN_BOOL_OP(t1, t2):
    r = None
    if (t1 == 'any' or t1 == 'boolean') and (t2 == 'any' or t2 == 'boolean'):
        r = 'boolean'
    return r

def verify_BIN_COMPARE_OP(t1, t2):
    r = verify_EQUALTYPE(t1,t2)
    
    if r != None:
        r = 'boolean'
    return r

def verify_COLON(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')
    
    if t1 == 'any':
        if t2 == 'any':
            r = 'any'
        elif t2_list_count > 0:
            r = t2
    elif t2 == 'any':
        if t1 == 'any':
            r = 'any'
        else:
            r = 'list_'+t1
    elif t2_list_count == t1_list_count + 1:
        t1_list_type = t1[t1_list_count*5:]
        t2_list_type = t2[t2_list_count*5:]
        
        if t1_list_type == t2_list_type:
            r = t2
        elif t2_list_type == '':
            r = 'list_'+t1
            
    return r
                        
def verify_CONCAT(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')
    
    if t1 == 'any':
        if t2 == 'any':
            r = 'any'
        elif t2_list_count > 0:
            r = t2
    elif t2 == 'any':
        if t1 == 'any':
            r = 'any'
        elif t1_list_count > 0:
            r = t1
    elif t2_list_count == t1_list_count:
        r = verify_EQUALTYPE(t1,t2)
        
    
    return r

def verify_EQUALTYPE(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')

    if t1 == 'any':
        r = t2
    elif t2 =='any':
        r=t1
    elif t1_list_count == t2_list_count:
        t1_list_type = t1[t1_list_count*5:]
        t2_list_type = t2[t2_list_count*5:]
        if t1_list_type == t2_list_type:
            r = t1
        elif t1_list_type == '':
            r = t2
        elif t2_list_type == '':
            r = t1
    return r        


def verify_ERROR(t, line, col):
    if t == None:
            raise TypeError(f'Type error at line {line}, column {col}')
    
