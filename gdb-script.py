import gdb

_BYTE = 1
_DWORD = 4
_QWORD = 8

def casting(val):
        return int(val.cast(gdb.lookup_type('unsigned long long')))

def setReg(reg, val):
    gdb.execute("set ${}={}".format(reg, val))

def setAddr(addr, val, _type=_QWORD):
    if _type==_QWORD: _type='{long}'
    elif _type==_DWORD: _type='{int}'
    elif _type==_BYTE: _type='{char}'
    gdb.execute("set {}{}={}".format(_type, addr, val))

def getSymbolAddress(sym):
        return casting(gdb.parse_and_eval(sym).address)

def getReg(register):
        return casting(gdb.selected_frame().read_register(register))

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

gdb.execute("file ./interpreter")
gdb.execute("start")

addr = 0x5555554009e0
print(getReg("rsp"))
print(hex(getQword("$rsp")))
print(hex(getDword(addr)))
print(Parse2Array(addr, 0x100, _QWORD))


addr = 0x00555555603000 + 0x800
setAddr(addr, 0xdeadbeefcafebabe, _QWORD)
print(hex(getQword(addr))) # 0xdeadbeefcafebabe

print(hex(getSymbolAddress('strlen'))) # Strlen Address
setReg("rax", 0xdedabeefcafebabe)
print(hex(getReg("rax"))) # 0xdeadbeefcafebabe

