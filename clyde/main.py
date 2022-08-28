from Spook import Spook

if __name__ == "__main__":
	#for i in range(4):#word
	#	for j in range(32):#bit
	#spook = Spook(8, 127, 3, 31)
	spook = Spook(8, 0, 1)
	spook.MakeModel()
	spook.SolveModel()                	

