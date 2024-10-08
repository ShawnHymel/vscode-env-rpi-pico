#!/usr/bin/env python

import argparse
import serial
import time

if __name__ == "__main__":
    # Configure argument parser
    parser = argparse.ArgumentParser(description="Measure round-trip time (RTT) over a serial connection.")

    # Add arguments
    parser.add_argument(
        "-p",  
        "--port", 
        type=str, 
        default="/dev/ttyPico",
        help="Serial port to use for communication (default: /dev/ttyPico)"
    )
    parser.add_argument(
        "-b",
        "--baudrate", 
        type=int, 
        default=9600, 
        help="Baudrate for serial communication (default: 9600)"
    )
    parser.add_argument(
        "-n",
        "--num_tests",
        type=int,
        default=1000,
        help="Number of tests to run (default: 1000)"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output (default: False)"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Open the serial connection
    ser = serial.Serial(args.port, args.baudrate, timeout=1.0)
    
    # Ensure the serial port is open
    if not ser.is_open:
        ser.open()
    
    # Character to send
    char_to_send = 'A'

    # Run the tests
    avg_rtt = 0.0
    for n in range(args.num_tests):
        try:
            # Record the start time
            start_time = time.time()
            
            # Send the character
            ser.write(char_to_send.encode('utf-8'))
            
            # Read the response (assuming it's echoing back the same character)
            response = ser.read(1)  # Read one byte/character
            
            # Record the end time
            end_time = time.time()
            
            # Calculate round-trip time
            rtt = end_time - start_time
            
            # Check if the response is the same as the character sent
            if response == char_to_send.encode('utf-8'):
                if args.verbose:
                    print(f"Test {n+1}: RTT = {rtt:.6f} s")
                avg_rtt += rtt
            else:
                print(f"Error: Sent '{char_to_send}' but received '{response.decode('utf-8', errors='ignore')}'")
                break
        
        except Exception as e:
            print(f"Error: {e}")
            break

    # Calculate the average round-trip time
    avg_rtt /= args.num_tests
    print(f"Average RTT = {avg_rtt:.6f} s")
        
    # Close the serial connection
    ser.close()
