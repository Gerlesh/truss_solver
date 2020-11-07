# Truss Tension Solver

Provide information into the `Truss` class, e.g.:
```py
# joints: dict of {name: coords} pairs
joints = {'A': (0,0), 'B': (3,4), 'C': (6,0), 'D': (9,4), 'E': (12,0)}

# members: list of endpoints for each member
members = ['AB','AC','BC', 'BD', 'CD', 'CE', 'DE']

# loads: dict of {joint: vertical load} pairs (up = +)
loads = {'C': -100}

truss = Truss(joints, members, loads)
```

Then solve the forces in the truss members using the `solve` method of `Truss` and get the tension in each member:
```py
truss.solve()

for i in range(len(truss.members)):
	print(members[i]+':', truss.members[i].tension)

# Output:
# AB: -62.5
# AC: 37.5
# BC: 62.5
# BD: -75.0
# CD: 62.5
# CE: 37.5
# DE: -62.5
```