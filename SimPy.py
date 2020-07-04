import simpy
import random

class Station(object):
    def __init__(self, env, num_worker):
        self.env = env
        self.worker = simpy.Resource(env, num_worker)

    def ticket(self, passenger):

        sch_train = random.randint(0,45) #Train arrives after sch_train minutes
        dep_train = sch_train + 10 #Train leaves after dep_train minutes
        print('Next train arriving after',sch_train,'minutes')
        del_ = random.randint(0,10)
        del_f = del_%2
        
        if del_f == 0:
            del_t = random.randint(5,20)
            print('Train is delayed by',del_t,'minutes')
            sch_train = sch_train + del_t
            dep_train = sch_train + 10
            print('Train will arrive after',sch_train,'minutes\n')
        else:
            print('No delay\n')
        num_pass = 0    
        for i in range(passenger):
            time = random.randint(5,60) #time after which passenger's train is scheduled
            if time<=dep_train:
                yield self.env.timeout(random.randint(1,3))
                print('Platform ticket generated')
                num_pass +=1
            else:
                print('Cannot generate platform ticket')

        print('\nPassengers on platorm:', num_pass)
        p = passenger - num_pass
        print('Passengers in waiting lounge:', p,'\n')    

def station_arrival(env, passenger, station):

    arrival_time = env.now

    with station.worker.request() as req:
        yield req
        yield env.process(station.ticket(passenger))

def run_station(env, num_worker):
    station = Station(env, num_worker)
    a = 5
    for passenger in range(20,40):
        env.process(station_arrival(env, passenger, station))

    while a > 0:
        yield env.timeout(0.7)
        passenger += 1
        env.process(station_arrival(env, passenger, station))

def main():
    random.seed(30)
    n = input('Enter no. of workers: ')
    num_worker = int(n)
    env = simpy.Environment()
    env.process(run_station(env, num_worker))
    env.run(until=200)
    
if __name__ == "__main__":
    main()
