from gurobipy import *

import time
import os

class Lblock:
	def __init__(self, Round, word, bit):
		self.Round = Round
		self.word = word
		self.bit = bit
		self.blocksize = 64
		self.objectiveBound = self.blocksize - 1
		self.filename_model = "Lblock_" + str(self.Round) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".lp"
		self.filename_modelv2 = "Lblock_" + str(self.Round) + "_word" + str(self.word) + "_bit" + str(self.bit) + "v2.lp"
		self.filename_modelv3 = "Lblock_" + str(self.Round) + "_word" + str(self.word) + "_bit" + str(self.bit) + "v3.lp"		
		self.filename_result = "result_" + str(self.Round) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".txt"
		self.filename_constraint = "constraint_" + str(self.Round) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".txt"
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


	# Linear inequalities for the 8 Sboxes used in LBlock round function
	S_T=[[[-1, -3, -4, -2, 1, 3, 2, -1, 5],\
	[1, -1, 0, 0, -1, 1, -1, -1, 2],\
	[-1, 0, -2, -2, 1, 0, -1, 2, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[-1, -1, 0, 0, 2, 2, 1, 2, 0],\
	[0, -1, -1, -1, 2, 2, 2, 1, 0],\
	[-2, -1, 0, 1, 2, -2, -1, -2, 5],\
	[1, 1, 1, 1, -2, -2, -2, 1, 1],\
	[-1, -1, 2, 0, -1, -1, -2, 1, 3],\
	[-1, 0, 2, -1, -1, -1, 1, -2, 3],\
	[-1, 0, -1, 2, -1, -1, 1, -2, 3]],\
	\
	[[-1, -1, 0, 1, 1, -1, 0, -2, 3],\
	[-1, -3, -4, -2, 1, 3, -1, 2, 5],\
	[-1, 0, -2, -2, 1, 0, 2, -1, 3],\
	[1, -1, 0, 1, -1, 1, -2, -2, 3],\
	[-1, 0, -1, -2, 0, 0, 2, -1, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[-2, -1, -1, 0, 2, 3, 2, 1, 1],\
	[0, -1, -1, -1, 2, 2, 1, 2, 0],\
	[-1, -1, 0, 0, -1, -1, -1, 2, 3],\
	[-1, 0, -1, 2, -1, -1, -2, 1, 3],\
	[-1, 0, 2, -1, -1, -1, -2, 1, 3],\
	[1, 1, 1, 1, -2, -2, 1, -2, 1]],\
	\
	[[-1, -3, -4, -2, 2, 1, -1, 3, 5],\
	[0, 0, 0, -1, -1, -1, 1, 0, 2],\
	[0, -1, -1, 0, 1, -1, -1, 1, 2],\
	[0, 1, 0, 1, -1, -1, 0, -1, 1],\
	[-1, 0, -2, -2, -1, 1, 2, 0, 3],\
	[1, -1, 0, 1, -2, -1, -2, 1, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[0, -1, -1, -1, 2, 2, 1, 2, 0],\
	[-1, -1, 0, 0, 1, 2, 2, 2, 0],\
	[1, 1, 1, 1, -2, -2, 1, -2, 1],\
	[0, 0, 0, 2, 0, -1, -1, -1, 1],\
	[-1, 0, 2, -1, 1, -1, -2, -1, 3]],\
	\
	[[-1, -2, 0, 2, -1, -2, 1, -1, 4],\
	[-1, 0, -2, -2, 0, -1, 1, 2, 3],\
	[-1, -3, -4, -2, 3, 2, 1, -1, 5],\
	[1, 0, 1, 1, 0, -2, -1, -2, 2],\
	[-1, 0, -1, -2, 0, -1, 0, 2, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[0, -1, -1, -1, 2, 2, 2, 1, 0],\
	[-3, -1, -2, -1, 4, 1, 3, 2, 2],\
	[-1, 0, 2, -1, -1, 1, -1, -2, 3],\
	[-1, 0, -1, 2, -1, 1, -1, -2, 3],\
	[1, 1, 1, 1, -2, -2, -2, 1, 1]],\
	\
	[[-1, -3, -4, -2, 2, 1, 3, -1, 5],\
	[0, -1, -1, 0, 1, -1, 1, -1, 2],\
	[0, 0, 0, -1, -1, -1, 0, 1, 2],\
	[-1, 0, -2, -2, -1, 1, 0, 2, 3],\
	[0, 1, 0, 1, -1, -1, -1, 0, 1],\
	[1, -1, 0, 1, -2, -1, 1, -2, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[-1, -1, 0, 1, -2, 1, -1, 0, 3],\
	[-1, -1, 0, 0, 1, 2, 2, 2, 0],\
	[0, -1, -1, -1, 2, 2, 2, 1, 0],\
	[-1, 0, 2, -1, 1, -1, -1, -2, 3],\
	[-1, 0, -1, 2, 1, -1, -1, -2, 3],\
	[1, 1, 1, 1, -2, -2, -2, 1, 1]],\
	\
	[[-1, -3, -4, -2, 1, 2, 3, -1, 5],\
	[0, 0, 0, -1, -1, -1, 0, 1, 2],\
	[-1, 0, -2, -2, 1, -1, 0, 2, 3],\
	[1, -1, 0, 1, -1, -2, 1, -2, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[-1, -1, 0, 0, 2, 1, 2, 2, 0],\
	[0, -1, -1, -1, 2, 2, 2, 1, 0],\
	[1, 1, 1, 1, -2, -2, -2, 1, 1],\
	[0, 0, 0, 2, -1, 0, -1, -1, 1],\
	[-1, 0, 2, -1, -1, 1, -1, -2, 3]],\
	\
	[[-1, -1, 0, 1, 1, -1, 0, -2, 3],\
	[-1, -3, -4, -2, 1, 3, -1, 2, 5],\
	[-1, 0, -2, -2, 1, 0, 2, -1, 3],\
	[1, -1, 0, 1, -1, 1, -2, -2, 3],\
	[-1, 0, -1, -2, 0, 0, 2, -1, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[-2, -1, -1, 0, 2, 3, 2, 1, 1],\
	[0, -1, -1, -1, 2, 2, 1, 2, 0],\
	[-1, -1, 0, 0, -1, -1, -1, 2, 3],\
	[-1, 0, -1, 2, -1, -1, -2, 1, 3],\
	[-1, 0, 2, -1, -1, -1, -2, 1, 3],\
	[1, 1, 1, 1, -2, -2, 1, -2, 1]],\
	\
	[[-1, -1, 0, 1, 1, -1, 0, -2, 3],\
	[-1, -3, -4, -2, 1, 3, -1, 2, 5],\
	[-1, 0, -2, -2, 1, 0, 2, -1, 3],\
	[1, -1, 0, 1, -1, 1, -2, -2, 3],\
	[-1, 0, -1, -2, 0, 0, 2, -1, 3],\
	[1, 1, 1, 1, -1, -1, -1, -1, 0],\
	[-2, -1, -1, 0, 2, 3, 2, 1, 1],\
	[0, -1, -1, -1, 2, 2, 1, 2, 0],\
	[-1, -1, 0, 0, -1, -1, -1, 2, 3],\
	[-1, 0, -1, 2, -1, -1, -2, 1, 3],\
	[-1, 0, 2, -1, -1, -1, -2, 1, 3],\
	[1, 1, 1, 1, -2, -2, 1, -2, 1]]]
		
	# Sbox permutation
	Player = [1,3,0,2,5,7,4,6]

	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model.
		"""
		#fileobj = open(self.filename_model, "a")
		fileobj = open(self.filename_model, "w")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	def Createv2(self):
		fileobj = open(self.filename_modelv2, "w")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
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
		for i in range(0,1):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,1):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("y_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		"""for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("u_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("v_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")"""
		fileobj.write("END")
		fileobj.close()

	@staticmethod
	def CreateVariables(n,s):
		"""
		Generate the variables used in the model.
		"""
		array = [["" for i in range(0,4)] for j in range(0,8)]
		for i in range(0,8):
			for j in range(0,4):
				array[i][j] = s + "_" + str(n) + "_" + str(j) + "_" + str(i)
		return array

	def ConstraintsBySbox(self, variable1, variable2):
		"""
		Generate the constraints by Sbox layer.
		"""
		fileobj = open(self.filename_model,"a")
		for k in range(0,8):
			for coff in Lblock.S_T[7 - k]:
				temp = []
				for u in range(0,4):
					temp.append(str(coff[u]) + " " + variable1[k][3 - u])
				for v in range(0,4):
					temp.append(str(coff[4 + v]) + " " + variable2[k][3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[Lblock.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 

	def ConstraintsByCopy(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variablex[i][j])
				temp.append(variableu[i][j])
				temp.append(variabley[i][j])
				s = " - ".join(temp)
				s += " = 0"
				fileobj.write(s)
				fileobj.write("\n")
		fileobj.close()

	def ConstraintsByXor(self, variabley,variablev,variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variablex[i][j])
				temp.append(variablev[i][j])
				temp.append(variabley[i][j])
				s = " - ".join(temp)
				s += " = 0"
				fileobj.write(s)
				fileobj.write("\n")
		fileobj.close()
	def ConstraintsBySboxv3(self, variable1, variable2):
		"""
		Generate the constraints by Sbox layer.
		"""
		fileobj = open(self.filename_modelv3,"a")
		for k in range(0,8):
			for coff in Lblock.S_T[7 - k]:
				temp = []
				for u in range(0,4):
					temp.append(str(coff[u]) + " " + variable1[k][3 - u])
				for v in range(0,4):
					temp.append(str(coff[4 + v]) + " " + variable2[k][3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[Lblock.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 

	def ConstraintsByCopyv3(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_modelv3,"a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variablex[i][j])
				temp.append(variableu[i][j])
				temp.append(variabley[i][j])
				s = " - ".join(temp)
				s += " = 0"
				fileobj.write(s)
				fileobj.write("\n")
		fileobj.close()

	def ConstraintsByXorv3(self, variabley,variablev,variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_modelv3,"a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variablex[i][j])
				temp.append(variablev[i][j])
				temp.append(variabley[i][j])
				s = " - ".join(temp)
				s += " = 0"
				fileobj.write(s)
				fileobj.write("\n")
		fileobj.close()

	@classmethod
	def NibblePermutation(cls, variable):
		"""
		Permute the nibble.
		"""
		temp = [["" for i in range(0,4)] for j in range(0,8)]
		for i in range(0,8):
			temp[i] = variable[cls.Player[i]]
		return temp

	@staticmethod	
	def NibbleRotation(variable):
		"""
		Rotate the nibble.
		"""
		temp = [["" for i in range(0,4)] for j in range(0,8)]
		for i in range(0,8):
			temp[i] = variable[(i + 2) % 8]
		return temp

	def Constraint(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		#fileobj.close()
		variableinx = Lblock.CreateVariables(0, "x")
		variableiny = Lblock.CreateVariables(0, "y")
		variableu = Lblock.CreateVariables(0, "u")
		variablev = Lblock.CreateVariables(0, "v")
		variableoutx = Lblock.CreateVariables(1, "x")
		variableouty = Lblock.CreateVariables(1, "y")
		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")


		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")
				"""if ((i == 0) and (j == 3)):
					fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")"""
		for i in range(0,8):
			for j in range(0,4):
				if ((i == self.word) and (j == self.bit)):
					fileobj.write("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 1\n")
				else:
					fileobj.write("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")
		#temp = " + ".join(eqn)
		#fileobj.write(temp)
		#fileobj.write("\n")
		fileobj.close()


		if self.Round == 1:
			self.ConstraintsByCopy(variableinx,variableu,variableouty)
			self.ConstraintsBySbox(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXor(variableiny,variablev,variableoutx)
		else:
			self.ConstraintsByCopy(variableinx,variableu,variableouty)
			self.ConstraintsBySbox(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXor(variableiny,variablev,variableoutx)
			for i in range(1,self.Round):
				variableinx = variableoutx
				variableiny = variableouty
				variableouty = Lblock.CreateVariables((i + 1),"y")
				variableoutx = Lblock.CreateVariables((i + 1),"x")
				variableu = Lblock.CreateVariables(i, "u")
				variablev = Lblock.CreateVariables(i, "v")
				self.ConstraintsByCopy(variableinx,variableu,variableouty)
				self.ConstraintsBySbox(variableu,variablev)
				variablev = Lblock.NibblePermutation(variablev)
				variableiny = Lblock.NibbleRotation(variableiny)
				self.ConstraintsByXor(variableiny,variablev,variableoutx)
	def Constraint2(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		#fileobj.write("Subject To\n")
		#fileobj.close()
		variableinx = Lblock.CreateVariables(0, "x")
		variableiny = Lblock.CreateVariables(0, "y")
		variableu = Lblock.CreateVariables(0, "u")
		variablev = Lblock.CreateVariables(0, "v")
		variableoutx = Lblock.CreateVariables(1, "x")
		variableouty = Lblock.CreateVariables(1, "y")

		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")

		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")
				"""if ((i == 0) and (j == 3)):
					fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")"""
		for i in range(0,8):
			for j in range(0,4):
				if ((i == self.word) and (j == self.bit)):
					fileobj.write("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 1\n")
				else:
					fileobj.write("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")
		#temp = " + ".join(eqn)
		#fileobj.write(temp)
		#fileobj.write("\n")
		fileobj.close()


		if self.Round == 1:
			self.ConstraintsByCopy(variableinx,variableu,variableouty)
			self.ConstraintsBySbox(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXor(variableiny,variablev,variableoutx)
		else:
			self.ConstraintsByCopy(variableinx,variableu,variableouty)
			self.ConstraintsBySbox(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXor(variableiny,variablev,variableoutx)
			for i in range(1,self.Round):
				variableinx = variableoutx
				variableiny = variableouty
				variableouty = Lblock.CreateVariables((i + 1),"y")
				variableoutx = Lblock.CreateVariables((i + 1),"x")
				variableu = Lblock.CreateVariables(i, "u")
				variablev = Lblock.CreateVariables(i, "v")
				self.ConstraintsByCopy(variableinx,variableu,variableouty)
				self.ConstraintsBySbox(variableu,variablev)
				variablev = Lblock.NibblePermutation(variablev)
				variableiny = Lblock.NibbleRotation(variableiny)
				self.ConstraintsByXor(variableiny,variablev,variableoutx)

	def Constraint3(self):

		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_modelv3, "w")

		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")

		fileobj.write("Subject To\n")
		for i in range(0,8):
			for j in range(0,4):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")
				"""if ((i == 0) and (j == 3)):
					fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")"""
		for i in range(0,8):
			for j in range(0,4):
				if ((i == self.word) and (j == self.bit)):
					fileobj.write("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 1\n")
				else:
					fileobj.write("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i) + " = 0\n")
		#fileobj.close()
		variableinx = Lblock.CreateVariables(0, "x")
		variableiny = Lblock.CreateVariables(0, "y")
		variableu = Lblock.CreateVariables(0, "u")
		variablev = Lblock.CreateVariables(0, "v")
		variableoutx = Lblock.CreateVariables(1, "x")
		variableouty = Lblock.CreateVariables(1, "y")
		eqn = []

		fileobj.close()
		if self.Round == 1:
			self.ConstraintsByCopyv3(variableinx,variableu,variableouty)
			self.ConstraintsBySboxv3(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXorv3(variableiny,variablev,variableoutx)
		else:
			self.ConstraintsByCopyv3(variableinx,variableu,variableouty)
			self.ConstraintsBySboxv3(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXorv3(variableiny,variablev,variableoutx)
			for i in range(1,self.Round):
				variableinx = variableoutx
				variableiny = variableouty
				variableouty = Lblock.CreateVariables((i + 1),"y")
				variableoutx = Lblock.CreateVariables((i + 1),"x")
				variableu = Lblock.CreateVariables(i, "u")
				variablev = Lblock.CreateVariables(i, "v")
				self.ConstraintsByCopyv3(variableinx,variableu,variableouty)
				self.ConstraintsBySboxv3(variableu,variablev)
				variablev = Lblock.NibblePermutation(variablev)
				variableiny = Lblock.NibbleRotation(variableiny)
				self.ConstraintsByXorv3(variableiny,variablev,variableoutx)

	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("y_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("u_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("v_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def VariableBinaryv3(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("y_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("u_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("v_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()		


	def MakeModel(self):
		"""
		Generate the MILP model of LBock given the round number.
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
			#m.params.TimeLimit=3600
			m.optimize()
			counter = counter+1
			obj = m.getObjective()
			print("**********************************************\n")
			print(m.Status)
			print("\n**********************************************\n")
			#if ((obj.getValue() > 1)&(obj.getValue() <self.blocksize)):
			if((m.Status == 2) or (m.Status == 9) or (m.Status == 11)):
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
							#else:
								#print(u.getAttr('VarName'))
						temp = " + ".join(eqn)
						fileobj = open(self.filename_constraint, "a")
						fileobj.write(temp)
						print("////////////////////////////////////////////////////////////////////////////////")
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
						for i in range(0,8):
							for j in range(0,4):
								eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
						for i in range(0,8):
							for j in range(0,4):
								eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
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
							fileobj.write(str(eqncnst))
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
					for i in range(0,8):
						for j in range(0,4):
							eqn.append("x" + "_0_" + str(3 - j) + "_" + str(i))
					for i in range(0,8):
						for j in range(0,4):
							eqn.append("y" + "_0_" + str(3 - j) + "_" + str(i))
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
						fileobj.write(str(eqncnst))
						fileobj.close()
					else:
						fileobj = open(self.filename_result, "a")	
						fileobj.write("\nv3_m.status:\n")
						fileobj.write(str(m.Status))
						fileobj.close()
		time_end = time.time()		
		fileobj = open(self.filename_result, "a")	
		fileobj.write("\nspent time in sec:\n")
		fileobj.write(str(time_end-time_start))	
		fileobj.close()		

