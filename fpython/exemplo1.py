"""FPY

deff ex{
    case (x:xs,c,a,True) = y * 1;
    case (y:ys,d,b,False) = b * 2;
}

deff maisum{
    case(x) = x+1;
}

deff sumf
{
    case ([]) = 0;
    case (x:xs) = x + sumf(xs); 
}

deff soma_impares
{
    case ([]) = 0;
    case (x:xs) = if x%2 == 1 then x + soma_impares(xs) else soma_impares(xs);
}

deff filtra_impares
{
    
    case ([],2,a) = [];
    case ([],2,1) = [];
    case ([],3,1) = [];
    case (x:y:xs,2,5) = if ! (x % 2 == 0) then filtra_impares(xs) else x : filtra_impares(xs);
    case (x:xs,3,5) = if ! (x % 2 == 0) then filtra_impares(xs) else x ++ filtra_impares(xs);
    case (x:xs,3,a) = if ! (x % 2 == 0) then filtra_impares(xs) else x ++ filtra_impares(xs);
}


deff soma_impares_2{
    case(x) = sumf . filtra_impares(x);
}



deff idF
{
    case (a) = a;
}

deff func_const
{
    case() = [1,3,4,6];
}

deff mult_list_Num
{
    case ([],i,2) = [];
    case ([],a,x) = i*x : mult_list_Num([],i,x-1);
    case ([],a,v) = i*v : mult_list_Num([],i,x-1);
    case ([],a,t) = i*t : mult_list_Num([],i,x-1);
}

deff nzp
{
    case (a) = if a > 0 then 1 else if a == 0 then 0 else a;
}

deff fib
{
    case (0) = 1;
    case (1) = 1;
    case (n) = fib(n-1) + fib(n-2);
}

deff maximo
{
    case([],a) = -3 + 5 - 2 ;
    case(x:xs,b) = maximo (x,maximo (xs));
}

deff ordF
{
    case([])=True;
    case(x:xs) = True && False;
    case(x:y:xs) = x <= y && ordF(y:xs);
}


deff concatena
{
    case(x:xs,ys) = mult(ys);
    case(x,ys) = x : concatena([],ys);
}

deff mult
{
    case (a,b) = a*b;
    case (b,g) = [1,2,3];
}

deff mult
{
    case () = 2;
}
"""

x = 4
y = f_idF_(x)
print(y)
l = [1, 2, 3, 4, 5]
sum_l = f_sumf_(l)
print(sum_l)

"""FPY
"""