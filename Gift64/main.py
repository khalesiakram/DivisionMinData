from gift import Gift

if __name__ == "__main__":

	"""ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

	OutputBit = int(raw_input("Input the OutputBit: "))
	while not (OutputBit < 64 and OutputBit >= 0):
		print "Input a number of OutputBit with range (0, 64):"
		ACTIVEBITS = int(raw_input("Input the number of OutputBit again: "))"""
		
	for i in range(0,64):

		gift = Gift(9, i)

		gift.MakeModel()

		gift.SolveModel()
		
