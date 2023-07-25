#Activate JUMP or NJUMP
JUMP = "JUMP"


class Register(object):
    def __init__(self, name, reorder = None):
        self.name = name
        self.reorder = reorder
        self.busy = False
    def clear(self):
        self.reorder = ""
        self.busy = False

class Instruction(object):
    def __init__(self, op, rs1, rs2=None, rd=None, shamt=None, imn=None, cycle = None):
        self.opname = op
        self.destination = rd
        self.source1 = rs1
        self.source2 = rs2
        self.immediate = shamt
        self.position = imn
        if self.opname in ['ADD','SUB']:
            self.cycle = 2
        elif self.opname in ['SLLI','SRLI','OR','BEQ','BNE','AND']:
            self.cycle = 1
        elif self.opname in ['LW','LB']:
            self.cycle = 3
        else:
            self.cycle = cycle
        self.ready = False
    
    def exe (self):
        if  self.cycle > 0:
            self.cycle-=1
            if self.cycle == 0:
                self.ready = True

    def __str__(self):
        st = ''
        if self.opname in ['SLLI', 'SRLI']:
            st = self.opname + ' ' + str(self.destination) + ', ' + str(self.source1) + ', ' + str(self.immediate)
        elif self.opname in ['LW', 'LB']:
            st = self.opname + ' ' + str(self.destination) + ', ' + str(self.source1) + ', ' + str(self.position)
        elif self.opname in ['BEQ', 'BNE']:
            st = self.opname + ' ' + str(self.source1) + ', ' + str(self.source2) + ', ' + str(self.position)
        else:
            st = self.opname + ' ' + str(self.destination) + ', ' + str(self.source1) + ', ' + str(self.source2)
        return st
    

class ReorderBufferPos(object):
    def __init__(self,id,busy,instruction,state,destination, value=None):
        self.id = id
        self.busy = busy
        self.instruction = instruction
        self.state =  state
        self.destination = destination
        self.value = value

    def clear(self):
        self.busy = False
        self.instruction = ''
        self.state = ''
        self.destination = ''
        self.value = ''

    def __str__(self):
        st= f'#{self.id} {self.busy} {self.instruction} {self.state} {self.destination} {self.value}' 
        return st



class ReservationStation(object):
    def __init__(self, opName, op = None,Vj = None,Vk = None,Qj = None,Qk = None,destination = None):
        self.opName = opName
        self.op = op
        self.busy = False
        self.Vj = Vj
        self.Vk = Vk
        self.Qj = Qj
        self.Qk = Qk
        self.destination = destination

    def clear(self):
        self.op = None
        self.busy = False
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.destination = None
    
    def isclear(self):
        return  self.op is None and self.busy is False and self.Vj is None and self.Vk is None and self.Qj is None and  self.Qk is None and  self.destination is None

def isRegCreated(r,RL):
    if r in RL:
        return True
    return False

def load_instructions (RL):
    program = []
    instructions = open("instructions.txt", 'r')
    for line in instructions.readlines():
        args = line.split()
        
        if len(args) == 0:
            pass
        else:
            tokens = line.split()
            opname = tokens[0]

            if opname in ['SLLI','SRLI']:
                destination = tokens[1].rstrip(',')
                if  not isRegCreated(destination,RL):
                    RL.append(destination)
                source1 = tokens[2].rstrip(',')
                if  not isRegCreated(source1,RL):
                    RL.append(source1)
                immediate = tokens[3]
                instruction = Instruction(opname, source1, None, destination, immediate)
            elif opname =='LW':
                destination = tokens[1].rstrip(',')
                if  not isRegCreated(destination,RL):
                    RL.append(destination)
                source1 = tokens[2].rstrip(',')
                if  not isRegCreated(source1,RL):
                    RL.append(source1)
                position = tokens[3]
                instruction = Instruction(opname, source1, None, destination, None, position)
            elif opname in ['SW','BEQ','BNE']:
                source1 = tokens[1].rstrip(',')
                if  not isRegCreated(source1,RL):
                    RL.append(source1)
                source2 = tokens[2].rstrip(',')
                if  not isRegCreated(source2,RL):
                    RL.append(source2)
                position = tokens[3]
                instruction = Instruction(opname, source1, source2, None, None, position)
            else:            
                destination = tokens[1].rstrip(',')
                if  not isRegCreated(destination,RL):
                    RL.append(destination)
                source1 = tokens[2].rstrip(',')
                if  not isRegCreated(source1,RL):
                    RL.append(source1)
                source2 = tokens[3]
                if  not isRegCreated(source2,RL):
                    RL.append(source2)
                instruction = Instruction(opname, source1, source2, destination)
            print(instruction)
            program.append(instruction)
            instructions.close
    return program




