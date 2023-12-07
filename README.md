# Digital Finite Impulse Response (DFE) and One-Dimensional Filter

## Overview

This Python script demonstrates the implementation of a Digital Finite Impulse Response (DFE) and an optional One-Dimensional (1-D) filter for signal processing and demodulation. The DFE is designed for demodulating signals, performing symbol estimation, and calculating the Bit Error Rate (BER) against known transmitted bits. The code includes functionalities for:

- DFE implementation
- Optional 1-D filter integration
- OOK (On-Off Keying) demodulation
- BER calculation

## Prerequisites

- Python 3.x
- Libraries: None additional to standard libraries

## Usage

1. Set the algorithm parameters:
   - `dfe_weights_N`: Number of taps for the DFE.
   - `one_d_ena`: Set to 1 if using the 1-D filter, 0 otherwise.

2. Instantiate the DFE and, optionally, the 1-D filter:

    ```python
    dfe = DFE(dfe_weights_N)
    one_d = one_d_filter()  # Only if `one_d_ena` is set to 1
    ```

3. Define or replace the `voltage_stream` list with actual voltage values representing the bit stream.

4. Process the voltage stream through the DFE:

    ```python
    y = []  # To store DFE output
    for voltage in voltage_stream:
        # Optionally process through the 1-D filter
        if one_d_ena:
            voltage = one_d.update(voltage)
        
        # Run the DFE
        a_k, x_out = dfe.run(voltage)
        
        # Collect the DFE output
        y.append(x_out)
    ```

5. Visualize or process the DFE output. For example:

    ```python
    print("Output values:", y)
    ```

6. Perform OOK demodulation with a specified threshold:

    ```python
    threshold = 1.0  # Adjust this threshold according to your signal characteristics
    demodulated_data = ['1' if value > threshold else '0' for value in y]
    print("OOK Demodulated data:", demodulated_data)
    ```

7. Calculate BER by comparing the demodulated data with assumed transmitted bits:

    ```python
    digital_bits = [1 if value > 1 else 0 for value in y]  # Convert output values to bits based on the 1V threshold

    transmitted_bits = [1, 0, 1, 0, 1, 0, 0, 1]  # Example assumed transmitted bits

    total_bits = len(transmitted_bits)
    error_bits = sum(1 for tb, rb in zip(transmitted_bits, digital_bits) if tb != rb)
    ber = error_bits / total_bits

    print("Simulated Bit Error Rate (BER):", ber)
    ```

Adjust and modify the code as needed to suit your specific signal processing and demodulation requirements.

## Disclaimer

This code is provided as an illustrative example and may require adjustments or additional components to function in specific scenarios. Use it at your own discretion and responsibility.
