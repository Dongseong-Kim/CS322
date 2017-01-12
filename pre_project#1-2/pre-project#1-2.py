def output(s, dic, out_dic, initial_state):
    if s == "\n":
        return "\n"
    else:
        result = ""
        s = s.strip()
        state = initial_state
        for i in range(0, len(s)):
            if s[i] in dic[state]:
                result = result + out_dic[state][s[i]]
                state = dic[state][s[i]]
            else:
                return "No path exists!!\n"
        return result + "\n"

mealy = open("mealy.txt", "r")
mealy.readline()
states = mealy.readline().strip().split(',')
mealy.readline()              # Input Symbol
input_symbol = mealy.readline().strip().split(',')
mealy.readline()              # State transition function

l = mealy.readline().strip()        # first state transition function
stf_dic = {}
while l != "Output symbol":
    stf = l.split(',')
    if stf[0] in stf_dic:
        stf_dic[stf[0]][stf[1]] = stf[2]    # only DFA, not for NFA
    else:
        stf_dic[stf[0]] = {stf[1]: stf[2]}
    l = mealy.readline().strip()

l = mealy.readline().strip()        # Output symbol
output_symbol = l.split(',')
mealy.readline()

l = mealy.readline().strip()        # first output function
of_dic = {}
while l != "Initial state":
    of = l.split(',')
    if of[0] in of_dic:
        of_dic[of[0]][of[1]] = of[2]
    else:
        of_dic[of[0]] = {of[1]: of[2]}
    l = mealy.readline().strip()

initial = mealy.readline().strip()    # Initial state


input_file = open("input.txt", "r")
output_file = open("output.txt", "w")
lines = input_file.readlines()


for line in lines:
    if line == "end":
        break
    output_file.write(output(line.strip(), stf_dic, of_dic, initial))

input_file.close()
output_file.close()
mealy.close()
