import sys
arr = [int(x) for x in sys.argv[1:]] # Don't change this line

def swapList(newList):
    size = len(newList)
     
    # Swapping 
    temp = newList[0]
    newList[0] = newList[size - 1]
    newList[size - 1] = temp
     
    return newList
     
 
print(swapList(arr))
