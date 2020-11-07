from flask import Flask, render_template, request
import solver

app = Flask(__name__)

@app.route('/')
def truss():
	return render_template('index.html')

@app.route('/solve')
def solve():
	joints = {}
	for i in request.args.get('joints').split(';'):
		name, coords = i.split(':')
		if (coords[0] == '(') and (coords[-1] == ')') and (',' in coords):
			try:
				coords = tuple([int(i) for i in coords[1:-1].split(',')])
				joints[name] = coords
			except ValueError:
				return render_template('error.html')
	print(joints)
		
	members = request.args.get('members').split(';')
	try:
		loads = {i.split(':')[0]: int(i.split(':')[1]) for i in request.args.get('loads').split(';')}
	except ValueError:
		return render_template('error.html')

	try:
		truss = solver.Truss(joints, members, loads)
		truss.solve()
	except:
		return render_template('error.html')
	return render_template('solve.html', len=len, str=str, truss=truss, members=members)


if __name__ == "__main__":
    app.run(debug=True)