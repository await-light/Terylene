# Terylene
The thing that make your terminal beautiful

# Example
A simple example
```python
import time
import terylene

bar = terylene.Bar(0)

for i in range(bar.totalvalues):
	bar + 1
	time.sleep(0.5)
```

And a more difficult example
```python
import time
import random
import terylene
from threading import Lock,Thread

terylene.curs_hide()

lock = Lock()

def task(y):
	bar = terylene.Bar(y,formats="[[#]] $rate$% $values$/$totalvalues$")
	for i in range(100):
		lock.acquire()
		bar + 2
		lock.release()
		time.sleep(random.random())

for i in range(10):
	Thread(target=task,args=(i,)).start()
```

# Afterwards
Enjoy it :smile: