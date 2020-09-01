import numpy as np
from matplotlib import pyplot as plt

true_x_list = [0]
x_list = [0]
y_list = [0]

true_x = 0
x = 0
p = 0

for i in range(20):
   #predict next state
   true_x = true_x + 1 + np.random.normal()
   true_x_list.append(true_x)
   x = x + 1
   p = p + 1
   
   #calculate kalman gain
   K = p / (p + 1)
   print(K)
   
   #measure data
   y = true_x + np.random.normal()
   y_list.append(y)
   
   #update with measurement
   p = (1 - K) * p
   x = x + K*(y-x)
   x_list.append(x)
   
plt.plot(true_x_list, ".", label="True x")
plt.plot(x_list, label="x")
plt.plot(y_list, label="y")
plt.legend()
plt.show()