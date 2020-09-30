import numpy as np

def random2Ddepth(width,scaling_factor):
    "Gives random depth list from 0 to 100, divided by scaling factor"

    import random as r

    depth = []
    for i in range(width):
        dist = r.randrange(1,100) / scaling_factor
        depth.append(int(dist))
        
    return depth

def random_coords(size_range):
    "Gives random coordiantes (xbottomleft, ybottomleft, xtopright, ytopright) for the object box within frame size >~10"

    import random as r

    xtopright = r.randrange(1,size_range - 10) + 10
    xbottomleft = r.randrange(1,xtopright - 8)
    ybottomleft = r.randrange(1,size_range - 10) + 10
    ytopright = r.randrange(1,ybottomleft - 8)

    coords = [xbottomleft, ybottomleft, xtopright, ytopright]
    return coords

depth = random2Ddepth(15,1)
print(str(depth))
coords = random_coords(100)
print(str(coords))

