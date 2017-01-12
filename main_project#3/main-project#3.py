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

t_CHAR = r"[123qweasdzxc]"
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


class Mealy(object):
    def __init__(self):
        self.stf = {}                                               # standard transition function
        self.of = {}                                                # output function
        self.states = set()
        self.inputSymbol = set()
        self.outputSymbol = set()
        self.initial = set()                                        # initial state

    def state(self, s):
        self.states = s

    def input_symbol(self, i):
        self.inputSymbol = i

    def output_symbol(self, o):
        self.outputSymbol = o

    def makestf(self, input_stf):                                   # input_stf = "state, input symbol, next state"
        if input_stf[0] in self.stf:
            self.stf[input_stf[0]][input_stf[1]] = input_stf[2]
        else:
            self.stf[input_stf[0]] = {input_stf[1]: input_stf[2]}

    def makeof(self, input_of):                                     # input_of = "state, input symbol, output"
        if input_of[0] in self.of:
            self.of[input_of[0]][input_of[1]] = input_of[2]
        else:
            self.of[input_of[0]] = {input_of[1]: input_of[2]}

    def set_initial(self, init):
        self.initial = init


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
    """
    print("----------------------------m-DFA : result---------------------------------")
    print("State Transition Function")
    print(mdfa.stf)
    print("Initial State")
    print(mdfa.initial)
    print("Final States")
    print(mdfa.final)
    print("--------------------------------finish!------------------------------------")
    """
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


state_cho = set()               # set which stores states in which the last input was cho-seong
state_jung = set()              # set which stores states in which the last input was jung-seong


def make_mealy(mdfa):           # make mealy machine with the information of mdfa
    mealy = Mealy()
    mealy.output_symbol(['ㄱ', 'ㄴ', 'ㄹ', 'ㅁ', 'ㅇ', 'ㅅ', 'ㅏ', 'ㅗ', 'ㅡ', 'ㅣ', '1', '2'])          # 1 : 획추가, 2 : 쌍자음
    mealy.input_symbol(mdfa.inputSymbol)
    mealy.state(mdfa.states)
    mealy.stf = mdfa.stf
    mealy.set_initial(mdfa.initial)

    for elem in mealy.stf:                          # set output function of mealy machine
        for elemelem in mealy.stf[elem]:
            temp = []
            if elemelem == 'z':
                temp = [elem, elemelem, '1']
            elif elemelem == 'c':
                temp = [elem, elemelem, '2']
            else:
                if elemelem == '1':
                    temp = [elem, elemelem, 'ㄱ']
                elif elemelem == '2':
                    temp = [elem, elemelem, 'ㄴ']
                elif elemelem == 'q':
                    temp = [elem, elemelem, 'ㄹ']
                elif elemelem == 'w':
                    temp = [elem, elemelem, 'ㅁ']
                elif elemelem == 'a':
                    temp = [elem, elemelem, 'ㅅ']
                elif elemelem == 's':
                    temp = [elem, elemelem, 'ㅇ']
                elif elemelem == '3':
                    temp = [elem, elemelem, 'ㅏ']
                elif elemelem == 'e':
                    temp = [elem, elemelem, 'ㅗ']
                elif elemelem == 'd':
                    temp = [elem, elemelem, 'ㅣ']
                elif elemelem == 'x':
                    temp = [elem, elemelem, 'ㅡ']
                else:
                    print("ERROR : make_mealy")

            if len(temp) != 0:
                mealy.makeof(temp)
    for elem in mealy.stf[mealy.initial]:               # store states in which the last input was 'definitely' choseong
        state_cho.add(mealy.stf[mealy.initial][elem])

    for elem in mealy.stf[mealy.stf[mealy.initial]['q']]:               # store states in which the last input was jungseong
        state_jung.add(mealy.stf[mealy.stf[mealy.initial]['q']][elem])
        if (elem == '3') or (elem == 'e'):
            state_jung.add(mealy.stf[mealy.stf[mealy.stf[mealy.initial]['q']][elem]][elem])
    temp_jung = set()
    for elem in state_jung:                                             # check if there are jungseong states missed during above step
        for elemelem in mealy.stf[elem]:                                # if such states exist, store them
            if '3' == elemelem or 'e' == elemelem or 'd' == elemelem or 'x' == elemelem  or 'z' == elemelem :
                temp_jung.add(mealy.stf[elem][elemelem])
    for elem in temp_jung:
        state_jung.add(elem)
    """
    print("------------------------Mealy machine : result-----------------------------")
    print("Output Function")
    print(mealy.of)
    print("Initial State")
    print(mealy.initial)
    print("state_cho")
    print(state_cho)
    print("state_jung")
    print(state_jung)
    print("--------------------------------finish!------------------------------------")
    """
    return mealy


