import serial
import datetime
import time
start = time.time()
import sys

def hex_to_signed(source):
    """Convert a string hex value to a signed hexidecimal value.

    This assumes that source is the proper length, and the sign bit
    is the first bit in the first byte of the correct length.

    hex_to_signed("F") should return -1.
    hex_to_signed("0F") should return 15.
    """
    if not isinstance(source, str):
        raise ValueError("string type required")
    if 0 == len(source):
        raise valueError("string is empty")
    sign_bit_mask = 1 << (len(source)*4-1)
    other_bits_mask = sign_bit_mask - 1
    value = int(source, 16)
    return -(value & sign_bit_mask) | (value & other_bits_mask)

def log_data(max_val):
    # used on 3/2 for grid signal measurements
    now = datetime.datetime.now()
    elapsed_time = str(time.time()-start)
    x = sys.argv[1]
    y = sys.argv[2]
    with open(str(x)+'_'+str(y)+'.txt',"a+") as file:
        file.write(elapsed_time+','+str(max_val)+'\n')
        file.close()

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    while True:
        vals = ser.read(10)
        ords = [ord(val) for val in vals]
        threes = [(ind, val) for ind, val in enumerate(ords) if val == 3]
        if len(threes) == 2:
            if threes[1][0] - threes[0][0] == 5:
                four_vals =  ords[threes[0][0]+1:threes[0][0]+5]
                v1 = four_vals[1] * 256 + four_vals[0] if four_vals[1] < 128 \
                    else -( (255 - four_vals[1]) * 256 + (255 - four_vals[0]) + 1 )
                v2 = four_vals[3] * 256 + four_vals[2] if four_vals[3] < 128 \
                    else -( (255 - four_vals[3]) * 256 + (255 - four_vals[2]) + 1 )
                max_val = max(abs(v1), abs(v2))
                print(max_val)
                # log_data(max_val)


if __name__ == "__main__":
    main()