def print_reorder_buffer(entries):
    column_sizes = [8, 7, 19, 18, 13, 21]

    print('-' * (sum(column_sizes) + 19))
    print('|', end='')

    headers = ['Entry', 'Busy', 'Instruction', 'State', 'Destination', 'Value']
    for i, header in enumerate(headers):
        print(f' {header:<{column_sizes[i]}} |', end='')

    print('\n' + '-' * (sum(column_sizes) + 19))

    for entry in entries:
        busy = 'Yes' if entry.busy else 'No'
        print('|', end='')
        print(f' {entry.id:<{column_sizes[0]}} |', end='')
        print(f' {busy:<{column_sizes[1]}} |', end='')
        print(f' {str(entry.instruction):<{column_sizes[2]}} |', end='')
        print(f' {entry.state:<{column_sizes[3]}} |', end='')
        print(f' {entry.destination:<{column_sizes[4]}} |', end='')
        print(f' {entry.value:<{column_sizes[5]}} |')

    print('-' * (sum(column_sizes) + 19))

def print_reservation_stations(entries):

    column_sizes = [8, 7, 5, 20, 20, 5, 5, 6]

    print('-' * (sum(column_sizes) + 25))
    print('|', end='')

    headers = ['Name', 'Busy', 'Op', 'Vj', 'Vk', 'Qj', 'Qk', 'Dest']
    for i, header in enumerate(headers):
        print(f' {header:<{column_sizes[i]}} |', end='')

    print('\n' + '-' * (sum(column_sizes) + 25))

    for entry in entries:
        busy = 'Yes' if entry.busy else 'No'
        print('|', end='')
        print(f' {entry.opName:<{column_sizes[0]}} |', end='')
        print(f' {busy:<{column_sizes[1]}} |', end='')
        print(f' {str(entry.op) if entry.op is not None else "" :<{column_sizes[2]}} |', end='')
        print(f' {str(entry.Vj) if entry.Vj is not None else "":<{column_sizes[3]}} |', end='')
        print(f' {str(entry.Vk) if entry.Vk is not None else "":<{column_sizes[4]}} |', end='')
        print(f' {str(entry.Qj) if entry.Qj is not None else "":<{column_sizes[5]}} |', end='')
        print(f' {str(entry.Qk) if entry.Qk is not None else "":<{column_sizes[6]}} |', end='')
        print(f' {str(entry.destination)if entry.destination is not None else "":<{column_sizes[7]}} |')

    print('-' * (sum(column_sizes) + 25))

def print_registers(entries):
    column_sizes = [8, 7, 5, 20, 20, 5, 5, 6]
    st1 = 'Fields  |'
    st2 = 'Reorder |'
    st3 = 'Busy    |'
    for entry in entries:
        busy = 'Yes' if entry.busy else 'No'
        
        st1+= f'{entry.name if entry.name is not None else "  " :<{column_sizes[2]}} | '
        st2+= f'{entry.reorder if entry.reorder is not None else "  " :<{column_sizes[2]}} | '
        st3 += f'{busy :<{column_sizes[2]}} | '

    print(st1)
    print(st2)
    print(st3)

