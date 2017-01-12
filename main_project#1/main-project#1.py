class Mealy(object):
    def __init__(self):
        self.stf = {}                                               # standard transition function
        self.of = {}                                                # output function
        self.states = []
        self.inputSymbol = []
        self.outputSymbol = []
        self.initial = ""                                           # initial state

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


def make_mealy(mealy_file):
    m = Mealy()
    mealy_file.readline()
    m.state(mealy_file.readline().strip().split(','))               # States
    mealy_file.readline()
    m.input_symbol(mealy_file.readline().strip().split(','))        # Input Symbol
    mealy_file.readline()

    l = mealy_file.readline().strip()
    while len(l.split(',')) == 3:                                   # State transition function
        stf = l.split(',')
        m.makestf(stf)
        l = mealy_file.readline().strip()

    l = mealy_file.readline().strip()
    m.output_symbol(l.split(','))                                   # Output symbol
    mealy_file.readline()

    l = mealy_file.readline().strip()
    while len(l.split(',')) == 3:                                   # Output function
        of = l.split(',')
        m.makeof(of)
        l = mealy_file.readline().strip()
    m.set_initial(mealy_file.readline().strip())                    # Initial state

    return m


def hangul(s):
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
        if s[len(s) - 2] == 'ㄱ' and s[len(s) - 1] == 'ㅅ':                      # 겹자음 여부 확인
            b = 3
        elif s[len(s) - 2] == 'ㄴ':
            if s[len(s) - 1] == 'ㅈ':
                b = 5
            elif s[len(s) - 1] == 'ㅎ':
                b = 6
            else:
                b = 2
        elif s[len(s) - 2] == 'ㄹ':
            if s[len(s) - 1] == 'ㄱ':
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


cho = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
jung = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅒ', 'ㅖ', 'ㅐ', 'ㅔ']
jungseong = ['O', 'U', 'A', 'I', 'W']
jongseong = ['K', 'N', 'R', 'L', 'D']
"""
* S : initial state
* V : 초성 입력
* 중성 state
  O : ㅗ
  U : ㅜ
  A : ㅏ ㅑ ㅓ ㅕ ㅘ ㅝ
  W : ㅡ
  I : ㅛ ㅠ ㅣ ㅐ ㅒ ㅔ ㅖ ㅚ ㅟ ㅢ ㅙ ㅞ
* 종성 state
  K : ㄱ ㅂ
  N : ㄴ
  R : ㄹ
  L : ㄷ ㅁ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ ㄲ ㅆ
  D : ㄳ ㄵ ㄶ ㄺ ㄼ ㄽ ㄾ ㄿ ㅀ

* state D은 겹자음이 될 수 있는 state를 나타내므로
  이후 모음이 input되면 해당 중성 state로, 자음이 입력되면 V로 state 전이되고 output으로 해당 input이 출력됨
"""


