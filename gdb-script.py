import gdb

_BYTE = 1
_DWORD = 4
_QWORD = 8

def getReg(register):
        return gdb.selected_frame().read_register(register)

def getQword(address):
    res = gdb.execute("x/gu {}".format(address), to_string=True)
    return int(res.strip().split("\t")[-1])

def getDword(address):
    res = gdb.execute("x/wu {}".format(address), to_string=True)
    return int(res.strip().split("\t")[-1])

def getByte(address):
    res = gdb.execute("x/bu {}".format(address), to_string=True)
    return int(res.strip().split("\t")[-1])

def Parse2Array(address, _range, _type=_BYTE):
    res = []
    if _type == _DWORD: func = getDword
    elif _type == _QWORD: func = getQword
    elif _type == _BYTE: func = getByte
    else: assert false

    for i in range(_range):
        res.append(func(address+i*_type))
    return res

gdb.execute("file ./a.out")
gdb.execute("start")

addr = 0x5555554009e0
print(getReg("rsp"))
print(hex(getQword("$rsp")))
print(hex(getDword(addr)))
print(Parse2Array(addr, 0x100, _QWORD))
