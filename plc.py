import snap7
from snap7.util import *
from snap7.types import *

# Reading Tags's Values in PLC
def ReadDataBlock(plc, data_block_number, byte, bit, size, data_type):
    """
    plc
    data-block(int): number of Data Block; DB1, DB2, ...
    byte(int): in case of 2.0, byte is 2.
    bit(int): in case of 2.0,bit is 0.
    size(int): The size of the db data to read  
    data_type(variable): S7WLBit, S7WLWord, S7WLReal, S7WLDDword 

    """
    result = plc.db_read(data_block_number, byte, size)
    if data_type == S7WLBit:
        return get_bool(result, 0, bit)
    elif data_type == S7WLByte or data_type == S7WLWord:
        return get_int(result, 0)
    elif data_type == S7WLReal:
        return get_real(result, 0)  
    elif data_type == S7WLDWord:
        return get_word(result, 0)
    else:
        return None  
    
    
client = snap7.client.Client()
client.connect("192.168.1.1", 0, 1) 
    


mouth_door_tag = ReadDataBlock(client, 63, 0, 2, 1, S7WLBit)
extrusion_tag = ReadDataBlock(client, 63, 0, 3, 1, S7WLBit)           
heartbeat_tag = ReadDataBlock(client, 63, 0, 4, 1, S7WLBit)


print(mouth_door_tag)