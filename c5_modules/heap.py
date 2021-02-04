# coding=utf8
"""
@project: python3
@file: heap
@author: mike
@time: 2021/2/4
 
@function:
"""
import heapq

heap = []
heapq.heappush(heap, (5, 'a'))
heapq.heappush(heap, (2, 'b'))
heapq.heappush(heap, (4, 'c'))

for _ in range(len(heap)):
    print(heapq.heappop(heap))

h = [1, 5, 11, 10, 3, 6, 20, 8, 7, 2, 9]
heapq.heapify(h)
for _ in range(len(h)):
    print(heapq.heappop(h))
