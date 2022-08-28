from present import Present

if __name__ == "__main__":

	ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

	ACTIVEBITS = 0	#not important
	"""int(raw_input("Input the number of acitvebits: "))
	while not (ACTIVEBITS < 64 and ACTIVEBITS > 0):
		print "Input a number of activebits with range (0, 64):"
		ACTIVEBITS = int(raw_input("Input the number of acitvebits again: "))"""

	#present = Present(ROUND, ACTIVEBITS)

        for i in range(0,16):
                for j in range(0,4):
                	present = Present(ROUND, ACTIVEBITS, i, j)

                	present.MakeModel()

                	present.SolveModel()

	#present.SolveModel()
