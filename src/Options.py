import numpy as np
from sympy import *
# Change variables here
par1, par2, par3 = 0.03, 0.04, 0.05
ParValue = 100
var = 0.2
couponrate = 0.05
call = ParValue
put = ParValue
OAS = 0.05

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
def V0_call(s1, s2, s3, var, ParValue=1, couponrate=0, call=ParValue):
    i1L, i1H = rate_i1(s1, s2, var, ParValue, couponrate)
    i2L, i2M, i2H = rate_i2(s1, s2, s3, var, ParValue, couponrate)
    V2L = min(ParValue * (1 + couponrate) / (1 + i2L) + ParValue * couponrate, ParValue*(1 + couponrate))
    V2M = min(ParValue * (1 + couponrate) / (1 + i2M) + ParValue * couponrate, ParValue*(1 + couponrate))
    V2H = min(ParValue * (1 + couponrate) / (1 + i2H) + ParValue * couponrate, ParValue*(1 + couponrate))
    V1L = min(0.5 * (V2L / (1 + i1L) + V2M / (1 + i1L)) + ParValue * couponrate, ParValue*(1 + couponrate))
    V1H = min(0.5 * (V2H / (1 + i1H) + V2M / (1 + i1H)) + ParValue * couponrate, ParValue*(1 + couponrate))
    V0 = 0.5 * (V1L/(1+s1) + V1H/(1+s1))

    return V0
def V0_put(s1, s2, s3, var, ParValue=1, couponrate=0, put=ParValue):
    i1L, i1H = rate_i1(s1, s2, var, ParValue, couponrate)
    i2L, i2M, i2H = rate_i2(s1, s2, s3, var, ParValue, couponrate)
    V2L = max(ParValue * (1 + couponrate) / (1 + i2L) + ParValue * couponrate, ParValue*(1 + couponrate))
    V2M = max(ParValue * (1 + couponrate) / (1 + i2M) + ParValue * couponrate, ParValue*(1 + couponrate))
    V2H = max(ParValue * (1 + couponrate) / (1 + i2H) + ParValue * couponrate, ParValue*(1 + couponrate))
    V1L = max(0.5 * (V2L / (1 + i1L) + V2M / (1 + i1L)) + ParValue * couponrate, ParValue*(1 + couponrate))
    V1H = max(0.5 * (V2H / (1 + i1H) + V2M / (1 + i1H)) + ParValue * couponrate, ParValue*(1 + couponrate))
    V0 = 0.5 * (V1L/(1+s1) + V1H/(1+s1))

    return V0
def tryOAS_call(OAS, s1, s2, s3, var, ParValue, couponrate, call=ParValue):
    i1L, i1H = rate_i1(s1, s2, var, ParValue, couponrate)
    i2L, i2M, i2H = rate_i2(s1, s2, s3, var, ParValue, couponrate)
    V2H = min((ParValue*(1+couponrate) / (1+i2H+OAS) + ParValue*couponrate),(call + ParValue*couponrate))
    V2M = min((ParValue*(1+couponrate) / (1+i2M+OAS) + ParValue*couponrate),(call + ParValue*couponrate))
    V2L = min((ParValue*(1+couponrate) / (1+i2L+OAS) + ParValue*couponrate),(call + ParValue*couponrate))
    V1H = min((0.5 * (V2H / (1 + i1H+OAS) + V2M / (1 + i1H+OAS)) + ParValue * couponrate),(call + ParValue*couponrate))
    V1L = min((0.5 * (V2L / (1 + i1L+OAS) + V2M / (1 + i1L+OAS)) + ParValue * couponrate),(call + ParValue*couponrate))
    V0 = 0.5 * (V1L/(1+s1+OAS) + V1H/(1+s1+OAS))

    return V0
def tryOAS_put(OAS, s1, s2, s3, var, ParValue, couponrate, put=ParValue):
    i1L, i1H = rate_i1(s1, s2, var, ParValue, couponrate)
    i2L, i2M, i2H = rate_i2(s1, s2, s3, var, ParValue, couponrate)
    V2H = max((ParValue*(1+couponrate) / (1+i2H+OAS) + ParValue*couponrate),(put + ParValue*couponrate))
    V2M = max((ParValue*(1+couponrate) / (1+i2M+OAS) + ParValue*couponrate),(put + ParValue*couponrate))
    V2L = max((ParValue*(1+couponrate) / (1+i2L+OAS) + ParValue*couponrate),(put + ParValue*couponrate))
    V1H = max((0.5 * (V2H / (1 + i1H+OAS) + V2M / (1 + i1H+OAS)) + ParValue * couponrate),(put + ParValue*couponrate))
    V1L = max((0.5 * (V2L / (1 + i1L+OAS) + V2M / (1 + i1L+OAS)) + ParValue * couponrate),(put + ParValue*couponrate))
    V0 = 0.5 * (V1L/(1+s1+OAS) + V1H/(1+s1+OAS))

    return V0

if __name__=='__main__':
    s1, s2, s3 = spotrates(par1, par2, par3)
    callV0 = V0_call(s1, s2, s3, var, ParValue, couponrate, call)
    putV0 = V0_put(s1, s2, s3, var, ParValue, couponrate, put)
    OAScallV0 = tryOAS_call(OAS, s1, s2, s3, var, ParValue, couponrate, call)
    OASputV0 = tryOAS_put(OAS, s1, s2, s3, var, ParValue, couponrate, put)
    print('Set Variables:')
    print(f'If Par rate 1 = {par1},    Par rate 2 = {par2},    Par rate 3 = {par3},\n'
          f'Par value = {ParValue},     Coupon rate = {couponrate},    Volatility = {var}\n'
          f'Call price = {call},    Put price = {put}\n')
    print('*' * 100)
    print(f'if the bond is callable at par:        V0= {callV0} ')
    print(f'if the bond is putable at par:         V0= {putV0} ')
    print('*' * 100)
    print(f'if the bond is callable at par and OAS={OAS}:      V0= {OAScallV0} ')
    print(f'if the bond is putable at par and OAS={OAS}:       V0= {OASputV0} ')