
import json

def convertToPostfixNotation():
    global RegEx
    global operators
    global parenthesis
    global priorities
    # introducem simbolul concatenarii
    i = 0
    while i < len(RegEx)-1 :
        if ( RegEx[i] == '*' or RegEx[i] == '+' or RegEx[i] == '?' or RegEx[i] not in operators) and RegEx[i] != '(' and RegEx[i+1] not in operators and RegEx[i+1] != ')':
            RegEx = RegEx[:i+1] + "." + RegEx[i+1:]
            i += 1
        i += 1

    postfixNotation = []
    stack = []
    for x in RegEx:
        if x not in operators and x not in parenthesis: # e doar un simbol
            postfixNotation.append(x)
        else:
            if x in operators: # e operator

                if len(stack) > 0:
                    top_of_stack = stack[ len(stack)-1 ]
                    if top_of_stack != '(' and priorities[x] > priorities[top_of_stack] or top_of_stack == '(':
                        stack.append(x)
                    else:
                        if top_of_stack != '(' and priorities[x] <= priorities[top_of_stack]:
                            postfixNotation.append(top_of_stack)
                            stack.pop()
                            stack.append(x)
                else:
                    stack.append(x)
            else: # e paranteza
                if x == '(':
                    stack.append(x)
                else:
                    top_of_stack = stack[ len(stack)-1 ]
                    while top_of_stack != '(':
                        postfixNotation.append(top_of_stack)
                        stack.pop()
                        top_of_stack = stack[ len(stack)-1 ]
                    stack.pop()

    top_of_stack = stack[ len(stack)-1 ]
    while len(stack) > 0 :
        postfixNotation.append(top_of_stack)
        stack.pop()
        if len(stack) > 0:
            top_of_stack = stack[ len(stack)-1 ]

    return postfixNotation

#structura tuplului nfa-urilor
#(start, end, transitions)