def issue(ROP,p):
    id=0
    for i in p :
        if i.destination:
            destination = i.destination
        else:
            destination = JUMP
        ROP.append(ReorderBufferPos(id=id,busy=False,instruction=i,state="Issued",destination=destination,value="")) 
        id+=1

def findAvaliableRS(inst,RSP):
    i=0
    for rs in RSP:
        if inst.opname in ['LW','LB']:
            if rs.opName.startswith("MEM"):
                if rs.isclear():
                    return i
        elif inst.opname  in ['ADD','SUB']:        
            if rs.opName.startswith("ATM"):
                if rs.isclear():
                    return i
        else :
            if rs.opName.startswith("LOG"):
                if rs.isclear():
                    return i
        i+=1
    return -1

def findLastEntry(roi,ROP,reg):
    if roi == 0 :
        return None
    for i in range(roi-1, -1, -1):
        if reg.name == ROP[i].destination and ROP[i].state != 'Commit':
            return i
    return None

def execute(roi,ROP,RSP,RLT):
    inst = ROP[roi].instruction
    rs = findAvaliableRS(inst,RSP)
    if rs != -1:
        RS=RSP[rs]
        find = False
        for reg in RLT:
            if reg.name == inst.source1:
                    if reg.busy:
                        h = findLastEntry(roi,ROP,reg)

                        if h is not None and ROP[h].state == 'Write result':
                            RS.Vj = reg.name
                        else:
                            RS.Qj = reg.reorder
                    else:
                        RS.Vj = reg.name
                    find = True

        
        find = False

        if inst.source2:
            for reg in RLT:
                if reg.name == inst.source2:
                    if reg.busy:
                        h = findLastEntry(roi,ROP,reg)

                        if h is not None and ROP[h].state == 'Write result':
                            RS.Vk = reg.name
                        else:
                            RS.Qk = reg.reorder
                    else:
                        RS.Vk = reg.name
                    find = True
            if not find:
                RS.Vk =reg.name
            

        if inst.destination not in ['JUMP']:
            for reg in RLT:
                if reg.name == inst.destination:
                    if not reg.busy:
                        reg.reorder = roi
                        reg.busy = True
                        ROP[roi].state = 'Execute'
                        ROP[roi].busy = True
                        break

        RS.destination = roi
        RS.busy = True
        RS.op = inst.opname
        ROP[roi].state = 'Execute'
        ROP[roi].busy = True

def refRO_or_reg(rs,V,RLT,ROP):
    
    if isinstance(V, int):
        if ROP[V].value != '':
            return True
        else:
            return False
    else:
        return writeready(rs,V,RLT)
    
        

def writeready(rs,V,RLT):
    for reg in RLT:
        if reg.name == V :
            if  reg is not None or reg.reorder > rs.destination:
                return True
    return False

def cycle_count(ROP):
    for ro in ROP:
        if ro.busy == True and ro.state =='Execute':
            ro.instruction.exe()

def write_result(ROP,RSP,RLT):
    for rs in RSP:
        if (rs.Qj is None and rs.Qk is None) and ((rs.Vj is None or refRO_or_reg(rs,rs.Vj,RLT,ROP) ) and (rs.Vk is None or refRO_or_reg(rs,rs.Vk,RLT,ROP))) :   

            if rs.busy is True:

                    temp = rs.destination
                    for rop in ROP:
                        if rop.instruction.ready is True: 
                            if rop.id == temp:
                                if rop.instruction.opname == 'ADD':
                                    rop.value = f'{rs.Vj} + {rs.Vk}'
                                elif rop.instruction.opname == 'SUB':
                                    rop.value = f'{rs.Vj} - {rs.Vk}'
                                elif rop.instruction.opname == 'OR':
                                    rop.value = f'{rs.Vj} | {rs.Vk}'
                                elif rop.instruction.opname == 'AND':
                                    rop.value = f'{rs.Vj} & {rs.Vk}'
                                elif rop.instruction.opname in ['SLLI','SRLI']:
                                    rop.value = f'{rs.Vj} /* '
                                elif rop.instruction.opname in ['LW','LB']:
                                    rop.value = f'Mem[{int(rop.instruction.position) * 4} + {rs.Vj}]'
                                elif rop.instruction.opname in ['BEQ','BNE']:
                                    rop.value = f'{JUMP}'
                                else:
                                    rop.value = f'ERRO'
                                rop.state = 'Write result'
                                
                                for rs2 in RSP:
                                    if rs2.Qj == temp:
                                        rs2.Vj = rs2.Qj
                                        rs2.Qj = None
                                    if rs2.Qk == temp:
                                        rs2.Vk = rs2.Qk 
                                        rs2.Qk = None
                                rs.busy = False
                                rs.clear()

