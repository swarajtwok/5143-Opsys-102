from rich import print
from rich.table import Table
from rich.live import Live
from rich.columns import Columns
import random
import time
from rich.progress import SpinnerColumn
from rich.console import Console
from rich.panel import Panel

from basic_sim import *
from basic_sim import timeSlice
import argparse
import sys
import os

# Gets the width of the console so I can size each column as a percentage so
# the width stays static looking and the "processes" can grow and shrink.
console = Console()
terminal_width = console.width


#pulling in optional arguments, with default values, from the command line
parser = argparse.ArgumentParser(description='Simulate a CPU scheduling algorithm')
parser.add_argument("--Time_Slice", type=int, default=0, help="Optional time slice variable, default is 0 which is first in first out with no preemption.")
parser.add_argument("--CPU", type=int, default=5, help="An optional CPU variable, default is 1. More CPUs more processes that can run at the same time.")
parser.add_argument("--IO", type=int, default=2, help="An optional IO variable, default is 1. More IOs more processes that can run at the same time.")
parser.add_argument("--filename", type=str, default="cpu_small.dat", help="An optional filename variable, default is datafile.dat.")
parser.add_argument("--type", type=str, default="PR", help="An optional type of scheduling variable, default is First Come First Serve('FCFS'). Priority('PR') is the other choice.")
parser.add_argument("--timer", type=float, default=0.0001, help="An optional time variable that determines how fast the table updates.")
parser.add_argument("--skip", type=int, default=1, help="Skip and print every nth iteration")
args = parser.parse_args()

#
def make_row(queue):
    queue_name = ""
    s = ""
    if queue == 0:
        queue_name = "New"
        s+= temp_new
    elif queue == 1:
        queue_name = "Ready"
        s+= temp_ready
    elif queue == 2:
        queue_name = "Running"
        s+= temp_run
    elif queue == 3:
        queue_name = "Waiting"
        s+= temp_wait
    elif queue == 4:
        queue_name = "I/O"
        s+= temp_io
    elif queue == 5:
        queue_name = "Exit"
        s+= temp_exit
    return [queue_name, s]

def generate_table() -> Table:
    """ 
        - This function returns a `rich` table that displays all the queue contents. How you format that is up to you.
        - The `end_section=True` is what puts a line between rows
        - I left a commented line to show how you can change background colors, but is not the whole table or column or row. You'll see.
        - All I do is call `make_row` with the queue name and my random ranges. The "*" is how you add a "list" as a row, it explodes it basically,
           and since `make_row` returns a list with one entry per column, we need to expand it. 
        - You will probably have to pass in your queues or put this in a class to generate your own table .... or don't. 
    """
    # Create the table
    table = Table(show_header=False)
    #table.add_column("Queue", style="bold yellow on blue dim", width=int(terminal_width*.1))
    table.add_column("Queue", style="bold red", width=int(terminal_width*.1))
    table.add_column("Processes", width=int(terminal_width*.8))
    table.add_row(*make_row(0), end_section=True)
    table.add_row(*make_row(1), end_section=True)
    table.add_row(*make_row(2), end_section=True)
    table.add_row(*make_row(3), end_section=True)
    table.add_row(*make_row(4), end_section=True)
    table.add_row(*make_row(5), end_section=True)
    return table

#sending the optional arguments to our simulator.
sim = Simulator(args.filename, args.Time_Slice, args.CPU, args.IO, args.type)
timeSlice = args.Time_Slice

#running the simulator
clock = SysClock()
#   this is for our inputs from file. We will check this every clock cycle to grab new processes
data = sim.getList()

# we want a list of tuples of (pcb, destination) for each pass, at the end of each pass we will put these in their destinations.
# destinations will be (0,1,2,3,4,5) for new, ready, running, waiting, io, and terminated respectively.
Move_List = []
#log of all the enter and exit messages into cpu and io for a given cycle.
Message_Log = []
conditional = True

iteration_count = 0
skipp = args.skip

