import numpy as np
import os
import path
import thinkstats2
from collections import OrderedDict
from scipy import stats
import matplotlib.pylab as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp


def gaus(x, a, x0, sigma):
    return a * exp(-(x - x0) ** 2 / (2 * sigma ** 2))




#generate matrix
gen = {} #store by index 1 -> [BSSID]

listFiles = ["BSSIDS11_54_18.txt","BSSIDS12_13_23.txt","BSSIDS12_18_55.txt","BSSIDS12_28_15.txt","BSSIDS12_35_22.txt","BSSIDS12_42_09.txt","BSSIDS12_46_51.txt","BSSIDS12_53_18.txt","BSSIDS12_57_34.txt","BSSIDS13_03_34.txt","BSSIDS13_08_26.txt","BSSIDS13_16_23.txt","BSSIDS13_20_43.txt","BSSIDS13_25_57.txt","BSSIDS13_31_02.txt","BSSIDS13_35_49.txt"]

numRooms = 16

latest_ssid = "2c:33:11:1a:31:a2\n"

path_files = os.path.join(os.pardir, "measurementSMS") 

counter = 0
for filename in listFiles:
    counter = counter + 1
    temp_dict ={}
    gen[counter] ={}

    BSSID = "0.0.0.0"
    level = -56

    f = open(os.path.join(path_files, filename), "r")
    print(filename)
    print(counter)
    line = f.readline()
    count = 0
    while line:
        if ((count % 2) != 0):
            #odd is RSSI
            level = int(line)
            if (BSSID in temp_dict.keys()):
                temp_dict[BSSID].extend([level])
            else:
                temp_dict[BSSID] = []
                temp_dict[BSSID].extend([level])
        else:
            BSSID = line

        line = f.readline()
        count = count+1

    newd = {}
    newd = sorted(temp_dict.keys())
    cell = {}

    for key, value in temp_dict.items():
        gen[counter][key] = value


#now we have the matrix w BSSID and RSS values, we need to start with BSSID create a dict that can hold pmf

dict_pmf={}

for key, value in gen.items():
    #key is the cell where I am
    index = (numRooms + 1) - key
    #loop through every BSSID
    for k, v in gen[key].items():
        #we get a BSSID
        if k in dict_pmf.keys():
            dict_pmf[k][index]=thinkstats2.Pmf(v)
        else:
            dict_pmf[k] = {}
            dict_pmf[k][index]=thinkstats2.Pmf(v)


#now I have dict_pmf but it should have a fixed format, I am going to consider values from -38 to -94
hey = np.arange(-38, -95, -1) #reference, future will be np.arange(0, 255, 1)
row = np.zeros(len(hey))
reference = np.arange(16, 0, -1)

matrix = {}

for key, value in dict_pmf.items():
    matrix[key] = {}
    for k, v in dict_pmf[key].items():
        matrix[key][k]={}
        for i in range(len(row)):
            matrix[key][k][i] = 0

count = 0
for key, value in dict_pmf.items():
    for j in range(len(reference)):
        if reference[j] in dict_pmf[key].keys():
            for kk, vv in dict_pmf[key][reference[j]].GetDict().items():
                if np.isin(kk, hey):
                    i, = np.where(hey == kk)
                    index = i[0]
                    matrix[key][reference[j]][index] = vv  # percent 0.03

        else:
            matrix[key][reference[j]] = {}
            for i in range(len(row)):
                matrix[key][reference[j]][i] = 0  # stuff non found cells w zeros

#REPEATED but to create Gauss
matGaus = {}

for key, value in dict_pmf.items():
    matGaus[key] = {}
    for k, v in dict_pmf[key].items():
        matGaus[key][k] = {}
        for i in range(len(row)):
            matGaus[key][k][i] = 0


for key, value in matrix.items():
    for k, v in matrix[key].items():
        ii = 0
        arr = np.zeros(len(hey))
        for kk, vv in matrix[key][k].items():
            arr[ii] = vv
            ii = ii + 1
        y = arr
        if (np.sum(y) != 0):
            x = np.arange(0, 57, 1)
            n = len(x)  # the number of data
            mean = sum(x * y) / n  # note this correction
            sigma = sum(y * (x - mean) ** 2) / n  # note this correction

            try:
                popt, pcov = curve_fit(gaus, x, y, p0=[1, mean, sigma])
                hh = gaus(x, *popt)

                for x in range(len(hh)):
                    matGaus[key][k][x] = '{:f}'.format(hh[x])
            except:
                matGaus[key][k] = v

        else:
            matGaus[key][k] = v



rrow = np.zeros(len(hey))
i=0

for kk, vv in matrix[latest_ssid][1].items():
    rrow[i]=vv
    i=i+1
y = rrow
x = np.arange(0, 57, 1)


n = len(x)                          #the number of data
mean = sum(x*y)/n                   #note this correction
sigma = sum(y*(x-mean)**2)/n        #note this correction


popt,pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

# Uncomment to plot the gaussian curves obtained from a cell
# plt.plot(x,y,'b+:',label='data')
# plt.plot(x,gaus(x,*popt),'ro:',label='fit')
# plt.show()

meann, sigmaa = norm.fit(hh)


#lets try to order dict
definitive = {}

for key, value in matrix.items():
    definitive[key] = {}
    definitive[key] = OrderedDict(sorted(matrix[key].items(), key=lambda t: t[0]))


definitiveGaus = {}

for key, value in matGaus.items():
    definitiveGaus[key] = {}
    definitiveGaus[key] = OrderedDict(sorted(matGaus[key].items(), key=lambda t: t[0]))

file1 = open("MyFileRawGaus.txt", "w")
for key, value in definitiveGaus.items():
    file1.write("\n")
    file1.write("key: ")
    file1.write(key)
    for k, v in definitiveGaus[key].items():
        file1.write("\n")
        file1.write( "cell: ")

        file1.write(str(k))
        file1.write("\n")
        for kk, vv in definitiveGaus[key][k].items():
            file1.write(str(vv))
            file1.write(" ,")
    file1.write("\n")

file1.close()

print("File to be added in phone Downloads directory FINALIZED")