def hangul(s):                  # from main project #1... CAUTION : 본 프로젝트1에서는 잘못된 한글 string도 입력받을 수 있게 처리를 해주었으나
                                # 이 프로그램에서는 그러한 경우는 에러로 간주하기 때문에 이 함수에는 이 프로그램을 구현하는데 쓸모가 없는 코드가 여럿 있을 수 있다.
    cho = {'ㄱ': 0, 'ㄲ': 1, 'ㄴ': 2, 'ㄷ': 3, 'ㄸ': 4, 'ㄹ': 5, 'ㅁ': 6, 'ㅂ': 7, 'ㅃ': 8, 'ㅅ': 9, 'ㅆ': 10, 'ㅇ': 11,
           'ㅈ': 12, 'ㅉ': 13, 'ㅊ': 14, 'ㅋ': 15, 'ㅌ': 16, 'ㅍ': 17, 'ㅎ': 18}
    jung = {'ㅏ': 0, 'ㅐ': 1, 'ㅑ': 2, 'ㅒ': 3, 'ㅓ': 4, 'ㅔ': 5, 'ㅕ': 6, 'ㅖ': 7, 'ㅗ': 8, 'ㅘ': 9, 'ㅙ': 10, 'ㅚ': 11,
            'ㅛ': 12, 'ㅜ': 13, 'ㅝ': 14, 'ㅞ': 15, 'ㅟ': 16, 'ㅠ': 17, 'ㅡ': 18, 'ㅢ': 19, 'ㅣ': 20}
    jong = {'ㄱ': 1, 'ㄲ': 2, 'ㄳ': 3, 'ㄴ': 4, 'ㄵ': 5, 'ㄶ': 6, 'ㄷ': 7, 'ㄹ': 8, 'ㄺ': 9, 'ㄻ': 10, 'ㄼ': 11, 'ㄽ': 12,
            'ㄾ': 13, 'ㄿ': 14, 'ㅀ': 15, 'ㅁ': 16, 'ㅂ': 17, 'ㅄ': 18, 'ㅅ': 19, 'ㅆ': 20, 'ㅇ': 21, 'ㅈ': 22, 'ㅊ': 23,
            'ㅋ': 24, 'ㅌ': 25, 'ㅍ': 26, 'ㅎ': 27}

    b = 0

    """
    * 아래 조건문에서 확인해주지 않는 case는 (ex.자모 2개 : 모음 + 자음)
      모두 프로그램 실행 과정 중에서 이 함수에 인자로 들어오지 못함
    """

    if len(s) <= 1:                                                             # 자모 1개는 조합 불가능하므로 그대로 return
        return s
    elif len(s) == 2:                                                           # 자모 2개
        if s[0] in cho:                                                         # 초성 + 중성
            return chr(0xac00 + 28 * 21 * cho[s[0]] + 28 * jung[s[1]])
        else:                                                                   # 겹모음
            if s[0] == 'ㅗ':
                if s[1] == 'ㅏ':
                    return 'ㅘ'
                elif s[1] == 'ㅐ':
                    return 'ㅙ'
                elif s[1] == 'ㅣ':
                    return 'ㅚ'
            elif s[0] == 'ㅜ':
                if s[1] == 'ㅓ':
                    return 'ㅝ'
                elif s[1] == 'ㅔ':
                    return 'ㅞ'
                elif s[1] == 'ㅣ':
                    return 'ㅟ'
            elif s[0] == 'ㅡ' and s[1] == 'ㅣ':
                return 'ㅢ'
    elif len(s) >= 3:                                                           # 자모 3~5개
        if s[len(s) - 2] == 'ㄱ' and s[len(s) - 1] == 'ㅅ':                       # 겹자음 여부 확인
            b = 3                                                                   # 2개의 자음이 붙어있으나 겹자음이 되지 않을때는 분리해서 출력
        elif s[len(s) - 2] == 'ㄴ':
            if s[len(s) - 1] == 'ㅅ':
                return hangul(s[:-1]) + hangul(s[-1])
            elif s[len(s) - 1] == 'ㅇ':
                return hangul(s[:-1]) + hangul(s[-1])
            elif s[len(s) - 1] == 'ㅈ':
                b = 5
            elif s[len(s) - 1] == 'ㅎ':
                b = 6
            else:
                b = 2
        elif s[len(s) - 2] == 'ㄹ':
            if s[len(s) - 1] == 'ㄴ':
                return hangul(s[:-1]) + hangul(s[-1])
            elif s[len(s) - 1] == 'ㄷ':
                return hangul(s[:-1]) + hangul(s[-1])
            elif s[len(s) - 1] == 'ㅇ':
                return hangul(s[:-1]) + hangul(s[-1])
            elif s[len(s) - 1] == 'ㄱ':
                b = 9
            elif s[len(s) - 1] == 'ㅁ':
                b = 10
            elif s[len(s) - 1] == 'ㅂ':
                b = 11
            elif s[len(s) - 1] == 'ㅅ':
                b = 12
            elif s[len(s) - 1] == 'ㅌ':
                b = 13
            elif s[len(s) - 1] == 'ㅍ':
                b = 14
            elif s[len(s) - 1] == 'ㅎ':
                b = 15
            else:
                b = 5
        elif s[len(s) - 2] == 'ㅂ' and s[len(s) - 1] == 'ㅅ':
            b = 18
        elif s[len(s) - 1] in jong:
            b = jong[s[len(s) - 1]]

        if s[1] == 'ㅗ':                                                         # 겹모음 여부 확인
            if s[2] == 'ㅏ':
                m = 9
            elif s[2] == 'ㅐ':
                m = 10
            elif s[2] == 'ㅣ':
                m = 11
            else:
                m = 8
        elif s[1] == 'ㅜ':
            if s[2] == 'ㅓ':
                m = 14
            elif s[2] == 'ㅔ':
                m = 15
            elif s[2] == 'ㅣ':
                m = 16
            else:
                m = 13
        elif s[1] == 'ㅡ' and s[2] == 'ㅣ':
            m = 19
        else:
            m = jung[s[1]]

        return chr(0xac00 + 28 * 21 * cho[s[0]] + 28 * m + b)


