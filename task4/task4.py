import sys


def comparison_of_arguments(arg1, arg2):
    if arg2.find('*') == -1:
        if arg1 == arg2:
            print('OK')
        else:
            print('KO')
    else:
        slc = arg2.split('*')
        for i in slc:
            if i == '':
                pass
            else:
                if arg1.find(i) != -1:
                    print(arg1.find(i))
                    arg1 = arg1[(arg1.find(i) + len(i)):]
                else:
                    print("KO")
                    return None
        print("OK")


def main():
    arg1, arg2 = sys.argv[1], sys.argv[2]
    comparison_of_arguments(arg1, arg2)


if __name__ == '__main__':
    main()