# 초성우선
def output1(s, m):
    # state_list에 각 input을 받은 뒤의 state를 순서대로 저장
    state_list = []
    result = ""
    if s == "":
        return result
    else:
        temp = ""           # 현재 완성이 되지 않은 자모들
        word = ""           # 현재 완성이 되지 않은 자모들을 임시로 조합
        backspace = 0       # 연속으로 입력된 backspace의 갯수
        state = m.initial
        for i in range(0, len(s)):
            if len(temp) == 1 and temp in cho:
                state = 'V'         # temp의 자모를 초성으로 인식
            if i != 0:
                state_list.append(state)

            """
            * 현재 state와 input에 대응되는 state가 존재하고
              temp가 empty string 또는 첫 자모가 모음이 아닌 자음 초성이어서 조합이 가능한 case
              또는 space & backspace
            """
            if s[i] == ' ' or s[i] == '<' or (s[i] in m.stf[state] and (len(temp) == 0 or temp[0] in cho)):
                # space
                if s[i] == ' ':
                    backspace = 0                               # backspace가 연속으로 나오지 않았으므로 초기화
                    word = hangul(temp)
                    result += word + ' '
                    temp = ""
                    word = ""
                # backspace
                elif s[i] == '<':
                    if len(temp) != 0:                          # 완성되지 않은 자모가 있을 경우 temp에서 자모 삭제
                        temp = temp[:-1]
                        word = hangul(temp)
                    elif len(result) != 0:                      # 완성되지 않은 자모가 없고 이미 완성된 낱말이 있을경우
                        result = result[:-1]                    # 낱말 삭제
                    else:
                        state = 'S'                             # 모두 empty string인 경우 initial state
                        print("")
                        continue

                    """
                    * 첫 backspace input : 이전 input을 지우고 그 이전 state로 돌아감 (state_list[i - 2])
                      연속된 backspace input : 이전 backspace를 처리한 후의 마지막 input 이전의 state로 돌아감
                                            (state_list[i - 2*(연속 backspace 횟수)])

                    * s[i - 2] 위치에 '<'이 있더라도 state_list[i - 2] 위치엔 이미 backspace 처리로 인해 올바른 state가
                      들어가 있으므로 처리 과정에 문제가 없다

                    * backspace 시 지워지지 않는 부분은 형태가 변하지는 않는다
                      (ex. 알ㅁ< -> 알, 알ㅁ<ㅎㄷㅏ -> 앓다)
                      또한, 완성된 것으로 취급된 낱말은 backspace로 다시 그 글자로 돌아가더라도 미완성 낱말로 취급하지 않는다
                      (ex. 알아<<ㅎ아 -> 알ㅎ아)
                    """
                    state = state_list[i - 2*(backspace+1)]
                    backspace += 1
                else:
                    backspace = 0
                    temp = temp + m.of[state][s[i]]                 # temp에 현재 input 추가
                    state = m.stf[state][s[i]]                      # input에 따라 state 갱신
                    # i != 0일때 input이 무조건 초성이 되어야 하는 위치에 온 경우
                    if i != 0 and state == 'V':
                        word = hangul(temp[:-1])
                        result += word
                        temp = temp[-1]
                        word = hangul(temp)
                    # input이 자음이며 낱말의 받침일 가능성이 있을 경우
                    elif state in jongseong:
                        word = hangul(temp[:-1]) + temp[-1]
                    # input이 모음일 경우
                    elif state in jungseong:
                        if len(temp) >= 2 and temp[-2] in cho:      # 바로 앞에 자음이 나타났던 경우 그 자음을 초성으로 함
                            word = hangul(temp[:-2])
                            result += word
                            temp = temp[-2:]
                            word = hangul(temp)
                        else:
                            word = hangul(temp)
                    # i == 0
                    else:
                        word = hangul(temp)
                print(result + word)                                # 완성된 낱말 + 완성되지 않은 자모들을 조합

            # 정상적인 낱말로 조합이 불가능한 조합 (ex. ㅏㅏㅏㅏ, ㅇㅈㅇㅇㅈ, ㅢ)
            else:
                # 모음 input
                if m.of['D'][s[i]] in jung:
                    # 현재 상태에서 이 input을 받는 상태 전이 함수가 존재 (ex. 겹모음 ㅢ)
                    if s[i] in m.stf[state]:
                        temp += m.of[state][s[i]]
                        word = hangul(temp)
                        state = m.stf[state][s[i]]
                    # 어떤 조합도 불가
                    else:
                        result += hangul(temp)                      # temp를 완성된 string에 붙인 뒤
                        temp = m.of['D'][s[i]]                      # temp를 현재 input으로 교체
                        word = hangul(temp)
                        state = m.stf['D'][s[i]]
                # 자음 input
                else:
                    result += hangul(temp)
                    temp = m.of['D'][s[i]]
                    word = hangul(temp)
                    state = 'V'                                     # temp에 이 input 뿐이므로 초성 입력으로 간주
                print(result + word)