while(conditional):
 
    #   Now to process each queue. We will do this in order of priority.
    #   running, io, new, ready, wait. Terminate doesn't require any processing.
    #   we check running and io first as they have a size limit and processing them first can free up space for new processes.
    
    os.system('cls' if os.name == 'nt' else 'clear')

    #   running
    for CPU in sim.CPU_List:
        if CPU.getPCB() is not None:
            CPU.decrementCurrentProcess()
            CPU.getPCB().incrementCpuTime()
            Temp = CPU.testKickOff()
            if Temp is not None:
                Move_List.append(Temp)
                Message_Log.append(f"J{Temp[0].getPID()} has stopped running.")
                sim.decrementUsedCPU()
        else:
            CPU.incrementIdleTime()
    #   io
    for IO in sim.IO_List:
        if IO.getPCB() is not None:
            IO.decrementCurrentProcess()
            IO.getPCB().incrementIOTime()
            Temp = IO.testKickOff()
            if Temp is not None:
                Move_List.append(Temp)
                Message_Log.append(f"J{Temp[0].getPID()} has left IO.")
                sim.decrementUsedIO()
        else:
            IO.incrementIdleTime()

    #   new
    for process in sim.new:
        Move_List.append((process,1))
    sim.new = Queue()
    #   ready
    i = 0
    sim.ready.increment("readytime")
    while i < len(sim.ready.queue):
        process = sim.ready.queue[i]
        if args.type != "PR":
            #we need to check if a CPU is empty and if one is then we need to move the process to it.
            if sim.AvailableCPU_Flag() == True:
                for CPU in sim.CPU_List:
                    if CPU.getPCB() is None:
                        CPU.loadProcess(process)
                        Message_Log.append(f"J{process.getPID()} is running.")
                        break
                sim.ready.queue.remove(process)
            else:
                i += 1
            #we need to check the lowester priority cpu.
        else:
            #Priority Queue promotion method.
            if process.priority[1:] != "1" and process.getReadyTime() == 200:
                process.priority = "p" + str(int(process.priority[1:]) - 1)
                Message_Log.append(f"J{process.getPID()} has been promoted to priority {process.priority[1:]}")
            elif process.priority[1:] != "1" and process.getReadyTime() == 400:
                process.priority = "p" + str(int(process.priority[1:]) - 1)
                Message_Log.append(f"J{process.getPID()} has been promoted to priority {process.priority[1:]}")
            elif process.priority[1:] != "1" and process.getReadyTime() == 800:
                process.priority = "p" + str(int(process.priority[1:]) - 1)
                Message_Log.append(f"J{process.getPID()} has been promoted to priority {process.priority[1:]}")

            #we need to check if a CPU is empty and if one is then we need to move the process to it.
            if sim.AvailableCPU_Flag() == True:
                for CPU in sim.CPU_List:
                    if CPU.getPCB() is None:
                        CPU.loadProcess(process)
                        Message_Log.append(f"J{process.getPID()} is running.")
                        break
                sim.ready.queue.remove(process)
            else:
                #we need to check the lowester priority cpu.
                lowest_cpu = None
                for cpu in sim.CPU_List:
                    if lowest_cpu == None:
                        lowest_cpu = cpu
                    if cpu.getPCB() != None:
                        if int(cpu.getPCB().priority[1:]) < int(lowest_cpu.getPCB().priority[1:]):
                            lowest_cpu = cpu
                if lowest_cpu.getPCB() != None and process > lowest_cpu.getPCB():
                    temp = lowest_cpu.getPCB()
                    lowest_cpu.loadProcess(process)
                    Message_Log.append(f"J{process.getPID()} is running.")
                    sim.ready.queue.append(temp)
                    Message_Log.append(f"J{temp.getPID()} is no longer running.")
                    sim.ready.queue.remove(process)
                else:
                    i += 1
    #   wait
    i = 0
    sim.wait.increment("waittime")
    while i < len(sim.wait.queue):
        process = sim.wait.queue[i]
        if args.type != "PR":
            #we need to check if a CPU is empty and if one is then we need to move the process to it.
            if sim.AvailableIO_Flag() == True:
                for IO in sim.IO_List:
                    if IO.getPCB() is None:
                        IO.loadProcess(process)
                        Message_Log.append(f"J{process.getPID()} has entered IO.")
                        break
                sim.wait.queue.remove(process)
            else:
                i += 1
            #we need to check the lowester priority cpu.
        else:
            if process.priority[1:] != "1" and process.getWaitTime() == 200:
                process.priority = "p" + str(int(process.priority[1:]) - 1)
                Message_Log.append(f"J{process.getPID()} has been promoted to priority {process.priority[1:]}")
            elif process.priority[1:] != "1" and process.getWaitTime() == 400:
                process.priority = "p" + str(int(process.priority[1:]) - 1)
                Message_Log.append(f"J{process.getPID()} has been promoted to priority {process.priority[1:]}")
            elif process.priority[1:] != "1" and process.getWaitTime() == 800:
                process.priority = "p" + str(int(process.priority[1:]) - 1)
                Message_Log.append(f"J{process.getPID()} has been promoted to priority {process.priority[1:]}")
            #we need to check if a CPU is empty and if one is then we need to move the process to it.
            if sim.AvailableIO_Flag() == True:
                for IO in sim.IO_List:
                    if IO.getPCB() is None:
                        IO.loadProcess(process)
                        Message_Log.append(f"J{process.getPID()} has entered IO.")
                        break
                sim.wait.queue.remove(process)
            else:
                #we need to check the lowester priority cpu.
                lowest_IO = None
                for IO in sim.IO_List:
                    if lowest_IO == None:
                        lowest_IO = IO
                    if IO.getPCB() != None:
                        if int(IO.getPCB().priority[1:]) < int(lowest_IO.getPCB().priority[1:]):
                            lowest_IO = IO
                if lowest_IO.getPCB() != None and process > lowest_IO.getPCB():
                    temp = lowest_IO.getPCB()
                    lowest_IO.loadProcess(process)
                    Message_Log.append(f"J{process.getPID()} has entered IO.")
                    sim.wait.queue.append(temp)
                    Message_Log.append(f"J{temp.getPID()} has left IO.")
                    sim.wait.queue.remove(process)
                else:
                    i += 1
    # now to process the move list.
    #adding items to the new queue
    for process in data:
        if int(process.getArrivalTime()) == int(clock):
            Move_List.append((process,0))

    #adding items to the ready queue
    if args.type != "PR":
        i = 0
        while i < len(Move_List):
            process = Move_List[i][0]
            destination = Move_List[i][1]
            if int(destination) == 0:
                sim.new.addPCB(process)
            elif int(destination) == 1:
                sim.ready.addPCB(process)
            elif int(destination) == 2:
                pass
                # for CPU in sim.CPU_List:
                #     if CPU.getPCB() is None:
                #         CPU.loadProcess(process)
                #         Message_Log.append(f"{process.getPID()} is running.")
                #         break
            elif int(destination) == 3:
                sim.wait.addPCB(process)
            elif int(destination) == 4:
                pass
                # for IO in sim.IO_List:
                #     if IO.getPCB() is None:
                #         IO.loadProcess(process)
                #         Message_Log.append(f"{process.getPID()} has entered IO.")
                #         break
            elif int(destination) == 5:
                sim.terminated.addPCB(process)
            else:
                print("Error: invalid destination")
            i += 1
    else:
        i = 0
        while i < len(Move_List):
            process = Move_List[i][0]
            destination = Move_List[i][1]
            if int(destination) == 0:
                sim.new.addPCB(process)
                sim.new.queue = sorted(sim.new.queue, key=lambda x: int(x.priority[1:]))
            elif int(destination) == 1:
                sim.ready.addPCB(process)
                sim.ready.queue = sorted(sim.ready.queue, key=lambda x: int(x.priority[1:]))
            elif int(destination) == 2:
                pass
