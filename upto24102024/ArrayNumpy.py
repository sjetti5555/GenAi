import numpy as np

data1 = np.array([10,20,30,40,50]) #creating an array   

data2 = np.array([60,70,80,90,100]) #creating another array

print(f"first element of data1:{data1[1]}")  #accessing the first element of data1

print(f"slice:{data2[1:4]}")    #slicing of array from 1 to 4

np.save("data1.npy",data1)
