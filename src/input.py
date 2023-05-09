"""FPY
deff sum
{
    case ([]) = 0;
    case (x:xs) = x + sum(xs); 
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
    case (x:xs,2,5) = if ! (x % 2 == 0) then filtra_impares(xs) else x ++ filtra_impares(xs);
    case (x:xs,3,5) = if ! (x % 2 == 0) then filtra_impares(xs) else x ++ filtra_impares(xs);
    case (x:xs,3,7) = if ! (x % 2 == 0) then filtra_impares(xs) else x ++ filtra_impares(xs);
}


deff soma_impares_2{
    case(x) = sum . filtra_impares(x);
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


deff id
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
    case(x:xs,b) = max (x,maximo (xs));
}

deff ord
{
    case([])=True;
    case(x:xs) = True && False;
    case(x:y:xs) = x <= y && ord(y:xs);
}


deff concatena
{
    case(x:xs,ys) = ys;
    case(x,ys) = x : concatena([],ys);
}
"""


x = 4
y = f_id_(x)
5
print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)
