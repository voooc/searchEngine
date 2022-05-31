# -!- coding: utf-8 -!-
class Heap:
    def __init__(self, arr):
        self.arr = arr

    def heap_insert(self, index):
        """依次看它的父节点的值是否大于它如果大于就交换"""""
        while self.arr[index] < self.arr[int((index - 1) / 2)]:
            self.arr[index], self.arr[int((index - 1) / 2)] = self.arr[int((index - 1) / 2)], self.arr[index]
            index = int((index - 1) / 2)

    def heapify(self, index, size):
        left = index * 2 + 1
        while left < size:
            """""寻找左子节点和右子节点的最大值"""""
            """""left + 1为右子节点"""""
            """""当右子节点存在且右子节点的值大于左子节点的值的时候，largest才是右子节点"""""
            if left + 1 < size and self.arr[left + 1] < self.arr[left]:
                largest = left + 1
            else:
                largest = left
            """""把左右子节点中的最大值和父节点进行比较，来判断是否进行交换"""""
            if self.arr[largest] > self.arr[index]:
                largest = index
            if largest == index:
                break
            self.arr[largest], self.arr[index] = self.arr[index], self.arr[largest]
            index = largest
            left = index * 2 + 1

    def heap_sort(self):
        size = len(self.arr)
        if self.arr == [] or len(self.arr) < 2:
            return
        """""建立小根堆"""""
        for i in range(len(self.arr)):
            self.heap_insert(i)
        size = size - 1
        self.arr[0], self.arr[size] = self.arr[size], self.arr[0]
        while size > 0:
            self.heapify(0, size)
            size = size - 1
            self.arr[0], self.arr[size] = self.arr[size], self.arr[0]

