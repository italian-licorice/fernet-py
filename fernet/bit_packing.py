from six.moves import reduce


__author__ = 'spersinger'

class BitPacking:
    @staticmethod
    def pack_int64_bigendian(value):
        """Pack bytes as big endian 64 bits int (long long). """
        return "".join(reversed([chr(value >> (index*8) & 0xFF) for index in range(8)]))


    @staticmethod
    def unpack_int64_bigendian(bytestr):
        bytes = bytearray(bytestr)
        return reduce(lambda val, (index, byte): val | (byte << (index*8)), enumerate(reversed(bytes)), 0)