from gurobipy import *

import time

class Simon:
	def __init__(self, Round, activebits, word_len, word, bit):
		self.Round = Round
		self.activebits = activebits
		self.word = word
		self.bit = bit
		self.blocksize = 2 * word_len
		self.objectiveBound = self.blocksize - 1
		self.WORD_LENGTH = word_len
		self.filename_model = "Simon_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".lp"
		self.filename_modelv2 = "Simon_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + "v2.lp"
		self.filename_modelv3 = "Simon_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + "v3.lp"
		self.filename_result = "result_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".txt"
		self.filename_constraint = "constraint_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileobj = open(self.filename_modelv2, "w")
		fileobj.close()		
		fileobj = open(self.filename_modelv3, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()
		fileboj = open(self.filename_constraint, "a")
		fileobj.close()

	# Rotational constants
	R1 = 1
	R2 = 8
	R3 = 2

	def CreateVariable(self, n, x):
		"""
		Generate variables used in the model.
		"""
		variable = []
		for i in range(0, self.WORD_LENGTH):
			variable.append(x + "_" + str(n) + "_" + str(i))
		return variable

	def CreateObjectiveFunction(self):
		"""
		Create Objective function of the MILP model.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,self.WORD_LENGTH):
			eqn.append("x" + "_0_" + str(i))
		for j in range(0,self.WORD_LENGTH):
			eqn.append("y" + "_0_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	def Createv2(self):
		fileobj = open(self.filename_modelv2, "w")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,self.WORD_LENGTH):
			eqn.append("x" + "_0_" + str(i))
		for j in range(0,self.WORD_LENGTH):
			eqn.append("y" + "_0_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

		fileobj = open(self.filename_constraint, "r")
		lines=fileobj.readlines()
		fileobj.close()

		fileobj = open(self.filename_modelv2, "a")
		fileobj.write("Subject To\n")
		for line in lines:
			fileobj.write(line)

		fileobj.write("Binary\n")
		for i in range(0, 1):
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("x_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("y_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def VariableRotation(self, x, n):
		"""
		Bit Rotation.
		"""
		eqn = []
		for i in range(0, self.WORD_LENGTH):
			eqn.append(x[(i + n) % self.WORD_LENGTH])
		return eqn

	def CreateConstrainsSplit(self,x_in, u, v, w, y_out):
		"""
		Generate constraints by split operation.
		"""
		fileobj = open(self.filename_model, "a")
		for i in range(0, self.WORD_LENGTH):
			eqn = []
			eqn.append(x_in[i])
			eqn.append(u[i])
			eqn.append(v[i])
			eqn.append(w[i])
			eqn.append(y_out[i])
			temp = " - ".join(eqn)
			temp = temp + " = " + str(0)
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def CreateConstrainsSplitv3(self,x_in, u, v, w, y_out):
		"""
		Generate constraints by split operation.
		"""
		fileobj = open(self.filename_modelv3, "a")
		for i in range(0, self.WORD_LENGTH):
			eqn = []
			eqn.append(x_in[i])
			eqn.append(u[i])
			eqn.append(v[i])
			eqn.append(w[i])
			eqn.append(y_out[i])
			temp = " - ".join(eqn)
			temp = temp + " = " + str(0)
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def CreateConstraintsAnd(self, u,v,t):
		"""
		Generate constraints by and operation.
		"""
		fileobj = open(self.filename_model, "a")
		for i in range(0, self.WORD_LENGTH):
			fileobj.write((t[i] + " - " + u[i] + " >= " + str(0)))
			fileobj.write("\n")
			fileobj.write((t[i] + " - " + v[i] + " >= " + str(0)))
			fileobj.write("\n")
			fileobj.write((t[i] + " - " + u[i] + " - " + v[i] + " <= " + str(0)))
			fileobj.write("\n")
		fileobj.close()

	def CreateConstraintsAndv3(self, u,v,t):
		"""
		Generate constraints by and operation.
		"""
		fileobj = open(self.filename_modelv3, "a")
		for i in range(0, self.WORD_LENGTH):
			fileobj.write((t[i] + " - " + u[i] + " >= " + str(0)))
			fileobj.write("\n")
			fileobj.write((t[i] + " - " + v[i] + " >= " + str(0)))
			fileobj.write("\n")
			fileobj.write((t[i] + " - " + u[i] + " - " + v[i] + " <= " + str(0)))
			fileobj.write("\n")
		fileobj.close()

	def CreateConstraintsXor(self, y_in, t, w, x_out):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model, "a")
		for i in range(0, self.WORD_LENGTH):
			eqn = []
			eqn.append(x_out[i])
			eqn.append(y_in[i])
			eqn.append(t[i])
			eqn.append(w[i])
			temp = " - ".join(eqn)
			temp = temp + " = " + str(0)
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def CreateConstraintsXorv3(self, y_in, t, w, x_out):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_modelv3, "a")
		for i in range(0, self.WORD_LENGTH):
			eqn = []
			eqn.append(x_out[i])
			eqn.append(y_in[i])
			eqn.append(t[i])
			eqn.append(w[i])
			temp = " - ".join(eqn)
			temp = temp + " = " + str(0)
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def Init(self):
		"""
		Generate constraints by the initial division property.
		"""
		assert(self.activebits < (2 * self.WORD_LENGTH))
		fileobj = open(self.filename_model, "a")
		x = self.CreateVariable(0,"x")
		y = self.CreateVariable(0,"y")
		if self.activebits <= self.WORD_LENGTH:
			for i in range(0,self.activebits):
				fileobj.write((y[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(1)))
				fileobj.write("\n")
			for i in range(self.activebits,self.WORD_LENGTH):
				fileobj.write((y[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(0)))
				fileobj.write("\n")
			for i in range(0,self.WORD_LENGTH):
				fileobj.write((x[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(0)))
				fileobj.write("\n")

		else:
			for i in range(0, self.WORD_LENGTH):
				fileobj.write((y[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(1)))
				fileobj.write("\n")
			for i in range(0, (self.activebits - self.WORD_LENGTH)):
				fileobj.write((x[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(1)))
				fileobj.write("\n")
			for i in range((self.activebits - self.WORD_LENGTH), self.WORD_LENGTH):
				fileobj.write((x[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(0)))
				fileobj.write("\n")
		fileobj.close()

	def CreateConstraints(self):
		"""
		Generate constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		eqn = []
		for i in range(0,self.WORD_LENGTH):
			eqn.append("x" + "_0_" + str(i))
		for j in range(0,self.WORD_LENGTH):
			eqn.append("y" + "_0_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
		for j in range(0,self.WORD_LENGTH):
			if ((self.word == 0) and (j == self.bit)):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(j) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(j) + " = 0\n")
		for j in range(0,self.WORD_LENGTH):
			if ((self.word == 1) and (j == self.bit)):
				fileobj.write("y" + "_" + str(self.Round) + "_" + str(j) + " = 1\n")
			else:
				fileobj.write("y" + "_" + str(self.Round) + "_" + str(j) + " = 0\n")
		fileobj.close()
		# Init(file)
		x_in = self.CreateVariable(0,"x")
		y_in = self.CreateVariable(0,"y")
		for i in range(0, self.Round):
			u = self.CreateVariable(i,"u")
			v = self.CreateVariable(i,"v")
			w = self.CreateVariable(i,"w")
			t = self.CreateVariable(i,"t")
			x_out = self.CreateVariable((i+1), "x")
			y_out = self.CreateVariable((i+1), "y")
			self.CreateConstrainsSplit(x_in, u, v, w, y_out)
			u = self.VariableRotation(u, Simon.R1)
			v = self.VariableRotation(v, Simon.R2)
			w = self.VariableRotation(w, Simon.R3)
			self.CreateConstraintsAnd(u, v, t)
			self.CreateConstraintsXor(y_in, t, w, x_out)
			x_in = x_out
			y_in = y_out

	def CreateConstraintsv2(self):
		"""
		Generate constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		#fileobj.write("Subject To\n")
		eqn = []
		for i in range(0,self.WORD_LENGTH):
			eqn.append("x" + "_0_" + str(i))
		for j in range(0,self.WORD_LENGTH):
			eqn.append("y" + "_0_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
		for j in range(0,self.WORD_LENGTH):
			if ((self.word == 0) and (j == self.bit)):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(j) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(j) + " = 0\n")
		for j in range(0,self.WORD_LENGTH):
			if ((self.word == 1) and (j == self.bit)):
				fileobj.write("y" + "_" + str(self.Round) + "_" + str(j) + " = 1\n")
			else:
				fileobj.write("y" + "_" + str(self.Round) + "_" + str(j) + " = 0\n")
		fileobj.close()
		# Init(file)
		x_in = self.CreateVariable(0,"x")
		y_in = self.CreateVariable(0,"y")
		for i in range(0, self.Round):
			u = self.CreateVariable(i,"u")
			v = self.CreateVariable(i,"v")
			w = self.CreateVariable(i,"w")
			t = self.CreateVariable(i,"t")
			x_out = self.CreateVariable((i+1), "x")
			y_out = self.CreateVariable((i+1), "y")
			self.CreateConstrainsSplit(x_in, u, v, w, y_out)
			u = self.VariableRotation(u, Simon.R1)
			v = self.VariableRotation(v, Simon.R2)
			w = self.VariableRotation(w, Simon.R3)
			self.CreateConstraintsAnd(u, v, t)
			self.CreateConstraintsXor(y_in, t, w, x_out)
			x_in = x_out
			y_in = y_out

	def CreateConstraintsv3(self):
		"""
		Generate constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,self.WORD_LENGTH):
			eqn.append("x" + "_0_" + str(i))
		for j in range(0,self.WORD_LENGTH):
			eqn.append("y" + "_0_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.write("Subject To\n")

		for j in range(0,self.WORD_LENGTH):
			if ((self.word == 0) and (j == self.bit)):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(j) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(j) + " = 0\n")
		for j in range(0,self.WORD_LENGTH):
			if ((self.word == 1) and (j == self.bit)):
				fileobj.write("y" + "_" + str(self.Round) + "_" + str(j) + " = 1\n")
			else:
				fileobj.write("y" + "_" + str(self.Round) + "_" + str(j) + " = 0\n")
		fileobj.close()
		# Init(file)
		x_in = self.CreateVariable(0,"x")
		y_in = self.CreateVariable(0,"y")
		for i in range(0, self.Round):
			u = self.CreateVariable(i,"u")
			v = self.CreateVariable(i,"v")
			w = self.CreateVariable(i,"w")
			t = self.CreateVariable(i,"t")
			x_out = self.CreateVariable((i+1), "x")
			y_out = self.CreateVariable((i+1), "y")
			self.CreateConstrainsSplitv3(x_in, u, v, w, y_out)
			u = self.VariableRotation(u, Simon.R1)
			v = self.VariableRotation(v, Simon.R2)
			w = self.VariableRotation(w, Simon.R3)
			self.CreateConstraintsAndv3(u, v, t)
			self.CreateConstraintsXorv3(y_in, t, w, x_out)
			x_in = x_out
			y_in = y_out

	def BinaryVariable(self):
		"""
		Specify variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0, self.Round):
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("x_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("y_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("u_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("v_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("w_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("t_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
		for j in range(0, self.WORD_LENGTH):
			fileobj.write(("x_" + str(self.Round) + "_" + str(j)))
			fileobj.write("\n")
		for j in range(0, self.WORD_LENGTH):
			fileobj.write(("y_" + str(self.Round) + "_" + str(j)))
			fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def BinaryVariablev3(self):
		"""
		Specify variable type.
		"""
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Binary\n")
		for i in range(0, self.Round):
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("x_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("y_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("u_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("v_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("w_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("t_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
		for j in range(0, self.WORD_LENGTH):
			fileobj.write(("x_" + str(self.Round) + "_" + str(j)))
			fileobj.write("\n")
		for j in range(0, self.WORD_LENGTH):
			fileobj.write(("y_" + str(self.Round) + "_" + str(j)))
			fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def MakeModel(self):
		"""
		Write the MILP model into the file
		"""
		self.CreateObjectiveFunction()
		self.CreateConstraints()
		#self.Init()
		self.BinaryVariable()

	def WriteObjective(self, obj):
		"""
		Write the objective value into filename_result.
		"""
		fileobj = open(self.filename_result, "a")
		fileobj.write("The objective value = %d\n" %obj.getValue())
		eqn1 = []
		eqn2 = []
		for i in range(0, self.blocksize):
			u = obj.getVar(i)
			if u.getAttr("x") != 0:
				eqn1.append(u.getAttr('VarName'))
				eqn2.append(u.getAttr('x'))
		length = len(eqn1)
		for i in range(0,length):
			s = eqn1[i] + "=" + str(eqn2[i])
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()

	def SolveModel(self):
		"""
		Solve the MILP model to search the integral distinguisher of Lblock.
		"""
		time_start = time.time()
		m = read(self.filename_model)
		counter = 0
		set_zero = []
		global_flag = False
		while (global_flag == False):
			m = read(self.filename_model)
			m.params.threads=8
			"""if counter<100:
        			m.params.TimeLimit=30
			elif counter<200:
        			m.params.TimeLimit=180
			elif counter<300:
        			m.params.TimeLimit=240
			elif counter<400:
        			m.params.TimeLimit=300
			elif counter<500:
        			m.params.TimeLimit=360
			else:
        			m.params.TimeLimit=420"""       
			m.params.TimeLimit=3600
			m.optimize()
			counter = counter+1
			obj = m.getObjective()
			print("**********************************************\n")
			print(m.Status)
			print("\n**********************************************\n")
			#if ((obj.getValue() > 1)&(obj.getValue() <self.blocksize)):
			if((m.Status == 2) or (m.Status == 9)):
				if ((m.ObjVal > 0)&(m.ObjVal <self.blocksize)):	#not infeasible
					self.objectiveBound = m.ObjVal
					obj = m.getObjective()
					#m.write("/home/az/Desktop/Khalesi/Division/Code/LBlock/1.sol")
					if obj.getValue() > 0:
						os.remove(self.filename_model)
						self.CreateObjectiveFunction()
						fileobj = open(self.filename_model, "a")
						fileobj.write("Subject To\n")
						fileobj.close()
						eqn = []
						for i in range(0, self.blocksize):
							u = obj.getVar(i)
							temp = u.getAttr('x')
							if temp == 0:
								eqn.append(u.getAttr('VarName'))
						temp = " + ".join(eqn)
						fileobj = open(self.filename_constraint, "a")
						fileobj.write(temp)
						fileobj.write(" >= 1\n")
						fileobj.close()
						fileobj = open(self.filename_constraint, "r")
						lines=fileobj.readlines()
						fileobj.close()
						fileobj = open(self.filename_model, "a")
						for line in lines:
							fileobj.write(line)
						fileobj.close()
						self.CreateConstraintsv2()
						#self.Init()
						self.BinaryVariable()
				else:
					global_flag = True
					self.Createv2()
					m = read(self.filename_modelv2)
					m.params.threads=8
					#m.params.TimeLimit=3600
					m.optimize()

					if m.Status == 2:				
						obj = m.getObjective()
						#m.write("/home/az/Desktop/Khalesi/Division/Code/LBlock/v2.sol")
						constbit=0
						eqncnst = []
						for i in range(0, self.blocksize):
							u = obj.getVar(i)
							temp = u.getAttr('x')
							if temp == 0:
								constbit += 1
								eqncnst.append(u.getAttr('VarName'))
						if (constbit == 0):
							print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&outputbit is unknown\n")
							fileobj = open(self.filename_result, "a")	
							fileobj.write("\nIntegral Distinguisher Do NOT Exist!\n\n")
							fileobj.write("\nNo. of Const bit is: ")
							fileobj.write(str(constbit))	
							fileobj.close()
							global_flag = True
							break
						temp = " + ".join(eqncnst)
						self.CreateConstraintsv3()
						fileobj = open(self.filename_modelv3, "a")
						fileobj.write(temp)
						fileobj.write(" = 0\n")
						print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
						print(constbit)
						print("!!!***********************\n")
						print(temp)
						print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
						eqn = []
						for i in range(0,self.WORD_LENGTH):
							eqn.append("x" + "_0_" + str(i))
						for j in range(0,self.WORD_LENGTH):
							eqn.append("y" + "_0_" + str(j))
						temp1 = " + ".join(eqn)
						fileobj.write(temp1)
						fileobj.write(" = " + str(self.blocksize-constbit) + "\n")
						fileobj.close()                                        
						self.BinaryVariablev3()
						m = read(self.filename_modelv3)
						m.params.threads=8
						#m.params.TimeLimit=3600
						m.optimize()
						fileobj = open(self.filename_result, "a")
						if m.Status == 3:		
							fileobj.write("\nIntegral Distinguisher Found!\n\n")
							fileobj.write("\nNo. of Const bit is: ")
							fileobj.write(str(constbit))
							fileobj.write(str(eqncnst))
						else:	
							fileobj.write("\nv3_1_m.status:\n")
							fileobj.write(str(m.Status))
						fileobj.close()
			else:
				global_flag = True
				self.Createv2()
				m = read(self.filename_modelv2)
				m.params.threads=8
				#m.params.TimeLimit=3600
				m.optimize()

				if m.Status == 2:				
					obj = m.getObjective()
					#m.write("/home/az/Desktop/Khalesi/Division/Code/LBlock/v2.sol")
					constbit=0
					eqncnst = []
					for i in range(0, self.blocksize):
						u = obj.getVar(i)
						temp = u.getAttr('x')
						if temp == 0:
							constbit += 1
							eqncnst.append(u.getAttr('VarName'))
					if (constbit == 0):
						print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&outputbit is unknown\n")
						fileobj = open(self.filename_result, "a")	
						fileobj.write("\nIntegral Distinguisher Do NOT Exist!\n\n")
						fileobj.write("\nNo. of Const bit is: ")
						fileobj.write(str(constbit))	
						fileobj.close()
						global_flag = True
						break
					temp = " + ".join(eqncnst)
					self.CreateConstraintsv3()
					fileobj = open(self.filename_modelv3, "a")
					fileobj.write(temp)
					fileobj.write(" = 0\n")
					print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
					print(constbit)
					print("!!!***********************\n")
					print(temp)
					print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
					eqn = []
					for i in range(0,self.WORD_LENGTH):
						eqn.append("x" + "_0_" + str(i))
					for j in range(0,self.WORD_LENGTH):
						eqn.append("y" + "_0_" + str(j))
					temp1 = " + ".join(eqn)
					fileobj.write(temp1)
					fileobj.write(" = " + str(self.blocksize-constbit) + "\n")
					fileobj.close()                                        
					self.BinaryVariablev3()
					m = read(self.filename_modelv3)
					m.params.threads=8
					#m.params.TimeLimit=3600
					m.optimize()
					fileobj = open(self.filename_result, "a")	
					if m.Status == 3:
						fileobj.write("\nIntegral Distinguisher Found!\n\n")
						fileobj.write("\nNo. of Const bit is: ")
						fileobj.write(str(constbit))	
						fileobj.write(str(eqncnst))
					else:	
						fileobj.write("\nv3_2_m.status:\n")
						fileobj.write(str(m.Status))
					fileobj.close()
		time_end = time.time()		
		fileobj = open(self.filename_result, "a")	
		fileobj.write("\nspent time in sec:\n")
		fileobj.write(str(time_end-time_start))	
		fileobj.close()						
