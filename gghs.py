import numpy as np

abc=np.zeros(shape=(1,5))
print(abc)
rabc=np.repeat(abc,10, axis=0)
print(rabc[0])