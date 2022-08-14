
class Node:
    def __init__(self, name,parent = None ,g = 0 , h = 0 ):
        self.name = name
        self.parent = parent
        self.g = g
        self.f = g + h

#viết lại hàm split nhận vào một chuỗi dữ liệu và trả và một list số nguyên
def split(line):
    list =[]
    tmp = line.split()
    for i in range(len(tmp)):
        list.append((int)(tmp[i]))
    return list

# đọc dữ liệu trong file
def readFile(filename):
    with open (filename, 'r') as f :
        N = (int)(f.readline())
        start , goal , search = split(f.readline())
        Matrix = []
        for i in range(N):
            Matrix.append(split(f.readline()))
        heristic = split(f.readline())

    return start, goal , search , Matrix ,heristic

def writeFile(filename, expanded , path):
    with open(filename,'w') as f:
        for x in expanded:
            f.write((str)(x) + ' ')
        f.write('\n')
        if path == 'No path':
            f.write(path)
        else :
            for x in path:
                f.write((str)(x) + ' ')

# Tìm đường đi từ Start đến Child
def findPath(Child , path):
    if Child.parent != None :
        findPath(Child.parent,path)
        path.append(Child) 
    else:
        path.append(Child)


# Check Child có ở trong list hay k
def checkInList(Child,list):
    for x in list:
        if x.name == Child.name:
            return True
    return False

# chuyển List kiểu Node thành list kiểu bình thường
def convert(listNode):
    list =[]
    for i in range(len(listNode)):
        list.append(listNode[i].name)

    return list


def BFS(Start , Goal , Matrix):
    if Start == Goal :
        return [],Goal 

    frontier =[Node(Start)] #queue
    expanded = []

    while len(frontier) != 0:
        Parent = frontier.pop(0)
        expanded.append(Parent)

        for i in range( len(Matrix) ):
            if Matrix[Parent.name][i] != 0:
                Child = Node(i,Parent)

                #Check Goal
                if i == Goal:
                    path = [] ; findPath(Child,path)
                    return convert(expanded) ,convert(path)
                else:
                    # Check Child có ở trong expanded hay frontier không
                    if not checkInList(Child,expanded) and not checkInList(Child,frontier) :
                        frontier.append(Child)
    return convert(expanded),'No path'

def DFS(Start , Goal , Matrix):
    frontier =[Node(Start)] #stack
    expanded = []

    while len(frontier) != 0:
        Parent = frontier.pop()
        expanded.append(Parent)

        #Check Goal
        if Parent.name == Goal :
            path =[] ;findPath(Parent,path)
            return convert(expanded) ,convert(path)

        for i in range(len(Matrix)- 1 ,-1 ,-1):
            if Matrix[Parent.name][i] != 0:
                Child = Node(i,Parent)

                # tìm đường đi hiện tại
                curPath =[] ;findPath(Parent,curPath)
                #Check Child có ở trong đường đi hiện tại hay không
                if not checkInList(Child,curPath):
                        frontier.append(Child)
    return convert(expanded),'No path'

def add(frontier,Child):
    for i in range( len(frontier) ):
        #Trường hợp Child đã có trong frontier
        if frontier[i].name == Child.name:
            if frontier[i].f > Child.f:
                frontier.pop(i)
                break
            else :
                return
    #Chèn Child vào frontier
    for i in range( len(frontier) ):
        if(Child.f < frontier[i].f):
            frontier.insert(i,Child)
            return 
    #Trường hợp frontier trống hoặc Child.f >all f của frontier
    frontier.append(Child)

def  UCS(Start,Goal,Matrix):
    frontier =[Node(Start)] #priority queue
    expanded = []

    while len(frontier) != 0:
        Parent = frontier.pop(0)
        expanded.append(Parent)

         #Check Goal
        if Parent.name == Goal :
            path =[] ; findPath(Parent,path)
            return convert(expanded) ,convert(path)

        for i in range(len(Matrix)):
            if Matrix[Parent.name][i] != 0:
                Child = Node(i , Parent , Parent.g + Matrix[Parent.name][i])
                
                # Nếu Child không ở trong expanded
                if not checkInList(Child,expanded) :
                    add(frontier,Child)
    return convert(expanded),'No path'