def getROPHead(ROP):
    i = 0
    for ro in ROP:
        if i != 0: 
            if ROP[i-1].state == "Commit" and ro.state == "Write result":
                return i
        else:
            if ro.state == "Write result":
                return i
        i+=1

    return -1

def commit(ROP,RSP,RLT):
    head = getROPHead(ROP)
    if head != -1:
        if ROP[head].instruction.opname in ["BNE","BEQ"]:
            if ROP[head].value == 'JUMP'  and head != len(ROP):
                for i in range(head+1,len(ROP)):
                    ROP[i].clear()
                    for reg in RLT:
                        reg.clear()
                    for rs in RSP:
                        rs.clear()
                ROP[head].busy = False
                ROP[head].state = "Commit"            
            else:
                ROP[head].busy = False
                ROP[head].state = "Commit"
        else:
            dest=ROP[head].destination
            for reg in RLT:
                if reg.name == dest:
                    reg.clear()
                    for i in range(head+1,len(ROP)):
                        if ROP[i].destination == reg.name:
                            reg.reorder = ROP[i].id
                            reg.busy = True
                            break
            ROP[head].busy = False
            ROP[head].state = "Commit"


def checkCycles(ROP):
    print("Current cycles")
    for r in ROP:
        if r.instruction != '' :
            print(f'r{r.id} cycle {r.instruction.cycle} ready {r.instruction.ready} state {r.state}')


def createRS(UF,RSP):
    for s in UF:
        RSP.append(ReservationStation(s))

def print_tables(ROP,RSP,RLT):
    print_reorder_buffer(ROP)
    print_reservation_stations(RSP)
    print_registers(RLT)

def finish(ROP):
    for rop in ROP:
        if  rop.state != 'Commit' and rop.state != '' :
            return False 
    return True


ROP = []
#UF = ["MEM1","MEM2","ATM1","ATM2","ATM3","LOG1","LOG2","LOG3"]
#UF = ["MEM1","ATM1","ATM2","LOG1"]
UF = ["MEM1","MEM2","ATM1","ATM2","ATM3","LOG1","LOG2"]
RSP = []
RL = []
p = load_instructions(RL)
RLT = []
for r in RL:
    RLT.append(Register(r))

createRS(UF,RSP)
issue(ROP,p)

print_reorder_buffer(ROP)
print_reservation_stations(RSP)
print_registers(RLT)


i = 0
step_by_step= input("0 if you want to run all at any point: ")
while (finish(ROP) != True):
    print("COMMIT")
    if step_by_step != '0':
        step_by_step= input(" Continue  ? any key = y , 0 = n ")
    commit(ROP,RSP,RLT)
    print_tables(ROP,RSP,RLT)
    print("WRITE RESULT")
    if step_by_step != '0':
        step_by_step= input(" Continue  ? any key = y , 0 = n ")
    write_result(ROP,RSP,RLT)
    print_tables(ROP,RSP,RLT)
    print("EXECUTE")
    if step_by_step != '0':
        step_by_step= input(" Continue  ? any key = y , 0 = n ")
    for p in ROP:
        if p.state == 'Issued':
            execute(p.id,ROP,RSP,RLT)
    print(f'cycle =  {i}')
    cycle_count(ROP)
    checkCycles(ROP)
    print_tables(ROP,RSP,RLT)
    i+=1

print("Program comitted all instructions of the Reorder Buffer")

