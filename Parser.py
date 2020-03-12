# Jeremiah Baclig - Parser(fixed) - 3/12/2020

import re
import sys

def looper(split_txt, regexes, tokens):
    for characters in split_txt:
        temp = characters
        for index in regexes:
            for index in regexes:
                for index in regexes:
                    if index.match(temp) is not None:
                        match_string = index.match(temp).group()
                        if regexes[0] is index:
                            tokens.append(index.match(temp).group())
                            temp = temp.replace(match_string, '', 1)
                        elif regexes[1] is index:
                            tokens.append(index.match(temp).group())
                            temp = temp.replace(match_string, '', 1)
                        elif regexes[2] is index:
                            tokens.append(index.match(temp).group())
                            temp = temp.replace(match_string, '', 1)
                        elif regexes[3] is index:
                            tokens.append(index.match(temp).group())
                            temp = temp.replace(match_string, '', 1)
                        elif regexes[4] is index:
                            tokens.append(index.match(temp).group())
                            temp = temp.replace(match_string, '', 1)
                    if temp == "":
                        break
    return tokens

keyword_list = ['return', 'while', 'else', 'void', 'int', 'if']
keywords = re.compile('return|while|else|void|int|if')
special = re.compile('-|\+|\/\*|\*\/|\*|\/|<=|<|>=|>|==|!=|=|;|,|\)|\(|]|\[|{|}')
id = re.compile('[a-z]+|[A-Z]+')
num = re.compile('[0-9]+')
singComments = re.compile('//.*')
multiComments = re.compile('(?s)/\*.*?\*/')
errors = re.compile('@|\!|\_')
regex_list = [id, special, keywords, num, errors]

try:
    file = open('test.txt', 'r')
except FileNotFoundError:
    print("File not found.")
    sys.exit()
except IndexError:
    print("Index error. Specify file.")
    sys.exit()

reader = file.read()
comments = re.sub(singComments, '', reader)
rComments = re.sub(multiComments, '', comments)

text = rComments.split()

i = 0
tokens = []
tokens = looper(text, regex_list, tokens)

if not tokens:
    print("REJECT")
    sys.exit(0)
else:
    tokens.append("$")
file.close()

def next_token():
    global i
    i += 1

def reject():
    print("REJECT")
    sys.exit(0)

def program():
    declaration_list()
    if tokens[i] == "$":
        print("ACCEPT")
    else:
        reject()

def declaration_list():
    declaration()
    declaration_list_prime()

def declaration_list_prime():
    if tokens[i] == "int" or tokens[i] == "void":
        declaration()
        declaration_list_prime()
    elif tokens[i] == "$":
        return
    else:
        return

def declaration():
    type_specifier()
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        declaration_prime()
    else:
        reject()

def declaration_prime():
    if tokens[i] == ";" or tokens[i] == "[":
        var_declaration_prime()
    elif tokens[i] == "(":
        next_token()
        params()
        if tokens[i] == ")":
            next_token()
            compound_stmt()
        else:
            reject()

def var_declaration():
    type_specifier()
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        var_declaration_prime()
    else:
        reject()

def var_declaration_prime():
    if tokens[i] == ";":
        next_token()
    elif tokens[i] == "[":
        next_token()
        if tokens[i].isnumeric():
            next_token()
            if tokens[i] == "]":
                next_token()
                if tokens[i] == ";":
                    next_token()
                else:
                    reject()
            else:
                reject()
        else:
            reject()

def type_specifier():
    if tokens[i] == "int":
        next_token()
    elif tokens[i] == "void":
        next_token()

def params():
    if tokens[i] == "int":
        next_token()
        params_dprime()
    elif tokens[i] == "void":
        next_token()
        params_prime()
    else:
        reject()  # CHANGED THIS PLS DOUBLE CHECK

def params_prime():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        params_dprime()
    else:
        return

def params_dprime():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        param_prime()
        param_list()

def param_list():
    if tokens[i] == ",":
        next_token()
        param()
        param_list()
    else:
        return

def param():
    if tokens[i] == "int" or tokens[i] == "void":
        type_specifier()
        if tokens[i].isalpha() and tokens[i] not in keyword_list:
            next_token()
            param_prime()
        else:
            reject()

def param_prime():
    if tokens[i] == "[":
        next_token()
        if tokens[i] == "]":
            next_token()
            param_prime()
        else:
            reject()
    else:
        return

def compound_stmt():
    if tokens[i] == "{":
        next_token()
        local_declarations()
        stmt_list()
        if tokens[i] == "}":
            next_token()
        else:
            reject()

def local_declarations():
    if tokens[i] == "int" or tokens[i] == "void":
        var_declaration()
        local_declarations()
    else:
        return

def stmt_list():
    if tokens[i] == "(" or tokens[i] == ";" or tokens[i] == "if" or tokens[i] == "while" \
            or tokens[i] == "return" or tokens[i] == "{":
        statement()
        stmt_list()
    elif tokens[i].isalpha() and tokens[i] not in keyword_list or tokens[i].isnumeric():
        statement()
        stmt_list()
    else:
        return

