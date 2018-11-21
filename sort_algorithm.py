from random import randint
arr = [271,11,7676,435,399,25,23,42,5454,6575,234,6,134213,56]


def Bigarr():
    f = open(r'E:\working\Python\sort\rand.txt', 'r')
    global bigarr
    bigarr = f.read()
    f.close()
    bigarr = bigarr.split('\n')
    bigarr = [int(x) for x in bigarr]


def bubble_sort(arr):
    l = len(arr)
    i = 0
    while l >= 1:
        while i+1 < l:
            if arr[i] > arr[i+1]:
                # arr[i] += arr[i+1]
                # arr[i+1] = arr[i] - arr[i+1]
                # arr[i] = arr[i] - arr[i+1]
                TEMP = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = TEMP
            i += 1
        l -= 1
        i = 0
    return arr


def quick_sort(arr, i=None, l=None):
    if i is None:
        i, left = 0, 0
    if l is None:
        l, right = len(arr)-1, len(arr)-1

    if i >= l:
        return

    left = i
    right = l
    # rnd = randint(left, right)
    key = arr[i]
    while i < l:
        while i < l:
            if arr[l] < key:
                arr[i] = arr[l]
                break
            l -= 1

        while i < l:
            if arr[i] > key:
                arr[l] = arr[i]
                break
            i += 1

    arr[i] = key
    quick_sort(arr, left, i-1)
    quick_sort(arr, l+1, right)
    return arr


def count_sort(arr):
    l = len(arr)
    vol = [0] * l
    for i in arr:
        position = 0
        freq = 0
        for n in arr:
            if i > n:
                position += 1
            elif i == n:
                freq += 1

        for f in range(freq):
            vol[position+f] = i
    return vol


def insert_sort(lst):
    arr = lst[:]
    L = len(arr)
    if L < 2:
        return
    n = 1
    sorter = 1
    right = 0
    while sorter <= L-1:
        while arr[right] > arr[sorter] and right >= 0:
            TEMP = arr[right]
            arr[right] = arr[sorter]
            arr[sorter] = TEMP
            right -= 1
            sorter -= 1
        n += 1
        sorter = n
        right = sorter - 1
    return arr


def heap_sort():
    pass