#                 for CPU in sim.CPU_List:
#                     #round one of searching for empty cpus
#                     if CPU.getPCB() is None:
#                         CPU.loadProcess(process)
#                         Message_Log.append(f"{process.getPID()} is running.")
#                         break
#                     #round find the cpu with the lowest priority process
#                     #if it is lower than the current process then we swap them
#                     else:
#                         lowest_cpu = None
#                         for cpu in sim.CPU_List:
#                             if lowest_cpu == None:
#                                 lowest_cpu = cpu
#                             if cpu.getPCB() != None:
#                                 if int(cpu.getPCB().priority[1:]) < int(lowest_cpu.getPCB().priority[1:]):
#                                     lowest_cpu = cpu
#                         #now that we have the lowest cpu we check if the process is higher priority than the lowest cpu
#                         if lowest_cpu.getPCB() != None:
# #                            print(lowest_cpu.getPCB())
#                             if int(process.priority[1:]) > int(lowest_cpu.getPCB().priority[1:]):
#                                 #if it is then we swap them
#                                 temp = lowest_cpu.getPCB()
#                                 lowest_cpu.loadProcess(process)
#                                 #adding the old process to the ready queue
#                                 Move_List.append((temp,1))
#                                 break
            elif int(destination) == 3:
                sim.wait.addPCB(process)
                sim.wait.queue = sorted(sim.wait.queue, key=lambda x: int(x.priority[1:]))
            elif int(destination) == 4:
                pass
                # for IO in sim.IO_List:
                #     #round one of searching for empty cpus
                #     if IO.getPCB() is None:
                #         IO.loadProcess(process)
                #         break
                #     #round find the cpu with the lowest priority process
                #     #if it is lower than the current process then we swap them
                #     else:
                #         lowest_IO = None
                #         for IO in sim.IO_List:
                #             if lowest_IO == None:
                #                 lowest_IO = IO
                #             if IO.getPCB() != None:
                #                 if IO < lowest_IO:
                #                     lowest_IO = IO
                #         #now that we have the lowest cpu we check if the process is higher priority than the lowest cpu
                #         if lowest_IO.getPCB() != None:
                #             if process > lowest_IO.getPCB():
                #                 #if it is then we swap them
                #                 temp = lowest_IO.getPCB()
                #                 lowest_IO.loadProcess(process)
                #                 #adding the old process to the ready queue
                #                 Move_List.append((temp,3))
                #                 break            
            elif int(destination) == 5:
                Message_Log.append(f"J{process.getPID()} has excited.")
                Message_Log.append(f"J{process.getPID()}: ST={process.getArrivalTime()}, TAT={process.getTurnaroundTime()}, RT={process.getWaitTime()}, IWT={process.getIOTime()}")
                # ST={process.getArrivalTime()}, TAT={process.getTurnaroundTime()}, RT={process.getWaitTime()}, IWT={process.getIOTime()}
                sim.terminated.addPCB(process)
            else:
                print("Error: invalid destination")        
            i += 1
    Move_List = []

