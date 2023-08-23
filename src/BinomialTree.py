import numpy as np
from sympy import *

# Change variables here
par1, par2, par3 = 0.03, 0.04, 0.05
ParValue = 100
var = 0.2
couponrate = 0.05

def spotrates(par1, par2, par3): # The function takes par rates return spot rates
    s1 = par1
    s2 = Symbol('s2', real=True) # only return real roots
    xs2 = solveset(1*par2/(1+s1) + 1*(1+par2)/(1+s2)**2 - 1, s2)
    # for item in xs2:
    #     if item[0] > 0:
    #         s2 = item[0]
    s2 = list(ConditionSet(s2, s2>0, xs2))[0]
    s3 = Symbol('s3', real=True)
    xs3 = solve([1*par3/(1+s1) + 1*par3/(1+s2)**2 + 1*(1+par3)/(1+s3)**3 - 1], [s3])
    for item in xs3:
        if item[0] > 0:
            s3 = item[0]
    # s3 = list(ConditionSet(s3, (s3>0) & (s3 in S.Reals), xs3))[0]
    return s1, s2, s3
def forwardrates(s1, s2, s3):
    f1 = s1
    f2 = Symbol('f2', real=True)
    xf2 = solveset((1+s2)**2 - (1+s1)*(1+f2), f2)
    # f2 = list(xf2.values())[0]
    f2 = list(ConditionSet(f2, f2>0, xf2))[0]
    f3 = Symbol('f3', real=True)
    xf3 = solveset((1+s3)**3 - (1+s2)**2*(1+f3), f3)
    # f3 = list(xf3.values())[0]
    f3 = list(ConditionSet(f3, f3>0, xf3))[0]
    return f1, f2, f3
def rate_i1(s1, s2, var, ParValue=1, couponrate=0): # return i1L, i1H
    pv2 = ParValue*couponrate/(1+s1) + ParValue*(1+couponrate)/(1+s2)**2
    i1L = Symbol('i1L', real=True)
    xi1L = solveset((0.5*(ParValue*(1+couponrate)/(1+i1L) + ParValue*(1+couponrate)/(1+i1L*np.e**(2*var)))
                  + ParValue*couponrate) / (1+s1) - pv2, i1L)
    i1L = list(ConditionSet(i1L, i1L > 0, xi1L))[0]
    i1H = i1L*np.e**(2*var)

    return i1L, i1H
def rate_i2(s1, s2, s3, var, ParValue=1, couponrate=0): # return i2L, i2M, i2H
    pv3 = ParValue*couponrate/(1+s1) + ParValue*couponrate/(1+s2)**2 + ParValue*(1+couponrate)/(1+s3)**3
    i1L, i1H = rate_i1(s1, s2, var, ParValue, couponrate)
    i2M = Symbol('i2M')
    V1H = 0.5*(ParValue*(1+couponrate)/(1+i2M) + ParValue*(1+couponrate)/(1+i2M*np.e**(2*var))) + ParValue*couponrate
    V1L = 0.5*(ParValue*(1+couponrate)/(1+i2M) + ParValue*(1+couponrate)/(1+i2M*np.e**(-2*var))) + ParValue*couponrate
    xi2M = solveset((0.5*(V1H/(1+i1H) + V1L/(1+i1L)) + ParValue*couponrate) / (1+s1) - pv3, i2M)
    i2M = list(ConditionSet(i2M, i2M>0, xi2M))[0]
    i2H = i2M*np.e**(2*var)
    i2L = i2M*np.e**(-2*var)

    return i2L, i2M, i2H

if __name__=='__main__':
    s1, s2, s3 = spotrates(par1, par2, par3)
    f1, f2, f3 = forwardrates(s1, s2, s3)
    pv1 = ParValue*couponrate/(1+s1)
    pv2 = ParValue * couponrate / (1 + s1) + ParValue * (1 + couponrate) / (1 + s2) ** 2
    pv3 = ParValue * couponrate / (1 + s1) + ParValue * couponrate / (1 + s2) ** 2 \
          + ParValue * (1 + couponrate) / (1 + s3) ** 3
    i1L, i1H = rate_i1(s1, s2, var, ParValue=1, couponrate=0)
    i2L, i2M, i2H = rate_i2(s1, s2, s3, var, ParValue=1, couponrate=0)
    V2L = ParValue * (1 + couponrate) / (1 + i2L) + ParValue * couponrate
    V2M = ParValue * (1 + couponrate) / (1 + i2M) + ParValue * couponrate
    V2H = ParValue * (1 + couponrate) / (1 + i2H) + ParValue * couponrate
    V1L = 0.5 * (V2L / (1 + i1L) + V2M / (1 + i1L)) + ParValue * couponrate
    V1H = 0.5 * (V2H / (1 + i1H) + V2M / (1 + i1H)) + ParValue * couponrate
    V0 = 0.5 * (V1L/(1+s1) + V1H/(1+s1))
    print('Set Variables:')
    print(f'Par rate 1 = {par1},    Par rate 2 = {par2},    Par rate 3 = {par3},\n'
          f'Par value = {ParValue},    Coupon rate = {couponrate},    Volatility = {var}\n'
          )
    print('*' * 100)
    print(f's1 = {s1:<}         s2 = {s2:>4}            s3={s3:>4}')
    print(f'f1 = {f1:<}         f2 = {f2:>4}            f3={f3:>4}')
    print(f'pv1 = {pv1:<}         pv2 = {pv2:>4}            pv3={pv3:>4}')
    print('*'*100)
    print(f'i1L = {i1L:<}         i1H = {i1H:>4}')
    print(f'i2L = {i2L:<}         i2M = {i2M:>4}            i2H={i2H:>4}')
    print('*' * 100)
    print(f'V2L = {V2L:<}         V2M = {V2M:>4}            V2H={V2H:>4}')
    print(f'V1L = {V1L:<}         V1H = {V1H:>4}')
    print(f'V0 = {V0:<} is very close to pv3 = {pv3:>4}')
