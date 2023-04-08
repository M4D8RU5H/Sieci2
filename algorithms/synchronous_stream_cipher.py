import os

from .lfsr import LFSR


class SynchronousStreamCipher:
    @staticmethod
    def encrypt(file_path: str, lfsr: LFSR):
        with open(file_path, 'rb') as file:
            dir_path, file_name = os.path.split(file_path)
            encrypted_file_path = dir_path + os.path.sep + "encrypted_" + file_name

            with open(encrypted_file_path, 'wb') as encrypted_file:
                for line in file:
                    encrypted_line = bytearray()

                    for byte in line:
                        encrypted_byte = 0
                        for i in range(8):
                            encrypted_byte = encrypted_byte << 1
                            encrypted_byte |= (byte >> (7 - i)) & 1
                            encrypted_byte ^= lfsr.step()

                        encrypted_line.append(encrypted_byte)

                    encrypted_file.write(encrypted_line)