#  this is for testing our cpu and io usage per clock cycle

#    print("time: " + str(clock))

#    print ("CPU usage: " + str(sim.getUsedCPU()) + "/" + str(sim.getnumCPU()))

    # Test: New Queue
    temp_new = ""
    for process in sim.new:
        temp_new += f"[J{process.getPID()}, {str(clock)}] "
#    print(f"New Queue: {temp_new}")

    # Test: Ready Queue
    temp_ready = ""
    for process in sim.ready.queue:
        temp_ready += f"[J{process.getPID()}, {process.getReadyTime()}] "
#    print(f"Ready Queue: {temp_ready}")

    # Test: Running Queue
    temp_run = ""
    for CPU in sim.CPU_List:
        if CPU.getPCB() is not None:
            temp_run += f"[J{CPU.getPCB().getPID()}, {CPU.getPCB().getCurrentBurstTime()}] "
#    print(f"Running Queue: {temp_run}")

    # Test: Waiting Queue
    temp_wait = ""
    for process in sim.wait.queue:
        temp_wait += f"[J{process.getPID()}, {process.getWaitTime()}] "
#    print(f"Waiting Queue: {temp_wait}")

    # Test: IO Queue
    temp_io = ""
    for IO in sim.IO_List:
        if IO.getPCB() is not None:
            temp_io += f"[J{IO.getPCB().getPID()}, {IO.getPCB().getCurrentBurstTime()}] "
#    print(f"IO Queue: {temp_io}")

    # Test: Exit Queue
    temp_exit = ""
    for process in sim.terminated.queue:
        temp_exit += f"[J{process.getPID()}] "
#    print(f"Exit Queue: {temp_exit}\n")

#            print(CPU.getPCB())
#            print("\n")
#            print(CPU.getPCB().getReadyTime())
#            print(CPU.getPCB().getCpuTime())
#            print(CPU.getPCB().getWaitTime())
#            print(CPU.getPCB().getIOTime())

#    print ("IO usage: " + str(sim.getUsedIO()) + "/" + str(sim.getnumIO()))
#    for IO in sim.IO_List:
#        if IO.getPCB() is not None:
#            print(IO.getPCB())