def statement():
    if tokens[i] == "(" or tokens[i] == ";":
        exp_stmt()
    elif tokens[i].isalpha() and tokens[i] not in keyword_list or tokens[i].isnumeric():
        exp_stmt()
    elif tokens[i] == "{":
        compound_stmt()
    elif tokens[i] == "if":
        select_stmt()
    elif tokens[i] == "while":
        iter_stmt()
    elif tokens[i] == "return":
        return_stmt()

def exp_stmt():
    if tokens[i] == "(":
        expression()
        if tokens[i] == ";":
            next_token()
        else:
            reject()
    elif tokens[i].isalpha() and tokens[i] not in keyword_list or tokens[i].isnumeric():
        expression()
        if tokens[i] == ";":
            next_token()
        else:
            reject()
    elif tokens[i] == ";":
        next_token()

def select_stmt():
    if tokens[i] == "if":
        next_token()
        if tokens[i] == "(":
            next_token()
            expression()
            if tokens[i] == ")":
                next_token()
                statement()
                select_stmt_prime()
            else:
                reject()
        else:
            reject()

def select_stmt_prime():
    if tokens[i] == "else":
        next_token()
        statement()
    else:
        return

def iter_stmt():
    if tokens[i] == "while":
        next_token()
        if tokens[i] == "(":
            next_token()
            expression()
            if tokens[i] == ")":
                next_token()
                statement()
            else:
                reject()
        else:
            reject()

def return_stmt():
    if tokens[i] == "return":
        next_token()
        return_stmt_prime()

def return_stmt_prime():
    if tokens[i] == ";":
        next_token()
    elif tokens[i] == "(":
        expression()
    elif tokens[i].isalpha() and tokens[i] not in keyword_list or tokens[i].isnumeric():
        expression()
        if tokens[i] == ";":
            next_token()
        else:
            reject()

def expression():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        expression_prime()
    elif tokens[i] == "(":
        next_token()
        expression()
        if tokens[i] == ")":
            next_token()
            expression_tprime()
        else:
            reject()
    elif tokens[i].isnumeric():
        next_token()
        expression_tprime()
    else:
        reject()

def expression_prime():
    if tokens[i] == "(":
        next_token()
        args()
        if tokens[i] == ")":
            next_token()
            expression_tprime()
        else:
            reject()
    var_prime()
    expression_dprime()

def expression_dprime():
    if tokens[i] == "=":
        next_token()
        expression()
    else:
        expression_tprime()

def expression_tprime():
    term_prime()
    add_exp_prime()
    simp_exp_prime()

def var():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        var_prime()

def var_prime():
    if tokens[i] == "[":
        next_token()
        expression()
        if tokens[i] == "]":
            next_token()
        else:
            reject()
    else:
        return

def simp_exp():
    add_exp()
    simp_exp_prime()

def simp_exp_prime():
    if tokens[i] == "<=" or tokens[i] == ">=" or tokens[i] == "==" or tokens[i] == "!=" or tokens[i] == ">" \
            or tokens[i] == "<":
        relop()
        add_exp()
    else:
        return

def relop():
    if tokens[i] == "<":
        next_token()
    elif tokens[i] == ">":
        next_token()
    elif tokens[i] == "<=":
        next_token()
    elif tokens[i] == ">=":
        next_token()
    elif tokens[i] == "==":
        next_token()
    elif tokens[i] == "!=":
        next_token()

def add_exp():
    term()
    add_exp_prime()

def add_exp_prime():
    if tokens[i] == "+" or tokens[i] == "-":
        addop()
        if tokens[i] == "(" or tokens[i].isnumeric() or tokens[i].isalpha() and tokens[i] not in keyword_list:
            term()
            add_exp_prime()
        else:
            reject()
    else:
        return

def addop():
    if tokens[i] == "+":
        next_token()
    elif tokens[i] == "-":
        next_token()

def term():
    factor()
    term_prime()

def term_prime():
    if tokens[i] == "*" or tokens[i] == "/":
        mulop()
        factor()
        term_prime()
    else:
        return

def mulop():
    if tokens[i] == "*":
        next_token()
    elif tokens[i] == "/":
        next_token()

def factor():
    if tokens[i] == "(":
        next_token()
        expression()
        if tokens[i] == ")":
            next_token()
        else:
            reject()

    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        factor_prime()
    elif tokens[i].isnumeric():
        next_token()

def factor_prime():
    if tokens[i] == "[":
        var_prime()
    elif tokens[i] == "(":
        next_token()
        args()
        if tokens[i] == ")":
            next_token()
        else:
            reject()

def call():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        if tokens[i] == "(":
            next_token()
            args()
            if tokens[i] == ")":
                next_token()
            else:
                reject()
        else:
            reject()

def args():
    if tokens[i] == "(":
        arg_list()
    elif tokens[i].isnumeric() or tokens[i].isalpha() and tokens[i] not in keyword_list:
        arg_list()
    else:
        return

def arg_list():
    if tokens[i] == "(":
        expression()
        arg_list_prime()
    elif tokens[i].isnumeric() or tokens[i].isalpha() and tokens[i] not in keyword_list:
        expression()
        arg_list_prime()

def arg_list_prime():
    if tokens[i] == ",":
        next_token()
        expression()
        arg_list_prime()
    else:
        return

program()
