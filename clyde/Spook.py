from gurobipy import *

import time
import os

class Spook:
	def __init__(self, Round, outWord, outBit):
		self.threads=8
		self.Round = Round
		self.outBit = outBit
		print("outBit")
		print(self.outBit)
		self.outWord = outWord	
		print("outWord")
		print(self.outWord)			
		self.blocksize = 128
		self.objectiveBound = self.blocksize - 1		
		self.filename_model = "Spook" + str(self.Round) + "_word" + str(self.outWord) + "_bit" + str(self.outBit) + ".lp"
		self.filename_modelv2 = "Spook" + str(self.Round) + "_word" + str(self.outWord) + "_bit" + str(self.outBit) + "v2.lp"
		self.filename_modelv3 = "Spook" + str(self.Round) + "_word" + str(self.outWord) + "_bit" + str(self.outBit) + "v3.lp"				
		self.filename_result = "result_" + "_word" + str(self.outWord) + "_bit" + str(self.outBit) + ".txt"
		#self.filename_result = "result.txt"
		self.filename_constraint = "constraint_" + str(self.Round) + "_word" + str(self.outWord) + "_bit" + str(self.outBit) + ".txt"		
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileobj = open(self.filename_modelv2, "w")
		fileobj.close()		
		fileobj = open(self.filename_modelv3, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "a")
		fileobj.close()
		fileboj = open(self.filename_constraint, "a")
		fileobj.close()
		
	S_T=[[1, 1, 1, 1, -1, -1, -1, -1, 0],\
             [-1, -3, -2, -1, 1, 2, 0, 2, 3],\
             [0, -1, -1, -1, 1, 0, 1, -1, 2],\
             [0, 1, 0, 0, -1, -1, -1, 1, 1],\
             [0, 0, 3, 0, -1, -2, -1, -1, 2],\
             [-1, 2, -1, 0, -1, -1, 1, -2, 3],\
             [0, -2, -1, -1, 2, 3, 2, 1, 0],\
             [-1, 0, 0, 0, 0, 0, -1, 1, 1],\
             [1, 1, 1, 2, -2, -2, -2, 0, 1],\
             [0, 1, 1, 2, -2, -1, -1, -2, 2],\
             [1, 2, 0, 0, -1, -1, -1, -1, 1],\
             [-1, 0, 0, 0, 1, 1, 0, 1, 0],\
             [0, 1, 2, 0, -1, -1, -1, -1, 1]]
	NUMBER = 9
             
	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model
		"""
		fileobj = open(self.filename_model, "w")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,4):
			for j in range(0,32):
				eqn.append("x" + "_0_" + str(i) + "_" + str(j))
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
		array = [[" " for j in range(0,32)] for i in range(0,4)]
		for i in range(0,4):
			for j in range(0,32):
				array[i][j] = s + "_" + str(n) + "_" + str(i) + "_" + str(j)
		return array
	@staticmethod
	def CreateVariables32(n,s):
		"""
		Generate the variables used in the model.
		"""
		array = [" " for i in range(0,32)] 
		for i in range(0,32):
			array[i] = s + "_" + str(n) + "_" + str(i)
		return array

	def rotate(self,x,n):
		return x[n:]+x[:n]				

	def ConstraintsBySbox(self, variable1, variable2):
		"""
		Generate the constraints by sbox layer.
		"""
		fileobj = open(self.filename_model,"a")
		variable1=zip(*variable1)
		variable2=zip(*variable2)
		for k in range(0,32):
			for coeff in Spook.S_T:
				temp = []
				for u in range(0,4):
					temp.append(str(coeff[u]) + " " + variable1[k][3-u])
				for v in range(0,4):
					temp.append(str(coeff[v + 4]) + " " + variable2[k][3-v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coeff[Spook.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 
		
	def ConstraintsByCopy2(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,32):
			temp = []
			temp.append(variablex[i])
			temp.append(variableu[i])
			temp.append(variabley[i])
			s = " - ".join(temp)
			s += " = 0"
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()
		
	def ConstraintsByCopy3(self, variablex, variableu, variabley, variablev):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,32):
			temp = []
			temp.append(variablex[i])
			temp.append(variableu[i])
			temp.append(variabley[i])
			temp.append(variablev[i])
			s = " - ".join(temp)
			s += " = 0"
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()		
		
	def ConstraintsByCopyv3(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_modelv3,"a")
		temp = []
		temp.append(variablex)
		temp.append(variableu)
		temp.append(variabley)
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		fileobj.close()		

	def ConstraintsByXor(self, variabley, variablev, variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,32):
			temp = []
			temp.append(variablex[i])
			temp.append(variablev[i])
			temp.append(variabley[i])
			s = " - ".join(temp)
			s += " = 0"
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()      
		
	def ConstraintsByXorv3(self, variable1, variable2, variable3, variable4, variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_modelv3,"a")
		temp = []
		temp.append(variablex)
		temp.append(variable1)
		temp.append(variable2)
		temp.append(variable3)
		temp.append(variable4)			
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		fileobj.close()      		                   
                
	def ConstraintsByAnd(self, variableIn1, variableIn2, variableOut):
		"""
		Generate the constraints by And.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write((variableOut + " - " + variableIn1 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn2 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn1 + " - " + variableIn2 + " <= " + str(0)))
		fileobj.write("\n")
		fileobj.close()	
		
	def ConstraintsByAndv3(self, variableIn1, variableIn2, variableOut):
		"""
		Generate the constraints by And.
		"""
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write((variableOut + " - " + variableIn1 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn2 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn1 + " - " + variableIn2 + " <= " + str(0)))
		fileobj.write("\n")
		fileobj.close()			

	def Constrain(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")

		eqn = []
		for i in range(0,4):
			for j in range(0,32):
				eqn.append("x" + "_0_" + str(i) + "_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
				
		for i in range(0,128):
			if (((i%32) == self.outBit) and ((i/32) == self.outWord)):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(i/32) + "_" + str(i%32) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(i/32) + "_" + str(i%32) + " = 0\n")
		fileobj.close()
		for i in range(0,self.Round):
			variableIn = Spook.CreateVariables(i,"x")
			variableOut = Spook.CreateVariables(i,"y")
			self.ConstraintsBySbox(variableIn,variableOut)
			s00 = Spook.CreateVariables32(i,"s00")
			s10 = Spook.CreateVariables32(i,"s10")
			s20 = Spook.CreateVariables32(i,"s20")
			s30 = Spook.CreateVariables32(i,"s30")
			s40 = Spook.CreateVariables32(i,"s40")
			s50 = Spook.CreateVariables32(i,"s50")
			s60 = Spook.CreateVariables32(i,"s60")
			s70 = Spook.CreateVariables32(i,"s70")
			self.ConstraintsByCopy3(variableOut[0],s00,s10,s20)
			self.ConstraintsByXor(s10,self.rotate(s20,12),s30)
			self.ConstraintsByCopy2(s30,s40,s50)
			self.ConstraintsByXor(s40,self.rotate(s50,3),s60)
			self.ConstraintsByXor(s60,self.rotate(s00,17),s70)	
			t00 = Spook.CreateVariables32(i,"t00")
			t10 = Spook.CreateVariables32(i,"t10")
			t20 = Spook.CreateVariables32(i,"t20")
			t30 = Spook.CreateVariables32(i,"t30")
			t40 = Spook.CreateVariables32(i,"t40")
			t50 = Spook.CreateVariables32(i,"t50")
			t60 = Spook.CreateVariables32(i,"t60")
			t70 = Spook.CreateVariables32(i,"t70")		
			self.ConstraintsByCopy3(variableOut[1],t00,t10,t20)
			self.ConstraintsByXor(t10,self.rotate(t20,12),t30)
			self.ConstraintsByCopy2(t30,t40,t50)
			self.ConstraintsByXor(t40,self.rotate(t50,3),t60)
			self.ConstraintsByXor(t60,self.rotate(t00,17),t70)
			s80 = Spook.CreateVariables32(i,"s80")
			s90 = Spook.CreateVariables32(i,"s90")
			u00 = Spook.CreateVariables32(i,"u00")
			u10 = Spook.CreateVariables32(i,"u10")
			u20 = Spook.CreateVariables32(i,"u20")
			u30 = Spook.CreateVariables32(i,"u30")
			u40 = Spook.CreateVariables32(i,"u40")
			self.ConstraintsByCopy3(s70,s80,u00,u10)
			self.ConstraintsByXor(self.rotate(u00,31),u10,u20)
			self.ConstraintsByCopy2(u20,u30,u40)
			self.ConstraintsByXor(s80,self.rotate(u30,15),s90)
			t80 = Spook.CreateVariables32(i,"t80")
			t90 = Spook.CreateVariables32(i,"t90")
			v00 = Spook.CreateVariables32(i,"v00")
			v10 = Spook.CreateVariables32(i,"v10")
			v20 = Spook.CreateVariables32(i,"v20")
			v30 = Spook.CreateVariables32(i,"v30")
			v40 = Spook.CreateVariables32(i,"v40")
			self.ConstraintsByCopy3(t70,t80,v00,v10)
			self.ConstraintsByXor(self.rotate(v00,31),v10,v20)
			self.ConstraintsByCopy2(v20,v30,v40)
			self.ConstraintsByXor(t80,self.rotate(v30,15),t90)
			
			variableOut = Spook.CreateVariables(i+1,"x")
			self.ConstraintsByXor(s90,self.rotate(v40,26),variableOut[0])			
			self.ConstraintsByXor(t90,self.rotate(u40,25),variableOut[1])
			
			############
			variableOut = Spook.CreateVariables(i,"y")
			s01 = Spook.CreateVariables32(i,"s01")
			s11 = Spook.CreateVariables32(i,"s11")
			s21 = Spook.CreateVariables32(i,"s21")
			s31 = Spook.CreateVariables32(i,"s31")
			s41 = Spook.CreateVariables32(i,"s41")
			s51 = Spook.CreateVariables32(i,"s51")
			s61 = Spook.CreateVariables32(i,"s61")
			s71 = Spook.CreateVariables32(i,"s71")
			self.ConstraintsByCopy3(variableOut[2],s01,s11,s21)
			self.ConstraintsByXor(s11,self.rotate(s21,12),s31)
			self.ConstraintsByCopy2(s31,s41,s51)
			self.ConstraintsByXor(s41,self.rotate(s51,3),s61)
			self.ConstraintsByXor(s61,self.rotate(s01,17),s71)	
			t01 = Spook.CreateVariables32(i,"t01")
			t11 = Spook.CreateVariables32(i,"t11")
			t21 = Spook.CreateVariables32(i,"t21")
			t31 = Spook.CreateVariables32(i,"t31")
			t41 = Spook.CreateVariables32(i,"t41")
			t51 = Spook.CreateVariables32(i,"t51")
			t61 = Spook.CreateVariables32(i,"t61")
			t71 = Spook.CreateVariables32(i,"t71")		
			self.ConstraintsByCopy3(variableOut[3],t01,t11,t21)
			self.ConstraintsByXor(t11,self.rotate(t21,12),t31)
			self.ConstraintsByCopy2(t31,t41,t51)
			self.ConstraintsByXor(t41,self.rotate(t51,3),t61)
			self.ConstraintsByXor(t61,self.rotate(t01,17),t71)
			s81 = Spook.CreateVariables32(i,"s81")
			s91 = Spook.CreateVariables32(i,"s91")
			u01 = Spook.CreateVariables32(i,"u01")
			u11 = Spook.CreateVariables32(i,"u11")
			u21 = Spook.CreateVariables32(i,"u21")
			u31 = Spook.CreateVariables32(i,"u31")
			u41 = Spook.CreateVariables32(i,"u41")
			self.ConstraintsByCopy3(s71,s81,u01,u11)
			self.ConstraintsByXor(self.rotate(u01,31),u11,u21)
			self.ConstraintsByCopy2(u21,u31,u41)
			self.ConstraintsByXor(s81,self.rotate(u31,15),s91)
			t81 = Spook.CreateVariables32(i,"t81")
			t91 = Spook.CreateVariables32(i,"t91")
			v01 = Spook.CreateVariables32(i,"v01")
			v11 = Spook.CreateVariables32(i,"v11")
			v21 = Spook.CreateVariables32(i,"v21")
			v31 = Spook.CreateVariables32(i,"v31")
			v41 = Spook.CreateVariables32(i,"v41")
			self.ConstraintsByCopy3(t71,t81,v01,v11)
			self.ConstraintsByXor(self.rotate(v01,31),v11,v21)
			self.ConstraintsByCopy2(v21,v31,v41)
			self.ConstraintsByXor(t81,self.rotate(v31,15),t91)
			
			variableOut = Spook.CreateVariables(i+1,"x")
			self.ConstraintsByXor(s91,self.rotate(v41,26),variableOut[2])			
			self.ConstraintsByXor(t91,self.rotate(u41,25),variableOut[3])			
									
			"""self.ConstraintsByCopy(variableIn[47],variableOut[46],variableBr[47])
			self.ConstraintsByCopy(variableIn[70],variableOut[69],variableBr[70])
			self.ConstraintsByCopy(variableIn[85],variableOut[84],variableBr[85])
			self.ConstraintsByCopy(variableIn[91],variableOut[90],variableBr[91])
			fileobj = open(self.filename_model, "a")
			for j in range(0,127):
				if ((j != 46)&(j != 69)&(j != 84)&(j != 90)):
					fileobj.write(str(variableOut[j]) + " - " +str(variableIn[j+1]) + " = 0 \n")
			fileobj.close()
			self.ConstraintsByAnd(variableBr[70],variableBr[85],variableIn[128])
			self.ConstraintsByXor(variableIn[0],variableBr[47],variableIn[128],variableBr[91],variableOut[127])"""
	def Constraint2(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		#fileobj.write("Subject To\n")

		eqn = []
		for i in range(0,4):
			for j in range(0,32):
				eqn.append("x" + "_0_" + str(i) + "_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
				
		for i in range(0,128):
			if (((i%32) == self.outBit) and ((i/32) == self.outWord)):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(i/32) + "_" + str(i%32) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(i/32) + "_" + str(i%32) + " = 0\n")
		fileobj.close()
		for i in range(0,self.Round):
			variableIn = Spook.CreateVariables(i,"x")
			variableOut = Spook.CreateVariables(i,"y")
			self.ConstraintsBySbox(variableIn,variableOut)
			s00 = Spook.CreateVariables32(i,"s00")
			s10 = Spook.CreateVariables32(i,"s10")
			s20 = Spook.CreateVariables32(i,"s20")
			s30 = Spook.CreateVariables32(i,"s30")
			s40 = Spook.CreateVariables32(i,"s40")
			s50 = Spook.CreateVariables32(i,"s50")
			s60 = Spook.CreateVariables32(i,"s60")
			s70 = Spook.CreateVariables32(i,"s70")
			self.ConstraintsByCopy3(variableOut[0],s00,s10,s20)
			self.ConstraintsByXor(s10,self.rotate(s20,12),s30)
			self.ConstraintsByCopy2(s30,s40,s50)
			self.ConstraintsByXor(s40,self.rotate(s50,3),s60)
			self.ConstraintsByXor(s60,self.rotate(s00,17),s70)	
			t00 = Spook.CreateVariables32(i,"t00")
			t10 = Spook.CreateVariables32(i,"t10")
			t20 = Spook.CreateVariables32(i,"t20")
			t30 = Spook.CreateVariables32(i,"t30")
			t40 = Spook.CreateVariables32(i,"t40")
			t50 = Spook.CreateVariables32(i,"t50")
			t60 = Spook.CreateVariables32(i,"t60")
			t70 = Spook.CreateVariables32(i,"t70")		
			self.ConstraintsByCopy3(variableOut[1],t00,t10,t20)
			self.ConstraintsByXor(t10,self.rotate(t20,12),t30)
			self.ConstraintsByCopy2(t30,t40,t50)
			self.ConstraintsByXor(t40,self.rotate(t50,3),t60)
			self.ConstraintsByXor(t60,self.rotate(t00,17),t70)
			s80 = Spook.CreateVariables32(i,"s80")
			s90 = Spook.CreateVariables32(i,"s90")
			u00 = Spook.CreateVariables32(i,"u00")
			u10 = Spook.CreateVariables32(i,"u10")
			u20 = Spook.CreateVariables32(i,"u20")
			u30 = Spook.CreateVariables32(i,"u30")
			u40 = Spook.CreateVariables32(i,"u40")
			self.ConstraintsByCopy3(s70,s80,u00,u10)
			self.ConstraintsByXor(self.rotate(u00,31),u10,u20)
			self.ConstraintsByCopy2(u20,u30,u40)
			self.ConstraintsByXor(s80,self.rotate(u30,15),s90)
			t80 = Spook.CreateVariables32(i,"t80")
			t90 = Spook.CreateVariables32(i,"t90")
			v00 = Spook.CreateVariables32(i,"v00")
			v10 = Spook.CreateVariables32(i,"v10")
			v20 = Spook.CreateVariables32(i,"v20")
			v30 = Spook.CreateVariables32(i,"v30")
			v40 = Spook.CreateVariables32(i,"v40")
			self.ConstraintsByCopy3(t70,t80,v00,v10)
			self.ConstraintsByXor(self.rotate(v00,31),v10,v20)
			self.ConstraintsByCopy2(v20,v30,v40)
			self.ConstraintsByXor(t80,self.rotate(v30,15),t90)
			
			variableOut = Spook.CreateVariables(i+1,"x")
			self.ConstraintsByXor(s90,self.rotate(v40,26),variableOut[0])			
			self.ConstraintsByXor(t90,self.rotate(u40,25),variableOut[1])
			
			############
			variableOut = Spook.CreateVariables(i,"y")
			s01 = Spook.CreateVariables32(i,"s01")
			s11 = Spook.CreateVariables32(i,"s11")
			s21 = Spook.CreateVariables32(i,"s21")
			s31 = Spook.CreateVariables32(i,"s31")
			s41 = Spook.CreateVariables32(i,"s41")
			s51 = Spook.CreateVariables32(i,"s51")
			s61 = Spook.CreateVariables32(i,"s61")
			s71 = Spook.CreateVariables32(i,"s71")
			self.ConstraintsByCopy3(variableOut[2],s01,s11,s21)
			self.ConstraintsByXor(s11,self.rotate(s21,12),s31)
			self.ConstraintsByCopy2(s31,s41,s51)
			self.ConstraintsByXor(s41,self.rotate(s51,3),s61)
			self.ConstraintsByXor(s61,self.rotate(s01,17),s71)	
			t01 = Spook.CreateVariables32(i,"t01")
			t11 = Spook.CreateVariables32(i,"t11")
			t21 = Spook.CreateVariables32(i,"t21")
			t31 = Spook.CreateVariables32(i,"t31")
			t41 = Spook.CreateVariables32(i,"t41")
			t51 = Spook.CreateVariables32(i,"t51")
			t61 = Spook.CreateVariables32(i,"t61")
			t71 = Spook.CreateVariables32(i,"t71")		
			self.ConstraintsByCopy3(variableOut[3],t01,t11,t21)
			self.ConstraintsByXor(t11,self.rotate(t21,12),t31)
			self.ConstraintsByCopy2(t31,t41,t51)
			self.ConstraintsByXor(t41,self.rotate(t51,3),t61)
			self.ConstraintsByXor(t61,self.rotate(t01,17),t71)
			s81 = Spook.CreateVariables32(i,"s81")
			s91 = Spook.CreateVariables32(i,"s91")
			u01 = Spook.CreateVariables32(i,"u01")
			u11 = Spook.CreateVariables32(i,"u11")
			u21 = Spook.CreateVariables32(i,"u21")
			u31 = Spook.CreateVariables32(i,"u31")
			u41 = Spook.CreateVariables32(i,"u41")
			self.ConstraintsByCopy3(s71,s81,u01,u11)
			self.ConstraintsByXor(self.rotate(u01,31),u11,u21)
			self.ConstraintsByCopy2(u21,u31,u41)
			self.ConstraintsByXor(s81,self.rotate(u31,15),s91)
			t81 = Spook.CreateVariables32(i,"t81")
			t91 = Spook.CreateVariables32(i,"t91")
			v01 = Spook.CreateVariables32(i,"v01")
			v11 = Spook.CreateVariables32(i,"v11")
			v21 = Spook.CreateVariables32(i,"v21")
			v31 = Spook.CreateVariables32(i,"v31")
			v41 = Spook.CreateVariables32(i,"v41")
			self.ConstraintsByCopy3(t71,t81,v01,v11)
			self.ConstraintsByXor(self.rotate(v01,31),v11,v21)
			self.ConstraintsByCopy2(v21,v31,v41)
			self.ConstraintsByXor(t81,self.rotate(v31,15),t91)
			
			variableOut = Spook.CreateVariables(i+1,"x")
			self.ConstraintsByXor(s91,self.rotate(v41,26),variableOut[2])			
			self.ConstraintsByXor(t91,self.rotate(u41,25),variableOut[3])
			
	def Constraint3(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,4):
			for j in range(0,32):
				eqn.append("x" + "_0_" + str(i) + "_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
				
		fileobj.write("Subject To\n")
			
		for i in range(0,128):
			if (((i%32) == self.outBit) and ((i/32) == self.outWord)):
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(i/32) + "_" + str(i%32) + " = 1\n")
			else:
				fileobj.write("x" + "_" + str(self.Round) + "_" + str(i/32) + "_" + str(i%32) + " = 0\n")
		fileobj.close()
		for i in range(0,self.Round):
			variableIn = Spook.CreateVariables(i,"x")
			variableOut = Spook.CreateVariables(i,"y")
			self.ConstraintsBySbox(variableIn,variableOut)
			s00 = Spook.CreateVariables32(i,"s00")
			s10 = Spook.CreateVariables32(i,"s10")
			s20 = Spook.CreateVariables32(i,"s20")
			s30 = Spook.CreateVariables32(i,"s30")
			s40 = Spook.CreateVariables32(i,"s40")
			s50 = Spook.CreateVariables32(i,"s50")
			s60 = Spook.CreateVariables32(i,"s60")
			s70 = Spook.CreateVariables32(i,"s70")
			self.ConstraintsByCopy3(variableOut[0],s00,s10,s20)
			self.ConstraintsByXor(s10,self.rotate(s20,12),s30)
			self.ConstraintsByCopy2(s30,s40,s50)
			self.ConstraintsByXor(s40,self.rotate(s50,3),s60)
			self.ConstraintsByXor(s60,self.rotate(s00,17),s70)	
			t00 = Spook.CreateVariables32(i,"t00")
			t10 = Spook.CreateVariables32(i,"t10")
			t20 = Spook.CreateVariables32(i,"t20")
			t30 = Spook.CreateVariables32(i,"t30")
			t40 = Spook.CreateVariables32(i,"t40")
			t50 = Spook.CreateVariables32(i,"t50")
			t60 = Spook.CreateVariables32(i,"t60")
			t70 = Spook.CreateVariables32(i,"t70")		
			self.ConstraintsByCopy3(variableOut[1],t00,t10,t20)
			self.ConstraintsByXor(t10,self.rotate(t20,12),t30)
			self.ConstraintsByCopy2(t30,t40,t50)
			self.ConstraintsByXor(t40,self.rotate(t50,3),t60)
			self.ConstraintsByXor(t60,self.rotate(t00,17),t70)
			s80 = Spook.CreateVariables32(i,"s80")
			s90 = Spook.CreateVariables32(i,"s90")
			u00 = Spook.CreateVariables32(i,"u00")
			u10 = Spook.CreateVariables32(i,"u10")
			u20 = Spook.CreateVariables32(i,"u20")
			u30 = Spook.CreateVariables32(i,"u30")
			u40 = Spook.CreateVariables32(i,"u40")
			self.ConstraintsByCopy3(s70,s80,u00,u10)
			self.ConstraintsByXor(self.rotate(u00,31),u10,u20)
			self.ConstraintsByCopy2(u20,u30,u40)
			self.ConstraintsByXor(s80,self.rotate(u30,15),s90)
			t80 = Spook.CreateVariables32(i,"t80")
			t90 = Spook.CreateVariables32(i,"t90")
			v00 = Spook.CreateVariables32(i,"v00")
			v10 = Spook.CreateVariables32(i,"v10")
			v20 = Spook.CreateVariables32(i,"v20")
			v30 = Spook.CreateVariables32(i,"v30")
			v40 = Spook.CreateVariables32(i,"v40")
			self.ConstraintsByCopy3(t70,t80,v00,v10)
			self.ConstraintsByXor(self.rotate(v00,31),v10,v20)
			self.ConstraintsByCopy2(v20,v30,v40)
			self.ConstraintsByXor(t80,self.rotate(v30,15),t90)
			
			variableOut = Spook.CreateVariables(i+1,"x")
			self.ConstraintsByXor(s90,self.rotate(v40,26),variableOut[0])			
			self.ConstraintsByXor(t90,self.rotate(u40,25),variableOut[1])
			
			############
			variableOut = Spook.CreateVariables(i,"y")
			s01 = Spook.CreateVariables32(i,"s01")
			s11 = Spook.CreateVariables32(i,"s11")
			s21 = Spook.CreateVariables32(i,"s21")
			s31 = Spook.CreateVariables32(i,"s31")
			s41 = Spook.CreateVariables32(i,"s41")
			s51 = Spook.CreateVariables32(i,"s51")
			s61 = Spook.CreateVariables32(i,"s61")
			s71 = Spook.CreateVariables32(i,"s71")
			self.ConstraintsByCopy3(variableOut[2],s01,s11,s21)
			self.ConstraintsByXor(s11,self.rotate(s21,12),s31)
			self.ConstraintsByCopy2(s31,s41,s51)
			self.ConstraintsByXor(s41,self.rotate(s51,3),s61)
			self.ConstraintsByXor(s61,self.rotate(s01,17),s71)	
			t01 = Spook.CreateVariables32(i,"t01")
			t11 = Spook.CreateVariables32(i,"t11")
			t21 = Spook.CreateVariables32(i,"t21")
			t31 = Spook.CreateVariables32(i,"t31")
			t41 = Spook.CreateVariables32(i,"t41")
			t51 = Spook.CreateVariables32(i,"t51")
			t61 = Spook.CreateVariables32(i,"t61")
			t71 = Spook.CreateVariables32(i,"t71")		
			self.ConstraintsByCopy3(variableOut[3],t01,t11,t21)
			self.ConstraintsByXor(t11,self.rotate(t21,12),t31)
			self.ConstraintsByCopy2(t31,t41,t51)
			self.ConstraintsByXor(t41,self.rotate(t51,3),t61)
			self.ConstraintsByXor(t61,self.rotate(t01,17),t71)
			s81 = Spook.CreateVariables32(i,"s81")
			s91 = Spook.CreateVariables32(i,"s91")
			u01 = Spook.CreateVariables32(i,"u01")
			u11 = Spook.CreateVariables32(i,"u11")
			u21 = Spook.CreateVariables32(i,"u21")
			u31 = Spook.CreateVariables32(i,"u31")
			u41 = Spook.CreateVariables32(i,"u41")
			self.ConstraintsByCopy3(s71,s81,u01,u11)
			self.ConstraintsByXor(self.rotate(u01,31),u11,u21)
			self.ConstraintsByCopy2(u21,u31,u41)
			self.ConstraintsByXor(s81,self.rotate(u31,15),s91)
			t81 = Spook.CreateVariables32(i,"t81")
			t91 = Spook.CreateVariables32(i,"t91")
			v01 = Spook.CreateVariables32(i,"v01")
			v11 = Spook.CreateVariables32(i,"v11")
			v21 = Spook.CreateVariables32(i,"v21")
			v31 = Spook.CreateVariables32(i,"v31")
			v41 = Spook.CreateVariables32(i,"v41")
			self.ConstraintsByCopy3(t71,t81,v01,v11)
			self.ConstraintsByXor(self.rotate(v01,31),v11,v21)
			self.ConstraintsByCopy2(v21,v31,v41)
			self.ConstraintsByXor(t81,self.rotate(v31,15),t91)
			
			variableOut = Spook.CreateVariables(i+1,"x")
			self.ConstraintsByXor(s91,self.rotate(v41,26),variableOut[2])			
			self.ConstraintsByXor(t91,self.rotate(u41,25),variableOut[3])

	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round)+1):
                        for j in range(0,4):
                        	for k in range(0,32):
                        		fileobj.write("x_" + str(i) + "_" + str(j) + "_" + str(k))
                        		fileobj.write("\n")
		for i in range(0,(self.Round)):
                        for j in range(0,4):
                        	for k in range(0,32):                        		
                        		fileobj.write("y_" + str(i) + "_" + str(j) + "_" + str(k))
                        		fileobj.write("\n")   
		for i in range(0,(self.Round)):
                        for j in range(0,32):
                		fileobj.write("s00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s40_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s50_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s60_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s70_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s80_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s90_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t40_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t50_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t60_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t70_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t80_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t90_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 	
                		fileobj.write("u00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u40_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v40_" + str(i) + "_" + str(j))
                		fileobj.write("\n")  

				fileobj.write("s01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s41_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s51_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s61_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s71_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s81_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s91_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t41_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t51_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t61_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t71_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t81_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t91_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 	
                		fileobj.write("u01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u41_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v41_" + str(i) + "_" + str(j))
                		fileobj.write("\n")                        		               			                		                		                       		                     		
                        		
                        	"""fileobj.write("x_" + str(i) + "_" + str(0))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(47))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(70))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(85))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(91))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(127))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(128))
                        	fileobj.write("\n")"""
		"""for i in range(0,self.Round):
			fileobj.write("br_" + str(i) + "_47")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_70")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_85")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_91")
			fileobj.write("\n")"""
		fileobj.write("END")
		fileobj.close()
	def VariableBinaryv3(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round)+1):
                        for j in range(0,4):
                        	for k in range(0,32):
                        		fileobj.write("x_" + str(i) + "_" + str(j) + "_" + str(k))
                        		fileobj.write("\n")
		for i in range(0,(self.Round)):
                        for j in range(0,4):
                        	for k in range(0,32):                        		
                        		fileobj.write("y_" + str(i) + "_" + str(j) + "_" + str(k))
                        		fileobj.write("\n")   
		for i in range(0,(self.Round)):
                        for j in range(0,32):
                		fileobj.write("s00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s40_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s50_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s60_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s70_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s80_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s90_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t40_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t50_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t60_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t70_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t80_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t90_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 	
                		fileobj.write("u00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u40_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v00_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v10_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v20_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v30_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v40_" + str(i) + "_" + str(j))
                		fileobj.write("\n")  

				fileobj.write("s01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s41_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s51_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s61_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s71_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s81_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("s91_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t41_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t51_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t61_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t71_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t81_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("t91_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 	
                		fileobj.write("u01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("u41_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v01_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v11_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v21_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v31_" + str(i) + "_" + str(j))
                		fileobj.write("\n") 
                		fileobj.write("v41_" + str(i) + "_" + str(j))
                		fileobj.write("\n")                        		               			                		                		                       		                     		
                        		
                        	"""fileobj.write("x_" + str(i) + "_" + str(0))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(47))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(70))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(85))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(91))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(127))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(128))
                        	fileobj.write("\n")"""
		"""for i in range(0,self.Round):
			fileobj.write("br_" + str(i) + "_47")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_70")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_85")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_91")
			fileobj.write("\n")"""
		fileobj.write("END")
		fileobj.close()
	def Init(self,counterInput):
		"""
		Generate the constraints introduced by the initial division property.
		"""
		variableout = Spook.CreateVariables(0,"x")
		fileobj = open(self.filename_model, "a")
		eqn = []
		for i in range(0, counterInput):
			temp = variableout[i] + " = 1"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range(counterInput, counterInput+1):
			temp = variableout[i] + " = 0"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range(counterInput+1, 128):
			temp = variableout[i] + " = 0"  #for ex search, should be one
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	#def MakeModel(self,counterInput,counterOut):
	def MakeModel(self):
		"""
		Generate the MILP model of Spook given the round number and activebits.
		"""
		self.CreateObjectiveFunction()
		self.Constrain()
		#self.Init()
		self.VariableBinary()

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
						for i in range(0,64):
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
					for i in range(0,64):
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
