import lex
import yacc

"""
# lex
"""

tokens = (
    "CHAR",
    "STAR",
    "PLUS",
    "LPAREN",
    "RPAREN",
    "EMPTY"
)

t_CHAR = r"[0-9a-z]"
t_STAR = r"\*"
t_PLUS = r"\+"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_EMPTY = r"\(\)"
t_ignore = " \t"


def t_error(t):
    print("Wrong input '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()

"""
# yacc
"""
precedence = (
    ('left', 'PLUS'),
    ('left', 'STAR')
)


def p_expression(p):
    '''expression : expression PLUS expression'''
    p[0] = ['+', [p[1], p[3]]]


def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]


def p_term(p):
    '''term : term factor'''
    p[0] = ['CONCATENATION', [p[1], p[2]]]


def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]


def p_factor_paren(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_factor_star(p):
    '''factor : factor STAR'''
    p[0] = ['*', [p[1]]]


def p_factor_empty(p):
    '''factor : EMPTY'''
    p[0] = ['CHAR', 'E']


def p_factor(p):
    '''factor : CHAR'''
    p[0] = ['CHAR', p[1]]


def p_error(p):
    print("Syntax error in input! : '%s'" % p.value)

f = open("re.txt","r")
l = f.readline().strip()

yacc.yacc()
result = yacc.parse(l)

f.close()
print(result)
"""
# make finite automata
"""


class FA(object):
    def __init__(self):
        self.stf = {}
        self.states = set()                                         # To make list with only one element per each state,
        self.inputSymbol = set()                                    # all of them are set
        self.initial = set()
        self.final = set()

    def state(self, s):
        self.states = s

    def input_symbol(self, i):
        self.inputSymbol = i

    def makestf(self, input_stf):                                   # input_stf = "state, input symbol, next_states state"
        if input_stf[0] in self.stf:
            if input_stf[1] in self.stf[input_stf[0]]:
                self.stf[input_stf[0]][input_stf[1]].add(input_stf[2])
            else:
                temp = set()
                temp.add(input_stf[2])
                self.stf[input_stf[0]][input_stf[1]] = temp
        else:
            temp = set()
            temp.add(input_stf[2])
            self.stf[input_stf[0]] = {input_stf[1]: temp}

    def set_initial(self, init):
        self.initial = init

    def set_final(self, f):
        self.final = f


class ExpressionUnit(object):
    def __init__(self):
        self.init = ""
        self.final = ""


def re2enfa(n, tree):
    if tree[0] == 'CHAR':
        if tree[1] != 'E':
            n.inputSymbol.add(tree[1])
        r = ExpressionUnit()
        q = "q" + str(len(n.states))
        r.init = q
        n.states.add(q)
        p = "q" + str(len(n.states))
        r.final = p
        n.states.add(p)

        if r.init not in n.stf:
            n.stf[r.init] = {tree[1]: {r.final}}
        else:
            n.stf[r.init][tree[1]] = {r.final}
        return [r, n]
    elif tree[0] == '*':
        subtree_result = re2enfa(n, tree[1][0])
        exp = subtree_result[0]
        new_n = subtree_result[1]
        r = ExpressionUnit()
        q = "q" + str(len(new_n.states))
        r.init = q
        new_n.states.add(q)
        p = "q" + str(len(new_n.states))
        r.final = p
        new_n.states.add(p)

        if r.init not in new_n.stf:
            new_n.stf[r.init] = {'E': {exp.init}}
        else:
            if 'E' not in new_n.stf[r.init]:
                new_n.stf[r.init]['E'] = {exp.init}
            else:
                new_n.stf[r.init]['E'].add(exp.init)

        new_n.stf[r.init]['E'].add(r.final)

        if exp.final not in new_n.stf:
            n.stf[exp.final] = {'E': {exp.init}}
        else:
            if 'E' not in new_n.stf[exp.final]:
                new_n.stf[exp.final]['E'] = {exp.init}
            else:
                new_n.stf[exp.final]['E'].add(exp.init)
        new_n.stf[exp.final]['E'].add(r.final)
        return [r,new_n]
    elif tree[0] == '+':
        left_result = re2enfa(n, tree[1][0])
        exp1 = left_result[0]
        new_n = left_result[1]
        right_result = re2enfa(new_n, tree[1][1])
        exp2 = right_result[0]
        newnew_n = right_result[1]
        r = ExpressionUnit()
        q = "q" + str(len(newnew_n.states))
        r.init = q
        newnew_n.states.add(q)
        p = "q" + str(len(newnew_n.states))
        r.final = p
        newnew_n.states.add(p)

        if r.init not in newnew_n.stf:
            newnew_n.stf[r.init] = {'E': {exp1.init}}
        else:
            if 'E' not in newnew_n.stf[r.init]:
                newnew_n.stf[r.init]['E'] = {exp1.init}
            else:
                newnew_n.stf[r.init]['E'].add(exp1.init)

        newnew_n.stf[r.init]['E'].add(exp2.init)

        if exp1.final not in newnew_n.stf:
            newnew_n.stf[exp1.final] = {'E': {r.final}}
        else:
            if 'E' not in newnew_n.stf[exp1.final]:
                newnew_n.stf[exp1.final]['E'] = {r.final}
            else:
                newnew_n.stf[exp1.final]['E'].add(r.final)

        if exp2.final not in newnew_n.stf:
            newnew_n.stf[exp2.final] = {'E': {r.final}}
        else:
            if 'E' not in newnew_n.stf[exp2.final]:
                newnew_n.stf[exp2.final]['E'] = {r.final}
            else:
                newnew_n.stf[exp2.final]['E'].add(r.final)
        return [r,newnew_n]
    else:
        left_result = re2enfa(n, tree[1][0])
        exp1 = left_result[0]
        new_n = left_result[1]
        right_result = re2enfa(new_n, tree[1][1])
        exp2 = right_result[0]
        newnew_n = right_result[1]
        r = ExpressionUnit()
        r.init = exp1.init
        r.final = exp2.final

        if exp1.final not in newnew_n.stf:
            newnew_n.stf[exp1.final] = {'E': {exp2.init}}
        else:
            if 'E' not in newnew_n.stf[exp1.final]:
                newnew_n.stf[exp1.final]['E'] = {exp2.init}
            else:
                newnew_n.stf[exp1.final]['E'].add(exp2.init)
        return [r,newnew_n]


def nfa2dfa(n, c):
    dfa = FA()
    nfa = n
    closure = c                                                             # c is from function 'epsilon_closure'
    dfa.input_symbol(nfa.inputSymbol)
    dfa.set_initial(states2string(closure[nfa.initial]))                    # epsilon closure of initial state of nfa
    dfa.states.add(states2string(closure[nfa.initial]))                     # => initial state of dfa

    temp = {dfa.initial}                                                    # temp : new states whose next states are not known yet
    while len(temp) != 0:                                                   # this condition means that there are new states to check
        next_states = set()                                                 # next_states : a set in which possibly new states are included
        for state in temp:
            state_set = string2states(state)
            for inputsymbol in dfa.inputSymbol:
                next_for_s = set()                                          # next_for_s : a set in which next states following current for one of input symbols are included
                next_for_s_add = set()                                      # next_for_s_add : because next_for_s will be used in for-loop, when some elements should be added in
                for states in state_set:                                    #                  next_for_s this set will be used instead to avoid situation where next_for_s is
                    if states in nfa.stf and inputsymbol in nfa.stf[states]:                 # changed during for-loop
                        for next_state in nfa.stf[states][inputsymbol]:
                            next_for_s.add(next_state)
                for elem in next_for_s:
                    if elem in closure:
                        for close in closure[elem]:
                            next_for_s_add.add(close)
                for addElem in next_for_s_add:
                    next_for_s.add(addElem)
                if len(next_for_s) == 0:                                    # this means there is no state next to current state for current input symbol
                    continue
                next_states.add(states2string(next_for_s))
                if state in dfa.stf:
                    dfa.stf[state][inputsymbol] = next_for_s
                else:
                    dfa.stf[state] = {inputsymbol: next_for_s}
        temp = set()
        for nextstate in next_states:
            if not (nextstate in dfa.states):
                dfa.states.add(nextstate)
                temp.add(nextstate)                                         # only new states among 'possibly' new states are added in temp
    for all_state in dfa.states:
        for all_final_state in nfa.final:
            if all_final_state in all_state:
                dfa.final.add(all_state)                                    # every states which have some final states of nfa will be final states of dfa
    return dfa


dis = []                # list of pairs of distinguishable states
indis = []              # list of pairs of indistinguishable states
all_set = []            # list of pairs which are not in dis nor indis yet


def dfa2mdfa(d):
    dfa = d
    mdfa = FA()
    if len(dfa.stf) > 0:
        to_be_removed = list()                                             # used when some elements from list should be removed during for-loop and the for-loop use the list
        for i in range(len(dfa.states) - 1):
            for j in range(i + 1, len(dfa.states)):
                all_set.append([list(dfa.states)[i], list(dfa.states)[j]])     # At first, all possible pairs are included in all_set

        for pair in all_set:
            if (list(pair)[0] in dfa.final and not (list(pair)[1] in dfa.final)) or (
                    list(pair)[1] in dfa.final and not (list(pair)[0] in dfa.final)):
                dis.append(pair)                                                        # all of final-non final pairs go to dis
        for pair in dis:
            all_set.remove(pair)

        cnt = 0
        while len(all_set) != 0:                                                        # this condition means some pairs are not in dis and indis yet
            for pair in all_set:

                ambiguous_pair = list()                                                 # ambiguous_pair : pairs of next states of current two states in 'pair' for same input string
                ambiguous_pair.append(pair)
                for i in range(cnt):                                                    # we want to determine if two states are distinguishable or not
                    temp = list()                                                       # to do this, compare next states of two current states for input string (length == cnt + 1)
                    for s in dfa.inputSymbol:                                           # all of these steps are repeated in while-loop until all pairs are in dis or indis
                        for p in ambiguous_pair:                                        # (table-filling method)
                            if s in dfa.stf[p[0]] and s in dfa.stf[p[1]]:
                                temp.append([dfa.stf[p[0]][s], [dfa.stf[p[1]][s]]])
                    ambiguous_pair = list()
                    for next_pair in temp:
                        if not(next_pair in ambiguous_pair):
                            ambiguous_pair.append(next_pair)

                checker = 0
                for all_pair in ambiguous_pair:
                    check = check_dis(dfa, all_pair)
                    if check == -1:                                                     # this means two states in 'pair' are distinguishable
                        dis.append(pair)                                                # (To see why , check the function 'check_dis'!)
                        to_be_removed.append(pair)
                        break
                    checker += check
                if checker == len(ambiguous_pair):                                      # this means all next states of two states in 'pair' are indistinguishable or same,
                    indis.append(pair)                                                  # thus two states are indistinguishable
                    to_be_removed.append(pair)

            for all_remove in to_be_removed:
                if all_remove in all_set:
                    all_set.remove(all_remove)
                    cnt -= 1                                                            # if some pairs are added in dis or indis, check ambiguous pairs again with the input strings
            cnt += 1                                                                    # of which length is the same with previous step
        mdfa_states = {}
        cnt = 0
        for pair in indis:
            if (pair[0] not in mdfa_states) and (pair[1] not in mdfa_states):
                mdfa_states[pair[0]] = 'q' + str(cnt)                                       # make the name of states more clear
                mdfa_states[pair[1]] = 'q' + str(cnt)                                       # indistinguishable states become same state
                mdfa.states.add('q' + str(cnt))                                             # and distinguishable states have different name with each other
                cnt += 1
            else:
                if (pair[0] in mdfa_states) and (pair[1] not in mdfa_states):
                    mdfa_states[pair[1]] = mdfa_states[pair[0]]
                elif (pair[1] in mdfa_states) and (pair[0] not in mdfa_states):
                    mdfa_states[pair[0]] = mdfa_states[pair[1]]
        for pair in dis:
            if not(pair[0] in mdfa_states):
                mdfa_states[pair[0]] = 'q' + str(cnt)
                mdfa.states.add('q' + str(cnt))
                cnt += 1
            if not(pair[1] in mdfa_states):
                mdfa_states[pair[1]] = 'q' + str(cnt)
                mdfa.states.add('q' + str(cnt))
                cnt += 1
        mdfa_final = set()
        for state in dfa.final:
            mdfa_final.add(mdfa_states[state])

        mdfa.set_final(mdfa_final)
        mdfa.input_symbol(dfa.inputSymbol)
        mdfa.set_initial(mdfa_states[dfa.initial])

        used = []
        for state in mdfa_states:
            if mdfa_states[state] in used:
                continue
            elif state in dfa.stf:
                for symbol in dfa.stf[state]:
                    if not(mdfa_states[state] in mdfa.stf):
                        mdfa.stf[mdfa_states[state]] = {symbol : mdfa_states[states2string(dfa.stf[state][symbol])]}
                    else:
                        mdfa.stf[mdfa_states[state]][symbol] = mdfa_states[states2string(dfa.stf[state][symbol])]
    else:
        mdfa.initial = "q0"                 # If DFA has only one state, there is no pair of two states,
        mdfa.final = {"q0"}                 # thus m-DFA has also only one state, which is both initial state and
        mdfa.states = {"q0"}                # final state, and no state transition function.
    print("--------------------------------result-------------------------------------")j
    print("State Transition Function")
    print(mdfa.stf)
    print("Initial State")
    print(mdfa.initial)
    print("Final States")
    print(mdfa.final)
    print("--------------------------------finish!------------------------------------")
    return mdfa


def check_dis(d, p):        # function that determines if given two states in pair are distinguishable or not (return 1 / return -1)
    dfa = d                 # however, distinguishability may not be determined in some cases (return 0)
    pair = p
    check = 0
    for s in dfa.inputSymbol:
        if (pair[0] in dfa.stf) and (s in dfa.stf[pair[0]]):
            if (pair[1] in dfa.stf) and (s in dfa.stf[pair[1]]):
                if dfa.stf[pair[0]][s] == dfa.stf[pair[1]][s]:
                    check += 1
                elif [states2string(dfa.stf[pair[0]][s]), states2string(dfa.stf[pair[1]][s])] in dis or [states2string(dfa.stf[pair[1]][s]), states2string(dfa.stf[pair[0]][s])] in dis:
                    return -1
                elif [states2string(dfa.stf[pair[0]][s]), states2string(dfa.stf[pair[1]][s])] in indis or [states2string(dfa.stf[pair[1]][s]), states2string(dfa.stf[pair[0]][s])] in indis:
                    check += 1
            else:
                return -1
        else:
            if (pair[1] in dfa.stf) and (s in dfa.stf[pair[1]]):
                return -1
            else:
                check += 1
    if check == len(dfa.inputSymbol):
            return 1
    return 0


def epsilon_one(nfa):
    closure = {}
    for state in nfa.states:
        temp = set()
        if (state in nfa.stf) and ('E' in nfa.stf[state]):
            temp = nfa.stf[state]['E']
        temp.add(state)
        closure[state] = temp
    return closure


def epsilon_closure(closure):
    current = {}
    temp_current = {}
    for s in closure:
        temp1 = set()
        temp2 = set()
        for elem in closure[s]:
            temp1.add(elem)
            temp2.add(elem)
        current[s] = temp1
        temp_current[s] = temp2
    for state in current:
        for e_state in current[state]:
            for ee_state in current[e_state]:
                temp_current[state].add(ee_state)
    if temp_current == closure:
        return current
    else:
        return epsilon_closure(temp_current)


def states2string(state):
    state_str = ""
    state = list(state)
    state.sort()
    for s in state:
        state_str = state_str + s + ","
    state_str = state_str[:-1]
    return state_str


def string2states(string):
    temp = string.split(',')
    return set(temp)


def write_mdfa(m):
    mdfa = m
    m_dfa = open("re2mdfa.txt", "w")

    m_dfa.write("State\n")
    states = states2string(mdfa.states)
    m_dfa.write(states + "\n")

    m_dfa.write("Input symbol\n")
    inputsymbol = states2string(mdfa.inputSymbol)
    m_dfa.write(inputsymbol + "\n")

    m_dfa.write("State transition function\n")
    if len(mdfa.stf) > 0:
        for key in mdfa.stf:
            for keykey in mdfa.stf[key]:
                m_dfa.write(key + "," + keykey + "," + mdfa.stf[key][keykey] + "\n")
    else:
        m_dfa.write("\n")

    m_dfa.write("Initial state\n")
    initial = mdfa.initial
    m_dfa.write(initial + "\n")

    m_dfa.write("Final state\n")
    f = states2string(mdfa.final)
    m_dfa.write(f)


def run():
    e_nfa = FA()
    re = re2enfa(e_nfa, result)
    e_nfa.set_initial(re[0].init)
    e_nfa.set_final({re[0].final})
    temp_closure = epsilon_one(e_nfa)
    e_closure = epsilon_closure(temp_closure)
    converted_dfa = nfa2dfa(e_nfa, e_closure)

    result_mdfa = dfa2mdfa(converted_dfa)
    write_mdfa(result_mdfa)
    # check_valid(result_mdfa)


"""
# function output and function check_valid are for checking if generated m-dfa works correctly
# Therefore those are not related to main performance of this program
"""


def output(s, dic, initial_state, final_state):
    if s == "\n":
        return "아니요\n"
    else:
        s = s.strip()
        state = initial_state
        for i in range(0, len(s)):
            if (state in dic) and (s[i] in dic[state]):
                state = dic[state][s[i]]
            else:
                return "아니요\n"
        if state in final_state:
            return "네\n"
        else:
            return "아니요\n"


def check_valid(mdfa):
    check_input = open("input_2.txt", "r")
    check_result = open("output_2.txt", "w")

    lines = check_input.readlines()

    for line in lines:
        check_result.write(output(line, mdfa.stf, mdfa.initial, mdfa.final))

    check_input.close()
    check_result.close()


run()