def GBFS(Start , Goal , Matrix , Heristic):
    frontier =[Node(Start)] #priority queue
    expanded = []

    while len(frontier) != 0:
        Parent = frontier.pop(0)
        expanded.append(Parent)

         #Check Goal
        if Parent.name == Goal :
            path =[] ; findPath(Parent,path)
            return convert(expanded) ,convert(path)

        for i in range(len(Matrix)):
            if Matrix[Parent.name][i] != 0:
                Child = Node(i,Parent,0,Heristic[i])
                
                # Nếu Child không ở trong expanded
                if not checkInList(Child,expanded) :
                    add(frontier,Child)
    return convert(expanded),'No path'

def A_Star(Start ,Goal ,Matrix , Heristic):
    frontier =[Node(Start)] #priority queue
    expanded = []

    while len(frontier) != 0:
        Parent = frontier.pop(0)
        expanded.append(Parent)

         #Check Goal
        if Parent.name == Goal :
            path =[] ; findPath(Parent,path)
            return convert(expanded) ,convert(path)

        for i in range(len(Matrix)):
            if Matrix[Parent.name][i] != 0:
                Child = Node(i , Parent , Parent.g + Matrix[Parent.name][i] , Heristic[i])
                
                # Nếu Child không ở trong expanded
                if not checkInList(Child,expanded) :
                    add(frontier,Child)
    return convert(expanded),'No path'

def DLS(Start , Goal , Matrix , limit ,expanded ,path ) :
    if limit <= 0:
        return False

    expanded.append(Start)
    if Start.name == Goal :
        findPath (Start , path)
        return True
    

    for i in range(len(Matrix)):
        if (Matrix[Start.name][i] != 0):
            curNode = Node(i,Start)

            #tìm đường đi hiện tại
            curPath = [] ; findPath(Start,curPath)
            #check curNode có ở trong đường đi hiện tại hay không
            if not checkInList (curNode ,curPath):
                if DLS(curNode, Goal , Matrix ,limit - 1, expanded , path ):
                    return True
    return False
def IDS (Start , Goal , Matrix ) :
    expanded , path  = [],[]
    count = 0 # đếm số state dc mở trong một limit

    for i in range(1 , len(Matrix)):
        tmp = []
        if DLS (Node(Start) , Goal ,Matrix , i ,tmp , path) :
            expanded.extend(tmp)
            return convert(expanded), convert(path)

        if len(tmp) == count : #Nếu số node dc mở  ở limit i bằng limit i-1 -> i-1 là maxDepth và không tìm thấy Path
            return convert(expanded),'No path'
        else :
            count = len( tmp) 
            expanded.extend(tmp)

def First_choice_HC(Start , Goal , Matrix, Heristic):
    expanded =[Start]
    cur = Start            

    i = 0
    while i < len(Matrix):
        if Matrix[cur][i] != 0 and Heristic[i] < Heristic[cur]:
            expanded.append(i)
            if i == Goal :
                return expanded, expanded
            cur = i ; i = 0
        else : i+=1

    return expanded,'No path'


if __name__ == '__main__':
    filename = input('File name:')
    start, goal , search , Matrix , heristic = readFile(filename)

    if search == 0:
        expanded , path = BFS(start , goal , Matrix)
    elif search == 1:
        expanded , path = DFS(start , goal , Matrix)
    elif search == 2:
        expanded , path = UCS(start , goal , Matrix)
    elif search == 3:
        expanded , path = IDS(start , goal , Matrix)
    elif search == 4:
        expanded , path = GBFS(start , goal , Matrix,heristic )
    elif search == 5:
        expanded , path = A_Star(start , goal , Matrix,heristic )
    else:
        expanded , path = First_choice_HC(start , goal , Matrix,heristic )

    writeFile('output.txt',expanded, path)
    print('Expanded:' , expanded)
    print('Path:' , path)














    

    
    






