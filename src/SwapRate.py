# 已知spot rate 求swap rate（par rate）
import numpy as np
import numpy_financial as npf
from sympy import *

s1, s2, s3, s4 = 0.05, 0.06, 0.07, 0.08
sw1= Symbol('sw1')
sw2= Symbol('sw2')
sw3= Symbol('sw3')
sw4= Symbol('sw4')
sw1 / (1 + s1) + 1 / (1 + s1) == 1
xsw1 = solveset(sw1 / (1 + s1) + 1 / (1 + s1) - 1, sw1)
xsw2 = solveset(sw2 / (1 + s1) + sw2 / ((1 + s2) ** 2) + 1 / ((1 + s2) ** 2) - 1, sw2)
xsw3 = solveset(sw3 / (1 + s1) + sw3 / ((1 + s2) ** 2) + sw3 / ((1 + s3) ** 3) + 1 / ((1 + s3) ** 3) - 1, sw3)
xsw4 = solveset(sw4 / (1 + s1) + sw4 / ((1 + s2) ** 2) + sw4 / ((1 + s3) ** 3) + sw4 / ((1 + s4) ** 4) + 1 / ((1 + s4) ** 4) - 1, sw4)

sw1 = list(ConditionSet(sw1, sw1 > 0, xsw1))[0]
sw2 = list(ConditionSet(sw2, sw2 > 0, xsw2))[0]
sw3 = list(ConditionSet(sw3, sw3 > 0, xsw3))[0]
sw4 = list(ConditionSet(sw4, sw4 > 0, xsw4))[0]
print(f'sw1:{sw1}    sw2:{sw2}    sw3:{sw3}    sw4:{sw4}')