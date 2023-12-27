#These will be set again during the init of the simulator
timeSlice = 0

class Queue:
    def __init__(self):
        self.queue = []

    def __iter__(self):
        return self.queue.__iter__()
    def __str__(self):
        s = ""
        for process in self.queue:
            s += str(process.getPID()) + " "
        return s

    def addPCB(self,pcb):
        self.queue.append(pcb)
    
    def removePCB(self):
        item = self.queue.pop()
        return item

    def decrement(self):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        for process in self.queue:
            process.decrementIoBurst()
    
    def increment(self,what):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        # for each process in queue
        #    call incrementwaittime
        if what == "waittime":
            for process in self.queue:
                process.incrementWaitTime()
        elif what == "readytime":
            for process in self.queue:
                process.incrementReadyTime()

class SysClock:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state
        if not 'clock' in self.__dict__: 
            self.clock = 0
    def __str__(self):
        return str(self.clock)
    def __int__(self):
        return self.clock
    def increment(self):
        self.clock += 1
    

class CPU:
    def __init__(self):
        self.busy = False
        self.runningPCB = None
        self.queue = []
        self.timer = 0
        self.inactiveTime = 0
    def __str__(self):
        if self.runningPCB is None:
            return ""
        else:
            s = str(self.runningPCB.getPID())
            return s

    def __cmp__(self):
        return int(self.getPCB().priority[1:])
    def __lt__(self,other):
        return int(self.getPCB().priority[1:]) < int(other.getPCB().priority[1:])
    def __gt__(self,other):
        return int(self.getPCB().priority[1:]) > int(other.getPCB().priority[1:])


    def getPCB(self):
        return self.runningPCB
    
    def decrementCurrentProcess(self):
        self.getPCB().decrementCpuBurst()
        self.timer += 1
    def incrementIdleTime(self):
        self.inactiveTime += 1
    def getIdleTime(self):
        return self.inactiveTime
        #no idea why this did not work.
#        self.runningPCB.incrementCpuTime()
    def loadProcess(self,pcb):
        self.runningPCB = pcb
        self.timer = 0
 #       if len(pcb.bursts) % 2 == 0:
 #           print(f"even, CPU. Bad -------------------------------------------------------------{pcb}")

    def testKickOff(self):
        global timeSlice
        #regardless of timeslicing this condition is priority
        if self.runningPCB.getCurrentBurstTime() == 0:
            self.runningPCB.popBurst()
            if self.runningPCB.getBurstLength() == 0:
                temp = self.runningPCB
                self.runningPCB = None
                return (temp,5)
            else:
                temp = self.runningPCB
                self.runningPCB = None
                return (temp,3)
        #now that we know curent burst time is not 0, check time slice.
        elif int(timeSlice) > 0 and self.timer == int(timeSlice):
            if self.runningPCB.getBurstLength() == 0:
                temp = self.runningPCB
                self.runningPCB = None
                return (temp,5)
            else:
                temp = self.runningPCB
                self.runningPCB = None
                return (temp,3)
        else:
            pass


class IO:
    def __init__(self):
        self.busy = False
        self.runningPCB = None
        self.queue = []
        self.timer = 0
        self.inactiveTime = 0
    def __str__(self):
        if self.runningPCB is None:
            return ""
        else:
            s = str(self.runningPCB.getPID())
            return s

    def __cmp__(self):
        return int(self.getPCB().priority[1:])
    def __lt__(self,other):
        return int(self.getPCB().priority[1:]) < int(other.getPCB().priority[1:])
    def __gt__(self,other):
        return int(self.getPCB().priority[1:]) > int(other.getPCB().priority[1:])

    def getPCB(self):
        return self.runningPCB

    def decrementCurrentProcess(self):
        self.getPCB().decrementIoBurst()
        self.timer += 1
    def incrementIdleTime(self):
        self.inactiveTime += 1
    def getIdleTime(self):
        return self.inactiveTime
    def loadProcess(self,pcb):
        self.runningPCB = pcb
        self.timer = 0
#        if len(pcb.bursts) % 2 == 1:
#            print(f"odd, CPU. Bad -------------------------------------------------------------{pcb}")

    def testKickOff(self):
        if self.runningPCB.getCurrentBurstTime() == 0:
            self.runningPCB.popBurst()
            #this if should never run in our current situation since the last burst is always cpu.
            if self.runningPCB.getBurstLength() == 0:
                temp = self.runningPCB
                self.runningPCB = None
                return (temp,5)
            else:
                temp = self.runningPCB
                self.runningPCB = None
                return (temp,1)
                #now that we know curent burst time is not 0, check time slice.
        # elif timeSlice > 0 and self.timer == timeSlice:
        #     if self.runningPCB.getBurstLength() == 0:
        #         temp = self.runningPCB
        #         self.runningPCB = None
        #         return (temp,5)
        #     else:
        #         temp = self.runningPCB
        #         self.runningPCB = None
        #         return (temp,1)
        # else:
        #     pass