def output1(string, mealy):     # 초성우선
    string_stack = []           # mealy machine으로 출력된 각각의 output symbol과 출력된 후의 state를 [output, state]의 형태로 순서대로 저장
    substring_stack = []        # 초성+중성 혹은 초성+중성+종성으로 이루어진 것으로 확정된 낱말을 순서대로 저장
    substring = ""              # 현재 아직 완성이 안된 output symbol들을 순서대로 저장
    state = mealy.initial       # 각 output symbol이 출력된 후의 state
    if len(string) == 0:
        print("")
    else:
        for c in string:
            if c == '<':                                    # if backspace가 입력되었을 때
                result_str = ""                                 # 출력될 string이 저장될 변수
                if len(substring) == 0:                         # if 완성이 안된 output symbol이 없을 때
                    if len(substring_stack) > 0:                    # if 완성이 된 낱말이 있을 때
                        substring = substring_stack[-1]                 # 완성된 낱말 중 마지막 낱말에서 backspace가 이루어져야 하므로 그 낱말을 substring으로 가져오고
                        substring_stack = substring_stack[:-1]          # substring_stack에서 해당 낱말(마지막 낱말) 제거
                    else:
                        print(result_str)                           # if 완성된 낱말도 없을 경우에는 더이상 지울 것이 없는 상태이므로 empty string 출력
                        continue
                if string_stack[-1][0] == '1':                      # 획추가가 있는 경우에는 획추가가 하나의 단모음을 나타내지 않으므로
                    while string_stack[-1][0] == '1':               # 획추가가 아닐때까지 string_stack에서 마지막 원소를 제거
                        string_stack = string_stack[:-1]            # 이후 string_stack의 마지막 원소를 한번 더 제거해 string_stack에서의 단모음 제거를 완료 (line 771)

                if string_stack[-1][0] == '2':                      # 쌍자음이 있는 경우, backspace를 할 경우 단자음이 남도록 처리
                    if substring[-1] == 'ㄲ':
                        substring = substring[:-1] + 'ㄱ'
                    elif substring[-1] == 'ㄸ':
                        substring = substring[:-1] + 'ㄷ'
                    elif substring[-1] == 'ㅃ':
                        substring = substring[:-1] + 'ㅂ'
                    elif substring[-1] == 'ㅉ':
                        substring = substring[:-1] + 'ㅈ'
                    elif substring[-1] == 'ㅆ':
                        substring = substring[:-1] + 'ㅅ'
                elif string_stack[-1][0] == 'ㅣ':                    # 단모음 + ㅣ 의 경우 단모음이 남도록 처리
                    if substring[-1] == 'ㅐ':
                        substring = substring[:-1] + 'ㅏ'
                    elif substring[-1] == 'ㅔ':
                        substring = substring[:-1] + 'ㅓ'
                    elif substring[-1] == 'ㅒ':
                        substring = substring[:-1] + 'ㅑ'
                    elif substring[-1] == 'ㅖ':
                        substring = substring[:-1] + 'ㅕ'
                    else:
                        substring = substring[:-1]
                elif string_stack[-1][0] == 'ㅗ':                    # ㅜ의 경우, ㅗㅗ로 입력되므로 backspace를 할 때 ㅗ 2개가 모두 지워지도록 처리
                    if string_stack[-2][0] == 'ㅗ':
                        string_stack = string_stack[:-1]
                    substring = substring[:-1]
                elif string_stack[-1][0] == 'ㅏ':                    # ㅓ의 경우, ㅜ의 경우와 마찬가지 이유로 ㅏ 2개가 모두 지워지도록 처리
                    if string_stack[-2][0] == 'ㅏ':
                        string_stack = string_stack[:-1]
                    substring = substring[:-1]
                else:                                               # 상기된 특수한 경우 이외에는 별도의 처리과정 없이 substring의 마지막 자모를 제거하기만 함
                    substring = substring[:-1]
                string_stack = string_stack[:-1]

                if len(string_stack) > 0:                           # 단모음 제거 후 string_stack에 원소가 있으면 마지막 원소에 해당하는 state로 변경
                    state = string_stack[-1][1]
                else:
                    state = mealy.initial

                if len(string_stack) > 0:
                    if len(substring_stack) > 0 and string_stack[-1][1] not in state_cho and string_stack[-1][1] not in state_jung and len(substring) == 1:
                        substring = substring_stack[-1] + substring                 # substring의 길이가 1이고 이미 완성된 낱말이 있으며 substring이 초성인지 아닌지 모를 때(not in state_cho and not in state_jung)
                        substring_stack = substring_stack[:-1]
                if len(substring) == 0:
                    if len(substring_stack) > 0:                                    # substring의 길이가 0일 때
                        substring = substring_stack[-1]
                        substring_stack = substring_stack[:-1]                      # 두 경우 모두 마지막으로 완성된 낱말을 미완성 substring으로 바꾸어주는 과정
                    else:
                        print(result_str)
                        continue
                for substr in substring_stack:
                    result_str = result_str + hangul(substr)                        # 완성된 낱말을 result string에 포함
                # print(string_stack)
                if string_stack[-1][1] not in state_cho and string_stack[-1][1] not in state_jung:
                    result_str = result_str + hangul(substring[:-1]) + hangul(substring[-1])        # 마지막 자모가 종성일 가능성이 있을 경우, 초성우선 방식에 맞추어 분리해서 출력
                else:
                    result_str = result_str + hangul(substring)                                     # 마지막 자모가 확실히 초성이거나 중성일 경우 그대로 처리
                print(result_str)
            else:
                if c in mealy.stf[state]:                                                           # 정상적으로 조합 가능한 경우에만 입력 처리
                    result_str = ""
                    out = mealy.of[state][c]                                                        # output symbol
                    state = mealy.stf[state][c]                                                     # transition 이후 state
                    string_stack.append([out, state])
                    if state in state_cho:                                  # '확실하게' 초성이 입력된 경우 (종성일 가능성 없음)
                        if (substring != "") and not (string_stack[-2][1] in state_cho):  # end of previous word / start of new word
                            if ((string_stack[-1][0] == '2') and (string_stack[-2][1] not in state_cho)) or ((string_stack[-1][0] == '1') and string_stack[-2][1] not in state_cho):
                                substring_stack.append(substring[:-1])
                            else:
                                substring_stack.append(substring)
                            substring = ""
                        if out == '2':                          # 쌍자음 입력
                            substring = substring[:-1]          # 기존의 단자음을 쌍자음으로 교체
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㄲ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅆ'
                            elif string_stack[-2][0] == '1':
                                if string_stack[-3][0] == 'ㄴ':
                                    out = 'ㄸ'
                                elif string_stack[-3][0] == 'ㅁ':
                                    out = 'ㅃ'
                                elif string_stack[-3][0] == 'ㅅ':
                                    out = 'ㅉ'
                        elif out == '1':                        # 획추가 입력 : 기존의 자음을 획추가 자음으로 교체
                            substring = substring[:-1]
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㅋ'
                            elif string_stack[-2][0] == 'ㄴ':
                                out = 'ㄷ'
                            elif string_stack[-2][0] == 'ㅁ':
                                out = 'ㅂ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅈ'
                            elif string_stack[-2][0] == 'ㅇ':
                                out = 'ㅎ'
                            elif string_stack[-2][0] == '1':
                                if string_stack[-3][0] == 'ㄴ':
                                    out = 'ㅌ'
                                elif string_stack[-3][0] == 'ㅁ':
                                    out = 'ㅍ'
                                elif string_stack[-3][0] == 'ㅅ':
                                    out = 'ㅊ'
                        substring = substring + out
                        for substr in substring_stack:
                            result_str = result_str + hangul(substr)
                        result_str = result_str + hangul(substring)
                        print(result_str)
                    elif state in state_jung:               # 중성(모음) 입력
                        if (string_stack[-2][1] not in state_cho) and (string_stack[-2][1] not in state_jung):  # 이전에 입력된 자모가 모음도 아니고 확실한 초성이 아니었으면
                            substring_stack.append(substring[:-1])                                              # 초성으로 취급하여 새로운 substring으로 분리
                            substring = substring[-1]
                        if out == '1':
                            substring_tail = substring[-1]
                            substring = substring[:-1]
                            if substring_tail == 'ㅏ':
                                out = 'ㅑ'
                            elif substring_tail == 'ㅓ':
                                out = 'ㅕ'
                            elif substring_tail == 'ㅗ':
                                out = 'ㅛ'
                            elif substring_tail == 'ㅜ':
                                out = 'ㅠ'
                        elif out == 'ㅏ':
                            if string_stack[-2][0] == 'ㅏ':
                                substring = substring[:-1]
                                out = 'ㅓ'
                            elif string_stack[-2][0] == 'ㅗ':
                                if substring[-1] == 'ㅜ':
                                    out = 'ㅓ'
                                elif substring[-1] == 'ㅗ':
                                    out = 'ㅏ'
                        elif (out == 'ㅗ') and ((len(string_stack) > 2) and (string_stack[-2][0] == 'ㅗ')):
                            substring = substring[:-1]
                            out = 'ㅜ'
                        elif (out == 'ㅣ') and ((len(substring) > 0) and ((substring[-1] == 'ㅏ') or (substring[-1] == 'ㅓ') or (substring[-1] == 'ㅕ') or (substring[-1] == 'ㅑ'))):
                            substring_tail = substring[-1]
                            substring = substring[:-1]
                            if substring_tail == 'ㅏ':
                                out = 'ㅐ'
                            elif substring_tail == 'ㅓ':
                                out = 'ㅔ'
                            elif substring_tail == 'ㅕ':
                                out = 'ㅖ'
                            elif substring_tail == 'ㅑ':
                                out = 'ㅒ'

                        substring = substring + out
                        for substr in substring_stack:
                            result_str = result_str + hangul(substr)
                        result_str = result_str + hangul(substring)
                        print(result_str)
                    else:               # 확실한 초성도 중성도 아닌 상태의 자음이 입력된 경우 ex) ㅈㅏㄱ의 경우 ㄱ이 초성이 될지 종성이 될지 알 수 없음
                        if out == '2':
                            substring = substring[:-1]          # ㄷ, ㅂ, ㅈ이후에 쌍자음이 입력될 경우 초성state가 되기 때문에 이 조건문에는 들어올 수 없다
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㄲ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅆ'
                        elif out == '1':
                            substring = substring[:-1]
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㅋ'
                            elif string_stack[-2][0] == 'ㄴ':
                                out = 'ㄷ'
                            elif string_stack[-2][0] == 'ㅁ':
                                out = 'ㅂ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅈ'
                            elif string_stack[-2][0] == 'ㅇ':
                                out = 'ㅎ'
                            elif string_stack[-2][0] == '1':
                                if string_stack[-3][0] == 'ㄴ':
                                    out = 'ㅌ'
                                elif string_stack[-3][0] == 'ㅁ':
                                    out = 'ㅍ'
                                elif string_stack[-3][0] == 'ㅅ':
                                    out = 'ㅊ'
                        for substr in substring_stack:
                            result_str = result_str + hangul(substr)
                        result_str = result_str + hangul(substring) + hangul(out)   # 초성우선 방식이기 때문에 받침을 이룰 수 있더라도 마지막 자음은 분리시킨다
                        substring = substring + out
                        print(result_str)
                else:
                    print("Error : wrong input")
                    break


