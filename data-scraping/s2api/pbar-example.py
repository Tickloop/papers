from tqdm import tqdm
import threading
import time

def my_func(pbar: tqdm):
    for i in range(100):
        pbar.update(1)
        time.sleep(0.1)

colors = ['red', 'green', 'blue']
threads = [
    threading.Thread(target=my_func, args=(tqdm(total=100, desc=f'File {idx}', colour=colors[idx], ascii=True), ))
    for idx in range(3)
]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

