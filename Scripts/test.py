def test():
    for x in range(2):
        print(x)
        match x:
            case 1:
                return False
            case 2:
                return False
    return True

print(test())