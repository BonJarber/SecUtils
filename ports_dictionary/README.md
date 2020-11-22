## ports.json
If you have a project that needs to label ports, this is a dictionary mapping every port to it's name and description

```python
import json
with open('ports.json', 'r') as portfile:
  ports = json.load(portfile)

ports['22']['tcp']['name']
'ssh'

ports['22']['tcp']['desc']
'The Secure Shell (SSH) Protocol'
```
