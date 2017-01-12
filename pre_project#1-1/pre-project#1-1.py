def output(s, lst, initial_state, final_state):
    if s == "\n":
        return "아니요\n"
    else:
        s = s.strip()
        state = initial_state
        for i in range(0, len(s)):
            check = 0
            for e in lst:
                if e[0] == state and e[1] == s[i]:
                    state = e[2]
                    check = 1
                    break
            if check == 0:
                return "아니요\n"
        if state in final_state:
            return "네\n"
        else:
            return "아니요\n"


dfa = open("dfa_2.txt", "r")

dfa.readline()              # State
states = dfa.readline().strip().split(',')
dfa.readline()              # Input Symbol
input_symbol = dfa.readline().strip().split(',')
dfa.readline()              # State transition function

l = dfa.readline().strip()        # first state transition function
stf_list = []

while l != "Initial state":
    stf = l.split(',')
    stf_list.append(stf)
    l = dfa.readline().strip()

initial = dfa.readline().strip()    # Initial state
dfa.readline()
final = dfa.readline().strip().split(',')     # Final state


input_file = open("input_2.txt", "r")
output_file = open("output_2.txt", "w")
lines = input_file.readlines()

for line in lines:
    output_file.write(output(line, stf_list, initial, final))

input_file.close()
output_file.close()
dfa.close()
