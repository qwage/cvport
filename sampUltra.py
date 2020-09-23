import random as r
import time as t


start = t.perf_counter() 
print(start)
mark = .2
distance = []

try:
    while True:
        if (t.perf_counter()  - start) > mark: 
            dist = r.randrange(1,100) # Distance in Centimeters
            print("The distance is", dist, "cm")
            distance.append(dist)
            mark += .2
        else:
            None
except KeyboardInterrupt:
    pass

print(distance)