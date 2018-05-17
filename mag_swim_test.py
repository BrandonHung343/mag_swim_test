from __future__ import print_function
import time
from roboclaw import Roboclaw
import math
import numpy as np 
import time
import pandas as pd
import matplotlib.pyplot as plt
from Complete_Control import M1AForward, M1ABackward, M2AForward, M2ABackward, M3AForward, M3ABackward, M4AForward, M4ABackward

def main():

	#rc_single = Roboclaw("/dev/cu.usbmodem14121",115200) find the specs somewhere

	rc_single.Open()

	address = 0x80
	motor1 = list();
	motor2 = list();
	exitflag   = 0   ; 

	#IMPORTANT
	#% IF VALUE RETURNED BY FUCKTON IS NEGATIVE MAKE IT POSITIVE 
	#f2      = 1   #frequency in hz
	t       = np.arange(0,1,.01) # likely ned to increase this range
	phi     = 0 #phase shift

	final_data = np.array([])

	#TODO open up magnetometer stuff and initialize
	
	sleep_time = 1
    
    test_hz = [0.25, 0.5, 0.75, 0.85, 0.95, 1.0] # add desired numbers, so far below 1 hz
    test_amp = [10, 15, 20, 25, 30, 35, 40, 45] # add desired numbers, below 50
    for hz in test_hz:
        freq_response = np.array([])
        plt.figure()
    	for a in test_amp:
    	    amp_response = np.array([]) 
    	    cos_test = (a*np.cos(2*np.pi*hz*t + phi))
		    for dpoint in len(cos_test):
			    if cos_test[dpoint] > 0:
					# may not be M1, but that can be changed later
				    rc_single.ForwardM1(address, M1AForward(cos_test[dpoint]))
			    else:
				    rc_single.BackwardM1(address, M1ABackward(cos_test[dpoint]))
				
                #TODO read in the magnetometer value(s) i.e. val = magnet.read()
 				#TODO np.append(amp_response, val)

 			    time.sleep(sleep_time)

 			#draws plot and labels on matplotlib
 			rgb = [np.random.uniform() for i in range(3)]
 			label = "Amp: %2d" % (a)
 			#amp_response = single array
        	plt.plot(t, amp_response, color=rgb, label=label)
        #freq response is a 100 x n matrix, where n is the number of test amplitudes. each column is it's own amplitude
        freq_response = np.column_stack((freq_response, amp_response))
	    title = "Hz: %.2f" % (hz)
	    plt.legend()
	    plt.xlabel("Timestep (seconds)")
	    plt.ylabel("Magnetic response (units)")
        final_data = np.column_stack((final_data, freq_response))
	#final dataframe is a (100 * h) x n matrix, where number of frequencies and n is the number of test amplitudes. adds all the frequency responses together. 
    final_dataframe = pd.Dataframe(final_data)
    final_dataframe.to_csv("response_vs_freq_per_amp_single_coil.csv")
    plt.show()






	    



if __name__ == '__main__':
	main()
