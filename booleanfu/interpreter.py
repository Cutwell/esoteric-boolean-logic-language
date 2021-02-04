import sys, getopt

class Interpreter_Error(Exception):
    pass

class Algebra_Error(Exception):
    pass

class interpreter:

    def __init__(self, program):

        self.program = program
        self.memory = {'0':'0','1':'1'}    #  dictionary for storing values using hex keys
        self.declared_values = []    #  list for storing declared memory values
        self.scope = 0    #  current depth of scope

    def main(self):

        #  iterate over the program, loading values from memory and executing instructions.

        program_functions = list(self.program)

        declaring_hex = False    #  boolean switch for declaring memory addresses
        fill_address = []        #  contains memory addresses that require updating

        for char in program_functions:

            #  declaring values

            '''
            [...]  .  creates a new memory address, can then be assigned using i.
                      can also be used to redeclare a memory value.
                      takes inputs as hex addresses.
                      memory is global.
            (...)  .  wraps around a new function, currently used only for decoration.
            () is a decorator because any value declared goes into the global scope.
            [] should be used whenever a value you may wish to use later is moved into the scope.
               proper syntax should be to always assign the ouput of a function to an address.
            '''

            if char == '[':
                declaring_hex = True
                hex_address = []

            elif char == ']':
                declaring_hex = False
                del hex_address[0]
                key = "".join(hex_address)
                try:
                    value = self.memory[key]
                    self.declared_values.insert(0, value)
                except:
                    self.memory.update({key:'0'})
                    fill_address.insert(0, key)

            '''
            declaring two unfilled memory addresses consecutively using eg: ([A][B]ii) will
            assign a value to [B] twice.
            This has been fixed by using a list instead of a var to identify memory addresses
            which need to be filled.
            '''

            if declaring_hex == True:
                hex_address.append(char)

            #  functions

            elif char == '^':    #  'and' function
                try:
                    A = self.declared_values[1]
                    B = self.declared_values[0]
                    if A == B and str(A) == '1':    #  requirements for and function to return 1
                        value = '1'
                        self.declared_values.insert(0, value)
                    else:
                        value = '0'
                        self.declared_values.insert(0, value)
                except:
                    sys.exit("Failed to execute '^' (and) function")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: value})
                        del fill_address[0]


            elif char == '¬':    #  'not' function
                try:
                    A = self.declared_values[0]

                    if A == None or str(A) == '0':    #  the only function that allows us to call it without passing an input
                        value = '1'
                        self.declared_values.insert(0, value)
                    else:
                        value = '0'
                        self.declared_values.insert(0, value)
                except:
                    sys.exit("Failed to execute '¬' (not) function")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: value})
                        del fill_address[0]


            elif char == 'v':    #  'or' function

                try:
                    A = self.declared_values[1]
                    B = self.declared_values[0]
                    if str(A) == '1' or str(B) == '1':
                        value = '1'
                        self.declared_values.insert(0, value)
                    else:
                        value = '0'
                        self.declared_values.insert(0, value)
                except:
                    sys.exit("Failed to execute 'v' (or) function")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: value})
                        del fill_address[0]


            elif char == 'x':    #  'exclusive or' function

                try:
                    A = self.declared_values[1]
                    B = self.declared_values[0]
                    if A==B:
                        value = '0'
                        self.declared_values.insert(0, value)
                    elif A=='1' or B=='1':
                        value = '1'
                        self.declared_values.insert(0, value)
                except:
                    sys.exit("Failed to execute 'v' (or) function")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: value})
                        del fill_address[0]


            elif char == 'U':    #  output ascii string
                try:
                    #  we can decode unicode strings using this exact code
                    #  however the interpreter limits itself to 7 bits in order
                    #  to keep it simple.

                    #  Unicode's first 255 values are shared with ASCII, so this
                    #  is effectively an ascii outputter.

                    bin_list = []
                    for x in range(7):
                        try:
                            bin_list.append(self.declared_values[int(7-x)])
                        except:
                            bin_list.append(0)
                    bin_list_reversed = bin_list.reverse()    #  so that its the right way round (most recently declared last in list)

                    bin_str = "".join(bin_list_reversed)
                    ind = hex(int(bin_str, 2))    #  converts the binary to hexadecimal

                    print(bytes.fromhex(ind).decode('utf-8'))    #  returns the unicode character from the hex index
                except:
                    sys.exit("Failed to execute 'U' (output unicode) function")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: bin_list[0]})
                        del fill_address[0]

            elif char == 'o':    #  output binary value
                try:
                    value = self.declared_values[0]
                    print(value)
                except:
                    sys.exit("Failed to execute 'o' (output) function")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: value})
                        del fill_address[0]




            elif char == 'i':    #  assign input to memory location

                value = str(input())

                if value != '1' and value != '0':
                    raise Interpreter_Error("Can only store single binary bits in memory")
                try:
                    self.memory.update({key: value})
                    self.declared_values.append(value)
                except:
                    sys.exit("No memory address designated for storing input")
                finally:
                    if fill_address != []:
                        self.memory.update({fill_address[0]: value})
                        del fill_address[0]



    def __str__(self):
        #  returns the current state of memory and the declared_values stack
        return str(self.memory)+'\n'+str(self.declared_values)

def main(argv):
    inputfile, outputfile = False, False

    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except getopt.GetoptError:
        print("usage: python3 interpreter.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("usage: python3 interpreter.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg

if __name__ == "__main__":

    inputfile, outputfile = get_args(sys.argv)
    program = ""

    if inputfile:
        with open(inputfile) as file:
            program = file.read()

    console = interpreter(program)

    console.main()

    if outputfile:
        with open(outputfile) as file:
            file.write(console)