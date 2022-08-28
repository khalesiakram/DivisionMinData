from gurobipy import *

import time
import os

class Gift:
	counter=0
	def __init__(self, Round, outputbit):
		self.Round = Round
		self.outputbit = outputbit
		self.blocksize = 128
		self.objectiveBound = self.blocksize - 1		
		self.filename_model = "Gift_" + str(self.Round) + "_" + str(self.outputbit) + ".lp"
		self.filename_modelv2 = "Gift_" + str(self.Round) + "_" + "_bit" + str(self.outputbit) + "v2.lp"
		self.filename_modelv3 = "Gift_" + str(self.Round) + "_" + "_bit" + str(self.outputbit) + "v3.lp"				
		self.filename_result = "result_" + str(self.Round) + "_" + "_bit" + str(self.outputbit) + ".txt"
		self.filename_constraint = "constraint_" + str(self.Round) + "_" + "_bit" + str(self.outputbit) + ".txt"		
		fileobj = open(self.filename_model, "w")
		#fileobj.write("Subject To\n")
		fileobj.close()
		fileobj = open(self.filename_modelv2, "w")
		fileobj.close()		
		fileobj = open(self.filename_modelv3, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()
		fileboj = open(self.filename_constraint, "a")
		fileobj.close()
		

	# Linear inequalities for the PRESENT Sbox
	S_T=[[1, 1, 1, 1, -1, -1, -1, -1, 0],\
             [-3, -3, -5, -4, 2, 3, 1, 1, 8],\
             [-3, -2, 3, -1, -1, -2, -4, 3, 7],\
             [-1, -1, -1, 0, 2, 3, 1, 1, 0],\
             [0, 0, 0, 3, -1, -2, -1, -1, 2],\
             [0, -1, 0, -2, -1, 1, 2, -2, 4],\
             [1, 0, 0, -1, 1, -1, -2, -1, 3],\
             [-3, -1, -5, -6, 2, 1, 5, 3, 8],\
             [0, 1, 3, 1, -2, -2, -1, -2, 2],\
             [0, 1, 0, 3, -2, -2, -1, -1, 2],\
             [-1, -1, 0, -1, 3, 2, 2, 1, 0],\
             [0, -1, 0, -1, 0, -1, 1, 1, 2],\
             [2, 1, 0, 1, -1, -2, -1, -2, 2],\
             [0, -2, -2, -1, 1, 2, 1, 1, 2],\
             [-1, 0, 0, -2, -1, 1, -2, 2, 4]]
	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,128):
			eqn.append("x" + "_0_" + str(i))
		#for i in range(0,128):
			#eqn.append("k_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	def Createv2(self):
		fileobj = open(self.filename_modelv2, "w")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,128):
			eqn.append("x" + "_0_" + str(i))
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
			for j in range(0,128):
				fileobj.write("x_" + str(i) + "_" + str(j))
				fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()	
	@staticmethod
	def CreateVariables(n,s):
		"""
		Generate the variables used in the model.
		"""
		array = []
		for i in range(0,128):
			array.append((s + "_" + str(n) + "_" + str(i)))
		return array

	
	def ConstraintsBySbox(self, varIn, varOut):
		"""
		Generate the constraints by sbox layer.
		"""
		fileobj = open(self.filename_model,"a")
		for k in range(0,32):
			for coff in Gift.S_T:
				temp = []
				for u in range(0,4):
					temp.append(str(coff[u]) + " " + varIn[(k * 4) + 3 - u])
				for v in range(0,4):
					temp.append(str(coff[v + 4]) + " " + varOut[(k * 4) + 3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[Gift.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 

	def ConstraintsBySboxv3(self, varIn, varOut):
		"""
		Generate the constraints by sbox layer.
		"""
		fileobj = open(self.filename_modelv3,"a")
		for k in range(0,32):
			for coff in Gift.S_T:
				temp = []
				for u in range(0,4):
					temp.append(str(coff[u]) + " " + varIn[(k * 4) + 3 - u])
				for v in range(0,4):
					temp.append(str(coff[v + 4]) + " " + varOut[(k * 4) + 3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[Gift.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 		
	@staticmethod
	def LinearLaryer(variable):
		"""
		Linear layer of Gift.
		"""
		#permutation=[0,17,34,51,48,1,18,35,32,49,2,19,16,33,50,3,4,21,38,55,52,5,22,39,36,53,6,23,20,37,54,7,8,25,42,59,56,9,26,43,40,57,10,27,24,41,58,11,12,29,46,63,60,13,30,47,44,61,14,31,28,45,62,15]
		permutation=[0,33,66,99,96,1,34,67,64,97,2,35,32,65,98,3,4,37,70,103,100,5,38,71,68,101,6,39,36,69,102,7,8,41,74,107,104,9,42,75,72,105,10,43,40,73,106,11,12,45,78,111,108,13,46,79,76,109,14,47,44,77,110,15,16,49,82,115,112,17,50,83,80,113,18,51,48,81,114,19,20,53,86,119,116,21,54,87,84,117,22,55,52,85,118,23,24,57,90,123,120,25,58,91,88,121,26,59,56,89,122,27,28,61,94,127,124,29,62,95,92,125,30,63,60,93,126,31]
#permutation=[0,5,10,15,16,21,26,31,32,37,42,47,48,53,58,63,12,1,6,11,28,17,22,27,44,33,38,43,60,49,54,59,8,13,2,7,24,29,18,23,40,45,34,39,56,61,50,55,4,9,14,3,20,25,30,19,36,41,46,35,52,57,62,51]
		array = ["" for i in range(0,128)]
		for i in range(0,128):
			array[i] = variable[permutation[i]]
		return array


	def Constraint(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")

		eqn = []
		for i in range(0,128):
			eqn.append("x" + "_0_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
		
		for i in range(0,128):
			if (i == self.outputbit):
				fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + " = 0\n")
		fileobj.close()		
				
		variablein = Gift.CreateVariables(0,"x")
		variableout = Gift.CreateVariables(1,"x")
		variableout = Gift.LinearLaryer(variableout)
		#variablek = Gift.CreateKeyVariables()

		if self.Round == 1:
			self.ConstraintsBySbox(variablein, variableout)
			# omit the last linear layer
		else:
			self.ConstraintsBySbox(variablein, variableout)
			for i in range(1, self.Round):
				variablein = Gift.CreateVariables(i,"x")
				variableout = Gift.CreateVariables(i+1,"x")                                
				variableout = Gift.LinearLaryer(variableout)
				self.ConstraintsBySbox(variablein, variableout)
				#omit the last linear layer

	def Constraint2(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		#fileobj.write("Subject To\n")

		eqn = []
		for i in range(0,self.blocksize):
			eqn.append("x" + "_0_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
		
		for i in range(0,self.blocksize):
			if (i == self.outputbit):
				fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + " = 0\n")
		fileobj.close()		
				
		variablein = Gift.CreateVariables(0,"x")
		variableout = Gift.CreateVariables(1,"x")
		variableout = Gift.LinearLaryer(variableout)
		#variablek = Gift.CreateKeyVariables()

		if self.Round == 1:
			self.ConstraintsBySbox(variablein, variableout)
			# omit the last linear layer
		else:
			self.ConstraintsBySbox(variablein, variableout)
			for i in range(1, self.Round):
				variablein = Gift.CreateVariables(i,"x")
				variableout = Gift.CreateVariables(i+1,"x")                                
				variableout = Gift.LinearLaryer(variableout)
				self.ConstraintsBySbox(variablein, variableout)
				#omit the last linear layer


	def Constraint3(self):
		"""
		Generate the constraints used in the MILP model.
		"""

		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,self.blocksize):
			eqn.append("x" + "_0_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		
		fileobj.write("Subject To\n")
		
		for i in range(0,self.blocksize):
			if (i == self.outputbit):
				fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + " = 0\n")
		fileobj.close()		
				
		variablein = Gift.CreateVariables(0,"x")
		variableout = Gift.CreateVariables(1,"x")
		variableout = Gift.LinearLaryer(variableout)
		#variablek = Gift.CreateKeyVariables()

		if self.Round == 1:
			self.ConstraintsBySboxv3(variablein, variableout)
			# omit the last linear layer
		else:
			self.ConstraintsBySboxv3(variablein, variableout)
			for i in range(1, self.Round):
				variablein = Gift.CreateVariables(i,"x")
				variableout = Gift.CreateVariables(i+1,"x")                                
				variableout = Gift.LinearLaryer(variableout)
				self.ConstraintsBySboxv3(variablein, variableout)
				#omit the last linear layer


	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0, (self.Round)+1):
			for j in range(0,self.blocksize):
				fileobj.write("x_" + str(i) + "_" + str(j))
				fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()
		
	def VariableBinaryv3(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Binary\n")
		for i in range(0, (self.Round)+1):
			for j in range(0,self.blocksize):
				fileobj.write("x_" + str(i) + "_" + str(j))
				fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()		
		
	def Init(self):
		"""
		Generate the constraints introduced by the initial division property.
		"""
		variableout = Gift.CreateVariables(self.Round,"x")
		fileobj = open(self.filename_model, "a")
		eqn = []
		for i in range(0, self.blocksize):
			if(i==self.outputbit):
				temp = variableout[63 - i] + " = 1"
				fileobj.write(temp)
				fileobj.write("\n")
			else:	
				temp = variableout[63 - i] + " = 0"
				fileobj.write(temp)
				fileobj.write("\n")
		fileobj.close()

	def MakeModel(self):
		"""
		Generate the MILP model of Gift given the round number and activebits.
		"""
		self.CreateObjectiveFunction()
		self.Constraint()
		#self.Init()
		self.VariableBinary()

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
		Solve the MILP model to search the integral distinguisher of Present.
		"""
		time_start = time.time()
		m = read(self.filename_model)
		set_zero = []
		global_flag = False
		while (global_flag == False):
			m = read(self.filename_model)
			m.params.threads=8	
			#m.params.TimeLimit=36000
			m.optimize()
			obj = m.getObjective()
			print("**********************************************\n")
			print(m.Status)
			print("\n**********************************************\n")
			if((m.Status == 2) or (m.Status == 9) or (m.Status == 11)):							
				if ((m.ObjVal > 0)&(m.ObjVal <self.blocksize)):	#not infeasible
					self.objectiveBound = m.ObjVal
					obj = m.getObjective()
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
							#print(u.getAttr('VarName'))
							#print(temp)
							if temp < 0.1:
								eqn.append(u.getAttr('VarName'))
						temp = " + ".join(eqn)
						fileobj = open(self.filename_constraint, "a")
						fileobj.write(temp)
						print("----------------------debug")
						print(temp)
						fileobj.write(" >= 1\n")
						fileobj.close()
						fileobj = open(self.filename_constraint, "r")
						lines=fileobj.readlines()
						fileobj.close()
						fileobj = open(self.filename_model, "a")
						for line in lines:
							fileobj.write(line)
						fileobj.close()
						self.Constraint2()
						#self.Init()
						self.VariableBinary()
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
							if temp < 0.1:
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
						self.Constraint3()
						fileobj = open(self.filename_modelv3, "a")
						fileobj.write(temp)
						fileobj.write(" = 0\n")
						print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
						print(constbit)
						print("!!!***********************\n")
						print(temp)
						print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
						eqn = []
						for i in range(0,self.blocksize):
							eqn.append("x" + "_0_" + str(i))
						temp1 = " + ".join(eqn)
						fileobj.write(temp1)
						fileobj.write(" = " + str(self.blocksize-constbit) + "\n")
						fileobj.close()                                        
						self.VariableBinaryv3()
						m = read(self.filename_modelv3)
						m.params.threads=8
						#m.params.TimeLimit=3600
						m.optimize()
						if m.Status == 3:
							fileobj = open(self.filename_result, "a")	
							fileobj.write("\nIntegral Distinguisher Found!\n\n")
							fileobj.write("\nNo. of Const bit is: ")
							fileobj.write(str(constbit))
						else:
							fileobj = open(self.filename_result, "a")	
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
						if temp < 0.1:
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
					self.Constraint3()
					fileobj = open(self.filename_modelv3, "a")
					fileobj.write(temp)
					fileobj.write(" = 0\n")
					print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
					print(constbit)
					print("!!!***********************\n")
					print(temp)
					print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
					eqn = []
					for i in range(0,self.blocksize):
						eqn.append("x" + "_0_" + str(i))
					temp1 = " + ".join(eqn)
					fileobj.write(temp1)
					fileobj.write(" = " + str(self.blocksize-constbit) + "\n")
					fileobj.close()                                        
					self.VariableBinaryv3()
					m = read(self.filename_modelv3)
					m.params.threads=8
					#m.params.TimeLimit=3600
					m.optimize()
					if m.Status == 3:
						fileobj = open(self.filename_result, "a")	
						fileobj.write("\nIntegral Distinguisher Found!\n\n")
						fileobj.write("\nNo. of Const bit is: ")
						fileobj.write(str(constbit))	
						fileobj.close()
					else:
						fileobj = open(self.filename_result, "a")	
						fileobj.write("\nv3_2_m.status:\n")
						fileobj.write(str(m.Status))
						fileobj.close()
