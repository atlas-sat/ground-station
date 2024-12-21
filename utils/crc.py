import crc32c

# open output.wav
with open("output.wav", 'rb') as f:
    # read the entire file
    byte_string = f.read()

# calculate the CRC32C checksum of the byte string
crc = crc32c.crc32c(byte_string)
print(f"CRC32C: {crc}")

# open data.wav
with open("data.wav", 'rb') as f:
    # read the entire file
    byte_string = f.read()

# calculate the CRC32C checksum of the byte string
crc = crc32c.crc32c(byte_string)
print(f"CRC32C: {crc}")