"""Задание №7
-Напишите программу на Python, которая будет находить сумму элементов массива из
 1000000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
-Массив должен быть заполнен случайными целыми числами от 1 до 100.
-При о решении задачи нужно использовать многопоточность, многопроцессорность
и асинхронность.
-В каждом решении нужно вывести время выполнения вычислений.
"""
import multiprocessing
import threading
import time
from random import randint
import asyncio

DECIM = 100_000

TOTAL = 1000_000


def generate_array():
    arr = [randint(1, 100) for i in range(TOTAL)]
    return arr


summa = 0


def get_sum(list, num):
    global summa
    for i in list:
        summa += i
    print(f"Сумма элементов массива ({num}): {summa}")


async def get_sum_async(list, num):
    global summa
    for i in list:
        summa += i
    print(f"Сумма элементов массива ({num}): {summa}")


def summa_threading(list):
    threads = []
    start_time = time.time()

    for i in range(10):
        start_index = i * DECIM
        end_index = start_index + DECIM
        t = threading.Thread(target=get_sum(list[start_index:end_index], i+1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time() - start_time
    print('завершение  потоков')
    print('результат суммирования массива:', summa)
    print(f"Общее время работы при многопоточном подходе: {end_time:.10f} seconds \n")
    return end_time


def summa_process(list):
    start_time = time.time()
    processes = []
    for i in range(10):
        start_index = i * DECIM
        end_index = start_index + DECIM
        p = multiprocessing.Process(target=get_sum(list[start_index:end_index], i+1))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    end_time = time.time() - start_time
    print('завершение  процессов')
    print('результат суммирования массива:', summa)
    print(f"Общее время работы при мультипроцессорном подходе: {end_time:.10f} seconds \n")
    return end_time


async def summa_async(list):
    tasks = []
    for i in range(10):
        start_index = i * DECIM
        end_index = start_index + DECIM
        task = asyncio.ensure_future(get_sum_async(list[start_index:end_index], i+1))
        tasks.append(task)
    await asyncio.gather(*tasks)
    end_time = time.time() - start_time
    print('завершение  асинхронного метода')
    print('результат суммирования массива:', summa)
    print(f"Общее время работы при асинхронном  подходе: {end_time:.10f} seconds \n")
    return end_time


if __name__ == "__main__":
    list = generate_array()

    print('\t Старт суммирования')
    start_time = time.time()
    get_sum(list, 1)
    end_time = time.time() - start_time
    print('завершение  суммирования')
    print('результат суммирования массива:', summa)
    print(f"Общее время работы при синхронном  подходе: {end_time:.10f} seconds \n")

    summa = 0

    print('\t Старт потоков')
    summa_threading(list)

    summa = 0
    print('\t Старт процессов')
    summa_process(list)

    summa = 0
    print('\t Старт асинхронного метода')
    start_time = time.time()
    loop = asyncio.get_event_loop()  # получили цикл событий
    loop.run_until_complete(summa_async(list))




