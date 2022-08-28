from simon import Simon

if __name__ == "__main__":

	WORD_LENGTH = int(raw_input("Input the word length of the target cipher (16 for SIMON32): "))
	while WORD_LENGTH not in [16, 24, 32, 48, 64]:
		print "Invalid word length!"
		WORD_LENGTH = int(raw_input("Input the word length again: "))

	ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

	ACTIVEBITS = 0	#not important
	"""ACTIVEBITS = int(raw_input("Input the number of acitvebits: "))
	while not (ACTIVEBITS < 64 and ACTIVEBITS > 0):
		print "Input a number of activebits with range (0, 64):"
		ACTIVEBITS = int(raw_input("Input the number of acitvebits again: "))"""

        for i in range(1,2):
                for j in range(32,WORD_LENGTH):

			simon = Simon(ROUND, ACTIVEBITS, WORD_LENGTH,i,j)

			simon.MakeModel()

			simon.SolveModel()