class PCB:
    def __init__(self,pid,bursts,at,priority):
        self.pid = pid     
        self.priority = priority     # 0
        self.arrivalTime = at
        self.bursts = bursts    # 5 3  2 2  2 3  3 3 3 2 3 3 4 2 5 2 5 3 3 3 4
        self.currBurst = 'IO'
        self.currBurstIndex = 0
        self.cpuBurst = 5
        self.readyQueueTime = 0
        self.waitQueueTime = 0
        self.cpuTime = 0
        self.ioTime = 0

    def __str__(self):
        return (f"{self.pid} {self.priority} {self.arrivalTime} {self.bursts}")
    def __cmp__(self):
        return int(self.priority[1:])
    def __lt__(self,other):
        return int(self.priority[1:]) < int(other.priority[1:])
    def __gt__(self,other):
        return int(self.priority[1:]) > int(other.priority[1:])
    def __eq__(self,other):
        if isinstance(other, PCB):
            return str(self.pid) == str(other.pid)
        return False
    
    def decrementCpuBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def decrementIoBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def incrementBurstIndex(self):
        self.currBurstIndex += 1
    
    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]
    
    #rather than move the burst index, I prefer to pop the values out of my burst list.
    #this way I can just check the length of the list to see if I am done.
    def popBurst(self):
        self.bursts.pop(self.currBurstIndex)


    #basic increment methods for data collection
    def incrementWaitTime(self):
        self.waitQueueTime += 1
    def incrementReadyTime(self):
        self.readyQueueTime += 1
    def incrementCpuTime(self):
        self.cpuTime += 1
    def incrementIOTime(self):
        self.ioTime += 1
    #basic getters for data collection
    def getWaitTime(self):
        return self.waitQueueTime
    def getReadyTime(self):
        return self.readyQueueTime
    def getCpuTime(self):
        return self.cpuTime
    def getIOTime(self):
        return self.ioTime
    #this is how I will tell if a process is going to io or cpu
    #every even index is io, every odd is cpu.
    #so if we have an even length, we go to io.
    #if we have an odd length we go to CPU.
    #if length is 0, then we are done.
    # cpu, io, cpu ,io, cpu , io, cpu.
    def getBurstLength(self):
        return len(self.bursts)
    def getArrivalTime(self):
        return self.arrivalTime
    def getPID(self):
        return self.pid
    def getTurnaroundTime(self):
        turntime = int(self.waitQueueTime) + int(self.readyQueueTime) + int(self.cpuTime) + int(self.ioTime)
        turntime = turntime - int(self.arrivalTime)
        return turntime

class Simulator:
    global timeSlice
    def __init__(self,datfile, TimeSlice, NumCPU, NumIO, Type):
        global timeSlice
        self.datfile = datfile
        self.new = Queue()
        self.wait = Queue()
        self.running = CPU()
        self.io = IO()
        self.ready = Queue()
        self.terminated = Queue()
        self.List = self.readData()
        timeSlice = int(TimeSlice)
        #max cpu/io and used cpu/io
        #this will be used to help determine if a cpu is available to take a process.
        #when we process ready and waiting queues
        self.numCPU = NumCPU
        self.UsedCPU = 0
        self.numIO = NumIO
        self.UsedIO = 0
        
        self.type = Type
        self.CPU_List = []
        self.IO_List = []
        for i in range(self.numCPU):
            self.CPU_List.append(CPU())    
        for i in range(self.numIO):
            self.IO_List.append(IO())
    def __str__(self):
        s = ""
        itercpu = 0
        iterio = 0
        if self.datfile is not None:
            s += "datfile: "+self.datfile +"\n"
        if self.new is not None:
            s += "new queue: "+",".join(str(self.new).split())  +"\n"
        if self.ready is not None:
            s += "ready queue: "+",".join(str(self.ready).split())  +"\n"
        for CPU in self.CPU_List:
            s += f"cpu {itercpu}: "+str(CPU)+"\n"
            itercpu += 1
        if self.wait is not None:
            s += "wait queue: "+",".join(str(self.wait).split())  +"\n"
        for IO in self.IO_List:
            s += f"io {iterio}: "+str(IO)+"\n"
            iterio += 1
        if self.terminated is not None:
            s += "exit queue: "+",".join(str(self.terminated).split())  +"\n"            
        return s


    def readData(self):
        List_Processes = []
        with open(self.datfile) as f:
            self.data = f.read().split("\n")

        for process in self.data:
            if len(process) > 0:
                parts = process.split(' ')
                arrival = parts[0]
                pid = parts[1]
                priority = parts[2]
                bursts = parts[3:]
                bursts = [int(i) for i in bursts]

                List_Processes.append(PCB(pid,bursts,arrival,priority))
#                print(f"{arrival}, {pid}, {priority} {len(bursts)}{bursts}")
        return List_Processes
    def getList(self):
        return self.List
    
    #getters and setters to deal with cpus and io availability
    #upgraded to a flag and increment/decrement functions.
    def AvailableCPU_Flag(self):
        for cpu in self.CPU_List:
            if cpu.getPCB() is None:
                return True
        return False
    def AvailableIO_Flag(self):
        for IO in self.IO_List:
            if IO.getPCB() is None:
                return True
        return False

    def getnumCPU(self):
        return self.numCPU
    def getnumIO(self):
        return self.numIO
    def getUsedCPU(self):
        temp = 0
        for cpu in self.CPU_List:
            if cpu.getPCB() is not None:
                temp += 1
        return temp
    def getUsedIO(self):
        temp = 0
        for IO in self.IO_List:
            if IO.getPCB() is not None:
                temp += 1
        return temp
    def setUsedCPU(self,used):
        self.UsedCPU = used
    def setUsedIO(self,used):
        self.UsedIO = used
    def incrementUsedCPU(self):
        self.UsedCPU += 1
    def incrementUsedIO(self):
        self.UsedIO += 1
    def decrementUsedCPU(self):
        self.UsedCPU -= 1
    def decrementUsedIO(self):
        self.UsedIO -= 1
    def isDone(self):
        if len(self.List) == len(self.terminated.queue) and self.new.queue == [] and self.ready.queue == [] and self.wait.queue == []:
            return True
        else:
            return False
if __name__=='__main__':
    sim = Simulator("datafile.dat")
    print(sim)
    for process in sim.data:
        print(process)

    