class one_d_filter(object):
    def __init__(self):
        self.x_k_td = 0 # hold the previous input value.

    def update(self, x_k):
        #x_k = now value
        result = x_k - self.x_k_td
        self.x_k_td = x_k
        return result


def sign(num):
    return (num > 0) - (num < 0)


class DFE(object):
    def __init__(self, N_taps):
        self.feedback = [0.0] * N_taps      # Initial tap values
        self.w_feedback = [0.0] * N_taps    # Weights vector
        self.lms_step = 1.25 * (2 / N_taps) # Adaptation step
        self.ARC_value = 0                  # Initial value for ARC

    def run(self, x_in):
        # Calculate DFE output		
        x_out = x_in - sum(f * w for f, w in zip(self.feedback, self.w_feedback))
        
        # Slicer - estimate symbol value (PAM4)
        if x_out > 2 * self.ARC_value:
            a_k = 3
        elif x_out >= 0:
            a_k = 1
        elif x_out >= -2 * self.ARC_value:
            a_k = -1
        else:
            a_k = -3
        
        # Update Adaptive Reference Control (ARC)
        error = x_out - self.ARC_value * a_k
        self.ARC_value += self.lms_step * error * a_k
        print('self Adaptive Reference Value :', self.ARC_value)
        
        # Update DFE weights
        self.w_feedback = [w + self.lms_step * f * sign(error) for f, w in zip(self.feedback, self.w_feedback)]
        print('weight feedback :', self.w_feedback)
        
        # Shift in a_k
        self.feedback = [a_k] + self.feedback[:-1]
        print("feedback :", self.feedback)
        
        return a_k, x_out

if __name__ == "__main__":
    # Setup algorithm parameters
    dfe_weights_N = 8  # Number of taps for the DFE
    one_d_ena = 0  # Set to 1 if using the 1-D filter, 0 otherwise
    
    # Instantiate DFE and optional 1-D filter
    dfe = DFE(dfe_weights_N)
    one_d = one_d_filter()
    
    # Example voltage values representing the bit stream (replace this with your actual voltage values)
    voltage_stream = [0.1, 0.5, 0.8, 1.3, 0.6, 0.9, 0.1, 0.7]
    
    # Process the voltage stream through the DFE
    y = []  # To store DFE output
    for voltage in voltage_stream:
        # For each voltage value in the stream, directly use it as input
        
        # Optionally process through the 1-D filter
        if one_d_ena:
            voltage = one_d.update(voltage)
        
        # Run the DFE
        a_k, x_out = dfe.run(voltage)
        
        # Collect the DFE output
        y.append(x_out)
    
    # Visualize the DFE output (e.g., plot or print)
    print("Output values:", y)
    


# Define a threshold for OOK demodulation (adjust this threshold as needed)
threshold = 1.0  # Adjust this threshold according to your signal characteristics

# Perform OOK demodulation
demodulated_data = [1 if value > threshold else 0 for value in y]

# Print the demodulated data
print("OOK Demodulated data:", demodulated_data)



threshold = 0.5  # Threshold for generating binary output
# Perform PWM encoding using DFE output values
pwm_binary_output = []
for value in y:
    if value > threshold:
        pwm_binary_output.append(1)  # Above threshold: output '1'
    else:
        pwm_binary_output.append(0)  # Below or equal to threshold: output '0'
        
# Display or process the binary PWM output
print("Binary PWM Output:", pwm_binary_output)



# Convert output values to bits based on the 1V threshold
digital_bits = [1 if value > 1 else 0 for value in y]

# Print the resulting digital bits
print("Digital bits:", digital_bits)

# Assumed transmitted bits (replace this with your actual transmitted bits)
transmitted_bits = [1, 0, 1, 0, 1, 0, 0, 1]  # Example assumed transmitted bits

# Calculate Bit Error Rate (BER)
total_bits = len(transmitted_bits)
error_bits = sum(1 for tb, rb in zip(transmitted_bits, digital_bits) if tb != rb)
ber = error_bits / total_bits

# Print the calculated Bit Error Rate
print("Simulated Bit Error Rate (BER):", ber)

