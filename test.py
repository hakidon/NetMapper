import threading
import other_file

results = []

def my_function(i):
    result = other_file.my_function(i)
    results.append(result)

threads = []
for i in range(10):
    t = threading.Thread(target=my_function, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(results)