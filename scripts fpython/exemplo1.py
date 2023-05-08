"""FPY
deff sum
{
    case ([]) = 0;
    case (x:xs) = x + sum(xs); 
}

deff soma_impares
{
    case ([]) = 0;
    case (x:xs) = if x>2 then soma_impares(xs) else x + soma_impares(xs);
}

deff filtra_impares
{
    case ([],2,2) = [];
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
}

deff id
{
    case (a) = a;
}

deff func_const
{
    case() = 3;
}

deff mult_list_Num
{
    case ([],i) = [];
    case (x:xs,i) = i*x : mult_list_Num(xs,i);
}

deff nzp
{
    case (a) = if a > 0 then 1 else if a == 0 then 0 else a;
}

deff fib
{
    case (0) = 0;
    case (a) = 1;
    case (True) = i*x : mult_list_Num(i);
    case (8) = fib(n-1) + fib(n-2);
}

deff maximo
{
    case([],a) = x;
    case(x:xs,b) = max (x,maximo (xs));
}

deff ord
{
    case([])=True;
    case(x:xs)=True;
    case(x:y:xs) = x <= y && ord(y:xs);
}


deff concatena
{
    case([],ys) = ys;
    case(x:xs,ys) = x : concatena(xs,ys);
}
"""

x = 4
y = f_mais_um_(x)
5
print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)
