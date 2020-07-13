from multiprocessing import Process

def test(data):
    for i in data:
        print(i)

if __name__ == "__main__":
    data = [i for i in range(20)]
    p = Process(target = test, args = (data, ))
    p.start()
    p.join()