def convertToLambdaNFA():
    global postfixNotation
    global operators
    global numarStari 
    numarStari = 0
    # caut primul operator, care va fi la pozitia i
    op = postfixNotation[0]
    i = 0
    while op not in operators:
        i += 1
        op = postfixNotation[i]

    while len(postfixNotation) > 1:
        if op == '*' or  op == '+' or  op == '?': # operator pentru un singur caracter/nfa
            x = postfixNotation[i-1]

            if isinstance(x, list): # este deja un nfa
                new_x = x
                if op == '*':
                    for elem in x[1]: # leaga starile finale de cea initiala
                        new_x[2].append( (elem, "lmb", x[0][0]) )
                    new_x[2].append( ('q'+str(numarStari), "lmb", x[0][0]) ) 
                    new_x[1].append(x[0][0]) # starea initiala actuala o face finala
                    new_x[0] = ['q'+str(numarStari)]  # pune o noua stare initiala
                    numarStari += 1
                if op == '+':
                    for elem in x[1]: # leaga starile finale de cea initiala
                        new_x[2].append( (elem, "lmb", x[0][0]) )
                    new_x[2].append( ('q'+str(numarStari), "lmb", x[0][0]) )
                    new_x[0] = ['q'+str(numarStari)]  # pune o noua stare initiala
                    numarStari += 1
                if op == '?':
                    new_x[2].append( ('q'+str(numarStari), "lmb", x[0][0]) )
                    new_x[1].append(x[0][0]) # starea initiala actuala o face finala
                    new_x[0] = ['q'+str(numarStari)]  # pune o noua stare initiala
                    numarStari += 1

            else: # e inca doar un simbol
                if op == '*':
                    start = ['q'+str(numarStari)]
                    end = ['q'+str(numarStari+2)]
                    transitions = [ ('q'+str(numarStari), "lmb", 'q'+str(numarStari+1)), ('q'+str(numarStari+1), x, 'q'+str(numarStari+1)), ('q'+str(numarStari), "lmb", 'q'+str(numarStari+2)), ('q'+str(numarStari+1), "lmb", 'q'+str(numarStari+2)) ]
                    numarStari += 3
                if op == '+':
                    start = ['q'+str(numarStari)]
                    end = ['q'+str(numarStari+2)]
                    transitions = [ ('q'+str(numarStari), "lmb", 'q'+str(numarStari+1)), ('q'+str(numarStari+1), x, 'q'+str(numarStari+1)), ('q'+str(numarStari+1), x, 'q'+str(numarStari+2)) ]
                    numarStari += 3
                if op == '?':
                    start = ['q'+str(numarStari)]
                    end = ['q'+str(numarStari+1)]
                    transitions = [ ('q'+str(numarStari), x, 'q'+str(numarStari+1)), ('q'+str(numarStari), "lmb", 'q'+str(numarStari+1)) ]
                    numarStari += 2
                new_x = [start, end, transitions]
            postfixNotation[i-1] = new_x
            postfixNotation[i:] = postfixNotation[i+1:]

        else: # operator pentru 2 caractere/nfa-uri
            x, y = postfixNotation[i-2], postfixNotation[i-1]
            nfa = [[], [], []]
            
            if isinstance(x, list):
                if isinstance(y, list): # x si y ambele liste
                    if op == '|':
                        nfa[0] = ['q'+str(numarStari+1)]
                        nfa[1] = ['q'+str(numarStari)]
                        nfa[2] = x[2] + y[2]

                        for elem in x[1]:
                            nfa[2].append( (elem, "lmb", 'q'+str(numarStari)) )
                        for elem in y[1]:
                            nfa[2].append( (elem, "lmb", 'q'+str(numarStari)) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", x[0][0]) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", y[0][0]) )

                        numarStari += 2
                    if op == '.':
                        nfa[0] = x[0]
                        nfa[1] = y[1]
                        nfa[2] = x[2] + y[2]

                        for elem in x[1]:
                            nfa[2].append( (elem, "lmb", y[0][0]) )

                else: # x lista si y simbol
                    if op == '|':
                        nfa[0] = ['q'+str(numarStari+1)]
                        nfa[1] = ['q'+str(numarStari)]
                        nfa[2] = x[2]

                        for elem in x[1]:
                            nfa[2].append( (elem, "lmb", 'q'+str(numarStari)) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", x[0][0]) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", 'q'+str(numarStari+2)) )
                        nfa[2].append( ('q'+str(numarStari+2), y, 'q'+str(numarStari+3)) )
                        nfa[2].append( ('q'+str(numarStari+3), "lmb", 'q'+str(numarStari)) )

                        numarStari += 4
                    if op == '.':
                        nfa[0] = x[0]
                        nfa[1] = ['q'+str(numarStari+1)]
                        nfa[2] = x[2]

                        for elem in x[1]:
                            nfa[2].append( (elem, "lmb", 'q'+str(numarStari)) )
                        nfa[2].append( ('q'+str(numarStari), y, 'q'+str(numarStari+1)) )

                        numarStari += 2
                    

            else: 
                if isinstance(y, list): # x simbol si y lista
                    if op == '|':
                        nfa[0] = ['q'+str(numarStari+1)]
                        nfa[1] = ['q'+str(numarStari)]
                        nfa[2] = y[2]
                    
                        for elem in y[1]:
                            nfa[2].append( (elem, "lmb", 'q'+str(numarStari)) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", y[0][0]) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", 'q'+str(numarStari+2)) )
                        nfa[2].append( ('q'+str(numarStari+2), x, 'q'+str(numarStari+3)) )
                        nfa[2].append( ('q'+str(numarStari+3), "lmb", 'q'+str(numarStari)) )

                        numarStari += 4
                    if op == '.':
                        nfa[0] = ['q'+str(numarStari)]
                        nfa[1] = y[1]
                        nfa[2] = y[2]

                        nfa[2].append( ('q'+str(numarStari), x, 'q'+str(numarStari+1)) )
                        nfa[2].append( ('q'+str(numarStari+1), "lmb", y[0][0]) )

                        numarStari += 2
                else: # x si y ambele simboluri
                    if op == '|':
                        nfa[2].append( ('q'+str(numarStari), "lmb", 'q'+str(numarStari+1)) )
                        nfa[2].append( ('q'+str(numarStari+1), x, 'q'+str(numarStari+2)) )
                        nfa[2].append( ('q'+str(numarStari+2), "lmb", 'q'+str(numarStari+3)) )
                        nfa[2].append( ('q'+str(numarStari), "lmb", 'q'+str(numarStari+4)) )
                        nfa[2].append( ('q'+str(numarStari+4), y, 'q'+str(numarStari+5)) )
                        nfa[2].append( ('q'+str(numarStari+5), "lmb", 'q'+str(numarStari+3)) )

                        nfa[0] = ['q'+str(numarStari)]
                        nfa[1] = ['q'+str(numarStari+3)]
                        numarStari += 6
                        
                    if op == '.':
                        nfa[2].append( ('q'+str(numarStari), x, 'q'+str(numarStari+1)) )
                        nfa[2].append( ('q'+str(numarStari+1), y, 'q'+str(numarStari+2)) )

                        nfa[0] = ['q'+str(numarStari)]
                        nfa[1] = ['q'+str(numarStari+2)]
                        numarStari += 3
            postfixNotation[i-2] = nfa
            postfixNotation [i-1:] = postfixNotation[i+1:]
            i -= 1
        
        # acum trebuie sa gasim urmatorul operator
        if i < len(postfixNotation):
            op = postfixNotation[i]

            while i < len(postfixNotation) and op not in operators:
                i += 1
                if i < len(postfixNotation):
                    op = postfixNotation[i]
    return postfixNotation[0]



