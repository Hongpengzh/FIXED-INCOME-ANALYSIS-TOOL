import numpy as np
import numpy_financial as npf
import pandas as pd

# Change variables here
ParValue = 100
couponrate = 0.04
maturity = 5
POD1 = 0.02
recoverrate = 0.4
YTM = 0.015

def PODn(n):
    if n == 1:
        return POD1
    else:
        return (1-POD1)**(n-1) * POD1

def POSn(n):
    return (1-POD1)**(n-1)

def Exposuren(n):
    coupon = 0
    for i in range(maturity - n + 1):
        coupon += ParValue * couponrate / (1 + YTM) **i

    return coupon + ParValue / (1 + YTM)**(maturity - n)

def Recoveryn(n):
    return Exposuren(n) * recoverrate

def LGDn(n):
    return Exposuren(n) - Recoveryn(n)

def ExpLoss(n):
    return PODn(n) * LGDn(n)

def DF(n):
    return 1/(1 + YTM)**n

def PVofExpLoss(n):
    return ExpLoss(n) * DF(n)

if __name__ == '__main__':
    df = pd.DataFrame(np.zeros((maturity, 8)), index=np.arange(1,maturity+1),
                      columns=['Exposure','Recovery','LGD','POD','POS','Expected Loss','DF','PV of Expected Loss'])
    for index in df.index:
        df.loc[index,:] = np.array([Exposuren(index), Recoveryn(index), LGDn(index), PODn(index),
                            POSn(index), ExpLoss(index), DF(index), PVofExpLoss(index)])
    CVA = df['PV of Expected Loss'].sum()
    pv = npf.pv(YTM, maturity, -ParValue*couponrate, -ParValue)
    pvafrisk = pv - CVA
    cashflow = np.hstack((-pvafrisk, np.full(maturity - 1, ParValue*couponrate), ParValue*(1 + couponrate)))
    YTMafrist = npf.irr(cashflow)
    creditspread = YTMafrist - YTM

    print('Set Variables:')
    print(f'ParValue = {ParValue}, Couponrate = {couponrate}\n'
          f'YTM = {YTM}, Maturity = {maturity}, \n'
          f'POD = {POD1}, Recovery rate = {recoverrate}\n'
          )
    print('*' * 100)
    print(f'The CVA is: {CVA}')
    print(f'The PV after risk is: {pvafrisk}')
    print(f'The credit spread is: {creditspread}')



