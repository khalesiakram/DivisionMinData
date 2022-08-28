from lblock import Lblock

if __name__ == "__main__":

	ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

        for i in range(3,8):
                for j in range(0,4):
                	lblock = Lblock(ROUND, i,j)

                	lblock.MakeModel()

                	lblock.SolveModel()