def output2(string, mealy):      # 종성우선 : 전체적인 틀은 초성우선과 같다
    string_stack = []
    substring_stack = []
    substring = ""
    state = mealy.initial
    if len(string) == 0:
        print("")
    else:
        for c in string:
            if c == '<' :
                result_str = ""
                if len(substring) == 0:
                    if len(substring_stack) > 0:
                        substring = substring_stack[-1]
                        substring_stack = substring_stack[:-1]
                    else:
                        print(result_str)
                        continue
                if string_stack[-1][0] == '1':
                    while string_stack[-1][0] == '1':
                        string_stack = string_stack[:-1]
                if string_stack[-1][0] == '2':
                    if substring[-1] == 'ㄲ':
                        substring = substring[:-1] + 'ㄱ'
                    elif substring[-1] == 'ㄸ':
                        substring = substring[:-1] + 'ㄷ'
                    elif substring[-1] == 'ㅃ':
                        substring = substring[:-1] + 'ㅂ'
                    elif substring[-1] == 'ㅉ':
                        substring = substring[:-1] + 'ㅈ'
                    elif substring[-1] == 'ㅆ':
                        substring = substring[:-1] + 'ㅅ'
                elif string_stack[-1][0] == 'ㅣ':
                    if substring[-1] == 'ㅐ':
                        substring = substring[:-1] + 'ㅏ'
                    elif substring[-1] == 'ㅔ':
                        substring = substring[:-1] + 'ㅓ'
                    elif substring[-1] == 'ㅒ':
                        substring = substring[:-1] + 'ㅑ'
                    elif substring[-1] == 'ㅖ':
                        substring = substring[:-1] + 'ㅕ'
                    else:
                        substring = substring[:-1]
                elif string_stack[-1][0] == 'ㅗ':
                    if substring[-1] == 'ㅜ':
                        string_stack = string_stack[:-1]
                    substring = substring[:-1]
                elif string_stack[-1][0] == 'ㅏ':
                    if string_stack[-2][0] == 'ㅏ':
                        string_stack = string_stack[:-1]
                    substring = substring[:-1]
                else:
                    substring = substring[:-1]
                string_stack = string_stack[:-1]
                if len(string_stack) > 0:
                    state = string_stack[-1][1]
                else:
                    state = mealy.initial
                if len(string_stack) > 0:
                    if len(substring_stack) > 0 and string_stack[-1][1] not in state_cho and string_stack[-1][1] not in state_jung and len(substring) == 1:
                        if (substring != "ㅃ") and(substring != "ㅉ") and (substring != "ㄸ"):
                            substring = substring_stack[-1] + substring
                            substring_stack = substring_stack[:-1]
                if len(substring) == 0 and len(substring_stack) > 0:
                    substring = substring_stack[-1] + substring
                    substring_stack = substring_stack[:-1]
                for substr in substring_stack:
                    result_str = result_str + hangul(substr)
                result_str = result_str + hangul(substring)
                print(result_str)
            else:
                if c in mealy.stf[state]:
                    result_str = ""
                    out = mealy.of[state][c]
                    state = mealy.stf[state][c]
                    string_stack.append([out, state])
                    if state in state_cho:
                        if (substring != "") and not(string_stack[-2][1] in state_cho):         # end of previous word / start of new word
                            if ((string_stack[-1][0] == '2') and (string_stack[-2][1] not in state_cho)) or ((string_stack[-1][0] == '1') and string_stack[-2][1] not in state_cho):
                                substring_stack.append(substring[:-1])
                            else:
                                substring_stack.append(substring)
                            substring = ""
                        if out == '2':
                            substring = substring[:-1]
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㄲ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅆ'
                            elif string_stack[-2][0] == '1':
                                if string_stack[-3][0] == 'ㄴ':
                                    out = 'ㄸ'
                                elif string_stack[-3][0] == 'ㅁ':
                                    out = 'ㅃ'
                                elif string_stack[-3][0] == 'ㅅ':
                                    out = 'ㅉ'
                        elif out == '1':
                            substring = substring[:-1]
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㅋ'
                            elif string_stack[-2][0] == 'ㄴ':
                                out = 'ㄷ'
                            elif string_stack[-2][0] == 'ㅁ':
                                out = 'ㅂ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅈ'
                            elif string_stack[-2][0] == 'ㅇ':
                                out = 'ㅎ'
                            elif string_stack[-2][0] == '1':
                                if string_stack[-3][0] == 'ㄴ':
                                    out = 'ㅌ'
                                elif string_stack[-3][0] == 'ㅁ':
                                    out = 'ㅍ'
                                elif string_stack[-3][0] == 'ㅅ':
                                    out = 'ㅊ'
                        substring = substring + out
                        for substr in substring_stack:
                            result_str = result_str + hangul(substr)
                        result_str = result_str + hangul(substring)
                        print(result_str)
                    elif state in state_jung:
                        if (string_stack[-2][1] not in state_cho) and (string_stack[-2][1] not in state_jung):
                            substring_stack.append(substring[:-1])
                            substring = substring[-1]
                        if out == '1':
                            substring_tail = substring[-1]
                            substring = substring[:-1]
                            if substring_tail == 'ㅏ':
                                out = 'ㅑ'
                            elif substring_tail == 'ㅓ':
                                out = 'ㅕ'
                            elif substring_tail == 'ㅗ':
                                out = 'ㅛ'
                            elif substring_tail == 'ㅜ':
                                out = 'ㅠ'
                        elif out == 'ㅏ':
                            if string_stack[-2][0] == 'ㅏ':
                                substring = substring[:-1]
                                out = 'ㅓ'
                            elif string_stack[-2][0] == 'ㅗ':
                                if substring[-1] == 'ㅜ':
                                    out = 'ㅓ'
                                elif substring[-1] == 'ㅗ':
                                    out = 'ㅏ'
                        elif (out == 'ㅗ') and ((len(string_stack)>2) and(string_stack[-2][0] == 'ㅗ')):
                            substring = substring[:-1]
                            out = 'ㅜ'
                        elif (out == 'ㅣ') and ((len(substring)>0) and ((substring[-1] == 'ㅏ') or (substring[-1] == 'ㅓ') or (substring[-1] == 'ㅕ') or (substring[-1] == 'ㅑ'))):
                            substring_tail = substring[-1]
                            substring = substring[:-1]
                            if substring_tail == 'ㅏ':
                                out = 'ㅐ'
                            elif substring_tail == 'ㅓ':
                                out = 'ㅔ'
                            elif substring_tail == 'ㅕ':
                                out = 'ㅖ'
                            elif substring_tail == 'ㅑ':
                                out = 'ㅒ'

                        substring = substring + out
                        for substr in substring_stack:
                            result_str = result_str + hangul(substr)
                        result_str = result_str + hangul(substring)
                        print(result_str)
                    else:
                        if out == '2':
                            substring = substring[:-1]
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㄲ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅆ'
                        elif out == '1':
                            substring = substring[:-1]
                            if string_stack[-2][0] == 'ㄱ':
                                out = 'ㅋ'
                            elif string_stack[-2][0] == 'ㄴ':
                                out = 'ㄷ'
                            elif string_stack[-2][0] == 'ㅁ':
                                out = 'ㅂ'
                            elif string_stack[-2][0] == 'ㅅ':
                                out = 'ㅈ'
                            elif string_stack[-2][0] == 'ㅇ':
                                out = 'ㅎ'
                            elif string_stack[-2][0] == '1':
                                if string_stack[-3][0] == 'ㄴ':
                                    out = 'ㅌ'
                                elif string_stack[-3][0] == 'ㅁ':
                                    out = 'ㅍ'
                                elif string_stack[-3][0] == 'ㅅ':
                                    out = 'ㅊ'
                        substring = substring + out
                        for substr in substring_stack:
                            result_str = result_str + hangul(substr)
                        result_str = result_str + hangul(substring)
                        print(result_str)
                else:
                    print("Error : wrong input")
                    break


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

    mealy1 = make_mealy(result_mdfa)

    while True:
        opt = input("초성우선 : 1, 종성우선 : 2, 종료 : 3 => ")
        if opt == '3':
            break
        if opt == '1':
            input_str = input("[초성우선] 한글 입력 : ")
            output1(input_str, mealy1)
        elif opt == '2':
            input_str = input("[종성우선] 한글 입력 : ")
            output2(input_str, mealy1)
        else:
            print("Wrong Input")



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