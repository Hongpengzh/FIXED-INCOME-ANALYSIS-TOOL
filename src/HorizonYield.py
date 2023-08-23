import numpy_financial as npf

# Change variables here
ParValue = 100
couponrate = 0.05
maturity = 10
n = 10               # The year sell the bond
YTMnew = 0.05      # The new YTM
YTMold = 0.05      # The old YTM

def horizonyeild(ParValue, couponrate, maturity, YTMold, YTMnew=YTMold,  n=maturity):
    coupon = 0
    for i in range(n):
        coupon += ParValue * couponrate * (1 + YTMnew) **i
    Pvold = npf.pv(YTMold, maturity, -ParValue*couponrate, -ParValue)
    Pvatn = npf.pv(YTMnew, (maturity - n), -ParValue*couponrate, -ParValue)
    horizonyeild = ((Pvatn + coupon) / Pvold)**(1/n) -1

    return coupon, Pvold, Pvatn, horizonyeild

if __name__ == '__main__':
    print('Set Variables:')
    print(f'ParValue = {ParValue}, Couponrate = {couponrate}\n'
          f'YTMold = {YTMold}, YTMnew = {YTMnew}, Maturity = {maturity}, \n'
          f'sell at year = {n}\n'
          )
    print('*' * 100)
    coupon, Pvold, Pvatn, horizonyeild = horizonyeild(ParValue, couponrate, maturity, YTMold, YTMnew, n)
    print(f'The pv when we bought the bond is : {Pvold}')
    print(f'The coupon reinvestment when we sell the bond at year {n} is: {coupon}')
    print(f'The pv when we sell the bond at year {n} is : {Pvatn}')
    print(f'The horizonyeild at year {n} is : {horizonyeild}')