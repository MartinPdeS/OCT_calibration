import numpy as np
import matplotlib.pyplot as plt

data = np.load('array1.npy')[0]


print(np.shape(data))





#plt.plot(slice[70,:])
plt.imshow(data[:,:,100],cmap = "gray")
plt.show()
