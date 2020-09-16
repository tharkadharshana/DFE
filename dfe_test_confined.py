import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy import sign

class one_d_filter(object):
    def __init__(self):
        self.x_k_td = 0

    def update(self, x_k):
        # FIR filter: 1 - z^(-1)
        result = x_k - self.x_k_td
        self.x_k_td = x_k
        return result

class DFE(object):
    def __init__(self, N_taps):
        self.feedback = np.zeros(N_taps, dtype=np.float32)      # Initial tap values
        self.w_feedback = np.zeros(N_taps, dtype=np.float32)    # Weights vector
        self.lms_step = 1.25 * (2 / N_taps)                     # Adaptation step
        self.ARC_value = 0                                      # Initial value for ARC
	
    def run(self, x_in):
        # Calculate DFE output		
        x_out = x_in - np.sum(self.feedback * self.w_feedback)
        # Slicer - estimate symbol value
        if x_out > 2*self.ARC_value: a_k = 3
        elif x_out >= 0: a_k = 1
        elif x_out >= -2*self.ARC_value: a_k = -1
        else: a_k = -3
        # Update Adaptive Reference Control (ARC)
        error = x_out - self.ARC_value*a_k
        self.ARC_value += self.lms_step*error*a_k
        # Update DFE weights
        self.w_feedback += self.lms_step * self.feedback * sign(error)
        # Shift in a_k
        self.feedback = np.roll(self.feedback, 1)
        self.feedback[0] = a_k 
        return a_k, x_out        

if __name__ == "__main__":
    # Setup algorithm parameters
    dfe_weights_N = 64
    one_d_ena = 0
    # Instantiate dsp blocks
    dfe = DFE(dfe_weights_N)
    one_d = one_d_filter()
    # Process signal
    y = []
    for x_k in np.load('data_for_dfe.npy'):
        if one_d_ena: x_k = one_d.update(x_k)
        (a_k, x_k) = dfe.run(x_k)
        y.append(x_k) 
    # Show results
    fig = plt.figure()
    plt.xlabel('Sample')
    plt.ylabel('A')
    plt.plot(y, 'ko')
    plt.show()