# SecUtils
Random utilities from my security projects that might be useful to others

## ports.json
```python
import json
with open('ports.json', 'r') as portfile:
  ports = json.load(portfile)

ports['22']['tcp']['name']
'ssh'

ports['22']['tcp']['desc']
'The Secure Shell (SSH) Protocol'```
