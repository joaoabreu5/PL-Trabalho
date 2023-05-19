def f_ex_(arg0, arg1, arg2, arg3):
	if len(arg0) >= 1:
		if arg3 == True:
			x = arg0[0]
			xs = arg0[1:]
			c = arg1
			a = arg2
			return x * 1
			
		elif arg3 == False:
			y = arg0[0]
			ys = arg0[1:]
			d = arg1
			b = arg2
			return d * 2
			
		else:
			raise ValueError
		
	else:
		raise ValueError
	

def f_maisum_(arg0):
	x = arg0
	return x + 1
	

def f_sumf_(arg0):
	if len(arg0) >= 1:
		x = arg0[0]
		xs = arg0[1:]
		return x + f_sumf_(xs)
		
	elif len(arg0) == 0:
		return 0
		
	else:
		raise ValueError
	

def f_soma_impares_(arg0):
	if len(arg0) >= 1:
		x = arg0[0]
		xs = arg0[1:]
		if x % 2 == 1:
			return x + f_soma_impares_(xs)
		else:
			return f_soma_impares_(xs)
		
	elif len(arg0) == 0:
		return 0
		
	else:
		raise ValueError
	

def f_filtra_impares_(arg0, arg1, arg2):
	if len(arg0) >= 2:
		if arg1 == 2:
			if arg2 == 5:
				x = arg0[0]
				y = arg0[1]
				xs = arg0[2:]
				if not (x % 2 == 0):
					return f_filtra_impares_(xs)
				else:
					return [x] + f_filtra_impares_(xs)
				
			else:
				raise ValueError
			
		else:
			raise ValueError
		
	elif len(arg0) >= 1:
		if arg1 == 3:
			if arg2 == 5:
				x = arg0[0]
				xs = arg0[1:]
				if not (x % 2 == 0):
					return f_filtra_impares_(xs)
				else:
					return x + f_filtra_impares_(xs)
				
			x = arg0[0]
			xs = arg0[1:]
			a = arg2
			if not (x % 2 == 0):
				return f_filtra_impares_(xs)
			else:
				return x + f_filtra_impares_(xs)
			
		else:
			raise ValueError
		
	elif len(arg0) == 0:
		if arg1 == 2:
			if arg2 == 1:
				return []
				
			a = arg2
			return []
			
		elif arg1 == 3:
			if arg2 == 1:
				return []
				
			else:
				raise ValueError
			
		else:
			raise ValueError
		
	else:
		raise ValueError
	

def f_soma_impares_2_(arg0):
	x = arg0
	return f_sumf_(f_filtra_impares_(x))
	

def f_idF_(arg0):
	a = arg0
	return a
	

def f_func_const_():
	return [1, 3, 4, 6]

def f_mult_list_Num_(arg0, arg1, arg2):
	if len(arg0) == 0:
		if arg2 == 2:
			i = arg1
			return []
			
		a = arg1
		x = arg2
		return [a * x] + f_mult_list_Num_([], a, x - 1)
		
	else:
		raise ValueError
	

def f_nzp_(arg0):
	a = arg0
	if a > 0:
		return 1
	else:
		if a == 0:
			return 0
		else:
			return a
	

def f_fib_(arg0):
	if arg0 == 0:
		return 1
		
	elif arg0 == 1:
		return 1
		
	n = arg0
	return f_fib_(n - 1) + f_fib_(n - 2)
	

def f_maximo_(arg0, arg1):
	if len(arg0) >= 1:
		x = arg0[0]
		xs = arg0[1:]
		b = arg1
		return f_maximo_(x, f_maximo_(xs))
		
	elif len(arg0) == 0:
		a = arg1
		return - 3 + 5 - 2
		
	else:
		raise ValueError
	

def f_ordF_(arg0):
	if len(arg0) >= 2:
		x = arg0[0]
		y = arg0[1]
		xs = arg0[2:]
		return x <= y and f_ordF_([y] + xs)
		
	elif len(arg0) >= 1:
		x = arg0[0]
		xs = arg0[1:]
		return True and False
		
	elif len(arg0) == 0:
		return True
		
	else:
		raise ValueError
	

def f_concatena_(arg0, arg1):
	if len(arg0) >= 1:
		x = arg0[0]
		xs = arg0[1:]
		ys = arg1
		return f_mult_(ys)
		
	x = arg0
	ys = arg1
	return [x] + f_concatena_([], ys)
	

def f_mult_(arg0, arg1):
	a = arg0
	b = arg1
	return a * b
	



x = 4
y = f_idF_(x)
print(y)
l = [1, 2, 3, 4, 5]
sum_l = f_sumf_(l)
print(sum_l)

