#Define accel
def accel(velocity):
    import time
    print(time.time())
    for k in range(1,10000000):
               
        rl_ahead(k*velocity / 10000000)
        rr_ahead(k*velocity / 10000000)
        fl_ahead(k*velocity / 10000000)
        fr_ahead(k*velocity / 10000000)
    print(time.time())

def rl_ahead(velocity):
    #print('rl moving at: ',velocity)
    b = 1
def rr_ahead(velocity):
    #print('rr moving at: ',velocity)
    b = 1
def fl_ahead(velocity):
    #print('fl moving at: ',velocity)
    b = 1
def fr_ahead(velocity):
    #print('fr moving at: ',velocity)
    b = 1

#Define Main
def main():
    accel(10)
main()