#  this is for our outputs per clock cycle

#    print("time: " + str(clock))
#    print(sim)
    timer = args.timer

    # with Live(generate_table(), refresh_per_second=4) as live:
    #     i = int(1)
    #     live.update(generate_table())
    #     # for _ in range(i):
        #     live.update(generate_table())

# CODE FOR PRINTING

    iteration_count += 1
    if iteration_count % skipp == 0:

        print(f"\n \n [bold green]Clock Ticks:[/bold green] [bold red]{str(clock)}[/bold red]\n")
        print(generate_table())        
        messages = "\n".join(Message_Log)
        panel_content = f"[bold green]Messages: [/bold green]\n{messages}"
        panel = Panel(panel_content,width=int(terminal_width*0.5))
        console.print(panel)

        # for line in Message_Log:
        #     panel_content = line
        #     panel = Panel(panel_content)
        #     console.print(panel)

        time.sleep(timer)



    #clearing the message log at the end of the cycle.
    Message_Log = []
#    print(sim.timeSlice)
    #increments our clock
    clock.increment()
    #checks if we are done
    if sim.isDone():
        conditional = False
#for process in sim.terminated.queue:
#    print(process)
#print(sim)

# this is to print out the final results of our wait times.
# we will print out the average wait time for each queue.
# we will also print out the average turnaround time for each process.
# print("Final Results:")


ready_time = 0
cpu_time = 0
wait_time = 0
io_time = 0
turnaround_time = 0

for process in sim.terminated.queue:
    ready_time += process.getReadyTime()
    cpu_time += process.getCpuTime()
    wait_time += process.getWaitTime()
    io_time += process.getIOTime()
    turnaround_time += int(process.getTurnaroundTime())


# Calculate the averages
ready_time_avg = ready_time / len(sim.terminated.queue)
cpu_time_avg = cpu_time / len(sim.terminated.queue)
wait_time_avg = wait_time / len(sim.terminated.queue)
io_time_avg = io_time / len(sim.terminated.queue)
turnaround_time_avg = turnaround_time / len(sim.terminated.queue)

# Averages Table
avg_table = Table(show_lines=True)
avg_table.title="[bold red]Averages[/bold red]"
avg_table.add_column("Metric", style="bold")
avg_table.add_column("Clock Ticks", style="bold")
avg_table.add_row("Ready Wait Time", f"{round(ready_time_avg, 2)}")
avg_table.add_row("CPU Time", f"{round(cpu_time_avg, 2)}")
avg_table.add_row("Wait Time", f"{round(wait_time_avg, 2)}")
avg_table.add_row("IO Time", f"{round(io_time_avg, 2)}")
avg_table.add_row("Turnaround Time", f"{round(turnaround_time_avg, 2)}")

# CPU Utilization
cpu_usage = 0
cpu_table = Table(show_lines=True)
cpu_table.title="[bold green]CPU Utilization[/bold green]"
cpu_table.add_column("CPU", style="bold")
cpu_table.add_column("Utilization", style="bold")

i = 0
for CPU in sim.CPU_List:
    cpu_downtime = CPU.getIdleTime()
    cpu_runtime = int(clock) - cpu_downtime
    cpu_usage += cpu_runtime
    cpu_percentage = (cpu_runtime / int(clock)) * 100
    cpu_table.add_row(f"CPU {i}", f"{cpu_percentage:.2f}%")
    i += 1

# IO Utilization
io_usage = 0
io_table = Table(show_lines=True)
io_table.title="[bold blue]IO Utilization[/bold blue]"
io_table.add_column("IO", style="bold")
io_table.add_column("Utilization", style="bold")

i = 0
for IO in sim.IO_List:
    io_downtime = IO.getIdleTime()
    io_runtime = int(clock) - io_downtime
    io_usage += io_runtime
    io_percentage = (io_runtime / int(clock)) * 100
    io_table.add_row(f"IO {i}", f"{io_percentage:.2f}%")
    i += 1

# Print the tables using rich
print("\n")
columns = Columns([avg_table, "   ", cpu_table, "   ", io_table])
console = Console()
console.print(columns)
print("\n")

# for process in sim.terminated.queue:
#     print(f"{process.getPID()}: {process.getTurnaroundTime()}")