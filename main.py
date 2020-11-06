import numpy as np

class TooManyUnknowns(Exception):
	pass

class Truss:
	def __init__(self, joints, members, loads):
		self.members = [Member((joints[i[0]], joints[i[1]])) for i in members]
		self.loads = {i: loads[i] if i in loads else 0 for i in joints}


		# Calculate reactions
		left_reaction_point = min(joints, key=lambda x: joints[x][0])
		right_reaction_point = max(joints, key=lambda x: joints[x][0])

		right_reaction_force = -np.sum([self.loads[i]*(joints[i][0]-joints[left_reaction_point][0]) for i in self.loads])\
										/(joints[right_reaction_point][0]-joints[left_reaction_point][0])

		left_reaction_force = -np.sum(list(self.loads.values()))-right_reaction_force

		self.loads[left_reaction_point] += left_reaction_force
		self.loads[right_reaction_point] += right_reaction_force

		self.joints = []
		for i in joints:
			self.joints.append(Joint([m for m in self.members if joints[i] in m.ends], joints[i], self.loads[i]))

	def solve(self):
		solved = []
		while None in [m.tension for m in self.members]:
			j = min([i for i in self.joints if i not in solved], key=lambda x: x.unknowns())
			try:
				j.solve()
			except np.linalg.LinAlgError:
				raise TooManyUnknowns

			solved.append(j)

class Joint:
	def __init__(self, members, coords, load=0):
		self.members = members
		self.coords = coords
		self.load = load

	def unknowns(self):
		return [m.tension for m in self.members].count(None)

	def solve(self):
		directions = [m.direction(self.coords) for m in self.members if m.tension is None]

		A = np.array([[i[j] for i in directions] for j in (0,1)])
		b = np.array([[-np.sum([m.direction(self.coords)[0]*m.tension for m in self.members if m.tension is not None])],
					  [-self.load-np.sum([m.direction(self.coords)[1]*m.tension for m in self.members if m.tension is not None])]])
		
		if len(directions) > 1:
			x = list(np.linalg.solve(A, b).transpose()[0])
		else:
			x = [b[0][0]/A[0][0]]

		knowns = [m for m in self.members if m.tension is None]
		for t in range(len(list(x))):
			knowns[t].tension = x[t]

class Member:
	def __init__(self, ends):
		self.ends = ends
		self.tension = None
	
	def direction(self, coords):
		'''
		Return the direction (xdirection, ydirection) of the member from the given coords
		'''
		if coords not in self.ends:
			return (0, 0)

		if coords == self.ends[0]:
		   direction = ((self.ends[1][0]-self.ends[0][0])/np.sqrt((self.ends[1][0]-self.ends[0][0])**2+(self.ends[1][1]-self.ends[0][1])**2),
		   				(self.ends[1][1]-self.ends[0][1])/np.sqrt((self.ends[1][0]-self.ends[0][0])**2+(self.ends[1][1]-self.ends[0][1])**2))
		else:
		   direction = ((self.ends[0][0]-self.ends[1][0])/np.sqrt((self.ends[1][0]-self.ends[0][0])**2+(self.ends[1][1]-self.ends[0][1])**2),
		   				(self.ends[0][1]-self.ends[1][1])/np.sqrt((self.ends[1][0]-self.ends[0][0])**2+(self.ends[1][1]-self.ends[0][1])**2))
		
		return direction

if __name__ == "__main__":
	joints = {'A': (0,0), 'B': (3,4), 'C': (6,0), 'D': (9,4), 'E': (12,0)}
	members = ['AB','AC','BC', 'BD', 'CD', 'CE', 'DE']
	loads = {'C': -100}
	truss = Truss(joints, members, loads)
	truss.solve()
	for i in range(len(truss.members)):
		print(members[i]+':', truss.members[i].tension)