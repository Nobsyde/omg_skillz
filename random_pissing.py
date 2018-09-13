from itertools import product
import random
import numpy as np
np.set_printoptions(threshold=np.inf)

SIZE_BATHROOM = 100
SIZE_PISS = 200 #keep this number low, don't piss outside the jar or joyrex will ban you
RANDOM_TRIGGERS = 4 #less is more

flow = [(0,0)]
bathroom = np.empty((SIZE_BATHROOM, SIZE_BATHROOM), dtype='str')
bathroom[:] = ' '
bathroom[0,0] = '.'

def neighbours(cell):
    for c in product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= n < SIZE_BATHROOM for n in c):
            yield c

def is_pissed_everywhere(pisses):
  pissed_everywhere = True
  for tile in pisses:
    if(bathroom[tile] == ' '):
      pissed_everywhere = False
      break
  return pissed_everywhere
 
flow_x = np.zeros(SIZE_PISS) 
flow_y = np.zeros(SIZE_PISS) 

last_piss = (0,0)
for i in range(1, SIZE_PISS):
    negative = False
    while(not negative):
      val = random.randint(1, 8) 
      if val == 1: 
          flow_x[i] = flow_x[i - 1] + 1
          flow_y[i] = flow_y[i - 1] 
      elif val == 2: 
          flow_x[i] = flow_x[i - 1] - 1
          flow_y[i] = flow_y[i - 1] 
      elif val == 3: 
          flow_x[i] = flow_x[i - 1] 
          flow_y[i] = flow_y[i - 1] + 1
      elif val == 4: 
          flow_x[i] = flow_x[i - 1] 
          flow_y[i] = flow_y[i - 1] - 1
      elif val == 5: 
          flow_x[i] = flow_x[i - 1] + 1
          flow_y[i] = flow_y[i - 1] + 1
      elif val == 6: 
          flow_x[i] = flow_x[i - 1] - 1
          flow_y[i] = flow_y[i - 1] + 1
      elif val == 7: 
          flow_x[i] = flow_x[i - 1] - 1
          flow_y[i] = flow_y[i - 1] - 1
      elif val == 8: 
          flow_x[i] = flow_x[i - 1] + 1
          flow_y[i] = flow_y[i - 1] - 1
      if(flow_x[i] >= 0 and flow_y[i] >=0):
        negative = True
      if(i > 1 and flow_x[i] == flow_x[i - 2] and flow_y[i] == flow_y[i -2]):
        negative = False
      next_piss = (int(flow_x[i]), int(flow_y[i]))
      last_piss = (int(flow_x[i-1]), int(flow_y[i-1]))
      if(bathroom[next_piss] != ' '):
        pisses = list(neighbours(last_piss))
        if(is_pissed_everywhere(pisses)):
          negative = True
        else:
          negative = False
    
    next_piss = (int(flow_x[i]), int(flow_y[i]))
    bathroom[next_piss] = '.'
    last_piss = next_piss

bathroom = bathroom[~np.all(bathroom == ' ', axis=0)]    
bathroom = bathroom[~np.all(bathroom == ' ', axis=1)]    

with open('res.txt', 'w') as f:
  for r in range(bathroom.shape[0]):
    for c in range(bathroom.shape[1]):
      f.write(bathroom[r,c])
    f.write('\n')

TS = '[triggered]'
TE = '[/triggered]'
count_triggered = 0
with open('res_triggered.txt', 'w') as f:
  f.write('[COLOR=\"Yellow\"]')
  for r in range(bathroom.shape[0]):
    for c in range(bathroom.shape[1]):
      trig_string = ''
      if(random.randint(0,RANDOM_TRIGGERS) == 0 and bathroom[r,c] == '.'):
        trig_string = TS
        count_triggered += 1
      f.write(trig_string+bathroom[r,c])
    f.write('\n')
  for n in range(count_triggered):
    f.write(TE)
  f.write('[/COLOR]')
