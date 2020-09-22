from sgp4.api import Satrec
from matplotlib import pyplot as plt

#parse doppler file and divide into individual curves

doppler_file = open("doppler.txt", "r")

doppler_curves = [[], []]

for line in doppler_file:
    data = line.split()
    if float(data[1])
    
    doppler_curves[0].append(float(data[0]))
    doppler_curves[1].append(float(data[1]))
    
plt.plot(doppler_curves[0], doppler_curves[1])
plt.show()