def convertToDFA():
    global nfa
    global numarStari

    symbol_dict = {}
    lambda_dict = {}
    for i in range(numarStari):
        lambda_dict[i] = [i]
    
    for transition in nfa[2]:
        if transition[1] != "lmb" and transition[1] not in symbol_dict:
            symbol_dict[ transition[1] ] = {}
        if transition[1] == "lmb":
            x, y = transition[0], transition[2]
            x, y = x[1:], y[1:]
            x, y = int(x), int(y) 
            if y not in lambda_dict[x]:
                lambda_dict[x].append(y)

    # pt fiecare stare, fac "BFS" de stari in care se poate ajunge doar cu lambda
    for i in range(numarStari):
        for x in lambda_dict[i]:
            if x != i:
                for y in lambda_dict[x]:
                    if y not in lambda_dict[i]:
                        lambda_dict[i].append(y)
    for x in lambda_dict:
        lambda_dict[x].sort()
    #print(lambda_dict)
    # dictionarul pentru fiecare simbol
    for transition in nfa[2]:
        if transition[1] != "lmb":
            x, y = transition[0], transition[2]
            x, y = x[1:], y[1:]
            x, y = int(x), int(y) 
            if x not in symbol_dict[ transition[1] ]:
                symbol_dict[ transition[1] ][x] = []
            if y not in symbol_dict[ transition[1] ][x]:
                symbol_dict[ transition[1] ][x].append(y)

    for s in symbol_dict:
        for x in symbol_dict[s]:
            symbol_dict[s][x].sort()
    #print(symbol_dict)

    symb_state_dict = {}
    for state in lambda_dict:
        symb_state_dict[state] = {}
        for s in symbol_dict:
            # fac lista cu stari in care ajung cu lambda* s lambda*
            list1 = []
            for x in lambda_dict[state]:
                if x in symbol_dict[s]:
                    for y in symbol_dict[s][x]:
                        if y not in list1:
                            list1.append(y)
            list2 = []
            for x in list1:
                for y in lambda_dict[x]:
                    if y not in list2:
                        list2.append(y)
            list2.sort()
            symb_state_dict[state][s] = list2
    #print(symb_state_dict)

    # starea initiala a dfa-ului
    x = nfa[0][0]
    x = x[1:]
    x = int(x)
    dfa_start = lambda_dict[x]
    
    dfa_dict = {}
    dfa_states = []
    # BFS 
    queue = [dfa_start]
    while len(queue) > 0:
        k = queue[0]
        queue = queue[1:]
        dfa_states.append(k)

        if ''.join(str(x) for x in k) not in dfa_dict:
            dfa_dict[','.join(str(x) for x in k)] = {}
            # daca dam de o stare neprocesata, trecem prin fiecare simbol
            for s in symbol_dict:
                new_state = []
                for x in k:
                    for y in symb_state_dict[x][s]:
                        if y not in new_state:
                            new_state.append(y) # am calculat starea in care ajunge k cu simbolul s
                new_state.sort()
                dfa_dict[','.join(str(x) for x in k)][s] = ','.join( str(x) for x in new_state)
                if new_state not in dfa_states:
                    queue.append(new_state)
    #print(dfa_dict)
    dfa_start = [','.join( str(x) for x in dfa_start )]

    dfa_end = []
    for state in dfa_dict:
        if state != "":
            state_parts = state.split(',')
            ok = False
            for x in state_parts:
                if 'q' + str(x) in nfa[1]:
                    ok = True
            if ok == True:
                dfa_end.append(state)
    
    dfa_transitions = []
    for state in dfa_dict:
        for s in dfa_dict[state]:
            if dfa_dict[state][s] != "":
                dfa_transitions.append( [state, s, dfa_dict[state][s]] )


    return [ dfa_start, dfa_end, dfa_transitions ]


def validateWithDFA(dfa_start, dfa_end, dfa_transitions, input_string):
    
    current_states = dfa_start 
    for symbol in input_string:
        next_states = []
        
        for state in current_states:
            for transition in dfa_transitions:
                if transition[0] == state and transition[1] == symbol and transition[2] not in next_states:
                    next_states.append(transition[2])
        
        if len(next_states) == 0:
            return False
        
        current_states = next_states
    
    for state in current_states: # la finalul inputului, verificam daca am ajuns intr-o stare finala
        if state in dfa_end:
            return True
    return False
        


with open('LFA-Assignment2_Regex_DFA_v2.json', 'r') as file:
    data = json.load(file)

for elem in data:
    RegEx = elem['regex']
    operators = ".|*+?"
    parenthesis = "()"
    priorities = {'*' : 4 , '+' : 4, '?' : 3, '.' : 2, '|' : 1 }

    postfixNotation = convertToPostfixNotation()
    #print( postfixNotation )

    numarStari = 0
    nfa = convertToLambdaNFA()

    #print(numarStari)

    dfa = convertToDFA()
    #print( dfa )

    for t in elem["test_strings"]:
        print(RegEx, t["input"], validateWithDFA(dfa[0], dfa[1], dfa[2], t["input"]), t["expected"] )