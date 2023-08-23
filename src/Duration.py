import numpy_financial as npf

# Change variables here, default values
Parvalue = 100
couponrate = 0.08
YTM = 0.104     # attention: for each term
maturity = 10  # attention: for each term
t = 0
T = 360

# Input variables
def input_test(variable, string):
    while True:
        user_input = input(f'Please input {string}:')
        try:
            variable = float(user_input)
        except ValueError:
            print(f'{string} must be a number, please input again!')
        else:
            print(f'{string} is {variable}')
            break
    return variable

def MacaulayDuration(Parvalue, couponrate, YTM, maturity, t=0, T=360):
    macaulay = 0
    pv = npf.pv(YTM, maturity, -Parvalue*couponrate, -Parvalue)
    for n in range(1, int(maturity)):
        macaulay += Parvalue * couponrate / (1 + YTM)**n / pv * (n - t / T)
    macaulay += Parvalue * (1 + couponrate) / (1 + YTM)**maturity / pv * (maturity - t / T)

    return macaulay
def ModDuration(macaulay, YTM, ann=1):
    return macaulay / ann / (1 + YTM)

if __name__ == '__main__':
    Parvalue = input_test(Parvalue, 'Parvalue')
    couponrate = input_test(couponrate, 'couponrate')
    YTM = input_test(YTM, 'YTM')
    maturity = input_test(maturity, 'maturity')
    t = input_test(t, 't')
    T = input_test(T, 'T')
    macaulay = MacaulayDuration(Parvalue, couponrate, YTM, maturity, t, T)
    mod = ModDuration(macaulay, YTM, ann=2)
    print('Set Variables:')
    print(f'ParValue = {Parvalue}, Couponrate = {couponrate}\n'
          f'YTM = {YTM}, Maturity = {maturity}\n'
          f't = {t}, T = {T}\n'
          )
    print('*' * 100)
    print(f'MacaulayDuration = {macaulay},    ModDuration = {mod}')