# 종성우선
def output2(s, m):
    # 주석이 없는 부분은 output1과 동일
    state_list = []
    result = ""
    if s == "":
        return result
    else:
        temp = ""
        word = ""
        backspace = 0
        state = m.initial
        for i in range(0, len(s)):
            if len(temp) == 1 and temp in cho:
                state = 'V'
            if i != 0:
                state_list.append(state)
            if s[i] == ' ' or s[i] == '<' or (s[i] in m.stf[state] and (len(temp) == 0 or temp[0] in cho)):
                if s[i] == ' ':
                    backspace = 0
                    word = hangul(temp)
                    result += word + ' '
                    temp = ""
                    word = ""
                elif s[i] == '<':
                    if len(temp) != 0:
                        temp = temp[:-1]
                        word = hangul(temp)
                    elif len(result) != 0:
                        result = result[:-1]
                    else:
                        state = 'S'
                        backspace += 1
                        print("")
                        continue

                    """
                    첫 backspace input : 이전 input을 지우고 그 이전 state로 돌아감 (state_list[i - 2])
                    연속된 backspace input : 이전 backspace를 처리한 후의 마지막 input 이전의 state로 돌아감
                                            (state_list[i - 2*(연속 backspace 횟수)])

                    * s[i - 2] 위치에 '<'이 있더라도 state_list[i - 2] 위치엔 이미 backspace 처리로 인해 올바른 state가
                      들어가 있으므로 처리 과정에 문제가 없다
                    """
                    state = state_list[i - 2 * (backspace+1)]
                    backspace += 1
                else:
                    backspace = 0
                    temp = temp + m.of[state][s[i]]
                    state = m.stf[state][s[i]]
                    # 현재 input이 낱말의 받침일 가능성이 있을 경우
                    if state in jongseong:
                        # 그 다음에 올 자모가 초성이 되는 경우
                        if i != len(s) - 1 and (s[i+1] in m.stf[state] and m.stf[state][s[i+1]] == 'V'):
                            word = hangul(temp)             # 현재 temp에 있는 자모들을 조합해 완성된 string에 추가
                            result += word                  # temp 초기화
                            temp = ""
                            word = ""
                        else:
                            word = hangul(temp)
                    # 현재 모음이 나타난 경우
                    elif state in jungseong:
                        # 앞에 자음이 나타났던 경우
                        if len(temp) >= 2 and temp[-2] in cho:
                            word = hangul(temp[:-2])            # temp에서 마지막 자음을 제외하고 조합 후
                            result += word                      # 완성된 string에 추가
                            temp = temp[-2:]                    # temp에 temp의 마지막 자음 및 모음 input을
                        # 다음에 올 문자가 받침이 될 수 없고 초성이 되는 경우 (ex. ㄸ, ㅃ)
                        if i != len(s) - 1 and (s[i+1] in m.stf[state] and m.stf[state][s[i+1]] == 'V'):
                            word = hangul(temp)
                            result += word
                            temp = ""
                            word = ""
                        else:
                            word = hangul(temp)
                    # state V
                    else:
                        word = hangul(temp)
                print(result + word)

            else:
                if m.of['D'][s[i]] in jung:
                    if s[i] in m.stf[state]:
                        temp += m.of[state][s[i]]
                        word = hangul(temp)
                        state = m.stf[state][s[i]]
                    else:
                        result += hangul(temp)
                        temp = m.of['D'][s[i]]
                        word = hangul(temp)
                        state = m.stf['D'][s[i]]
                else:
                    if m.of['D'][s[i]] in cho:
                        result += hangul(temp)
                        temp = m.of['D'][s[i]]
                        word = hangul(temp)
                        state = 'V'
                print(result + word)


def run(m):
    while True:
        opt = input("초성우선 : 1, 종성우선 : 2, 종료 : 3 => ")
        if opt == '3':
            break
        input_str = input("한글 입력 : ")
        if opt == '1':
            output1(input_str, m)
        elif opt == '2':
            output2(input_str, m)
        else:
            print("Wrong Input")

m_file = open("mealy.txt", "r")
mealy1 = make_mealy(m_file)
run(mealy1)
m_file.close()
