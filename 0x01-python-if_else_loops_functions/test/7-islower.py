def islower(c):
    value = ord(c)
    print(value)
    if value > 96 and value < 123:
        return True
    else:
        return False
    
    
print(islower("z"))