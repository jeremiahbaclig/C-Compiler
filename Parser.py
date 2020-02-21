# Jeremiah Baclig - Parser (2/19/2020)


import re
import sys


def looper(split_txt, regexes, tokens):
    for characters in split_txt:
        temp = characters
        for index in regexes:
            for index in regexes:
                if index.match(temp) is not None:
                    if regexes[0] is index:
                        tokens.append(index.match(temp).group())
                        temp = temp.replace(index.match(temp).group(), '', 1)
                    elif regexes[1] is index:
                        tokens.append(index.match(temp).group())
                        temp = temp.replace(index.match(temp).group(), '', 1)
                    elif regexes[2] is index:
                        tokens.append(index.match(temp).group())
                        temp = temp.replace(index.match(temp).group(), '', 1)
                    elif regexes[3] is index:
                        tokens.append(index.match(temp).group())
                        temp = temp.replace(index.match(temp).group(), '', 1)
                    elif regexes[4] is index:
                        tokens.append(index.match(temp).group())
                        temp = temp.replace(index.match(temp).group(), '', 1)
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
errors = re.compile('.')
regex_list = [keywords, special, id, num, errors]

try:
    file = open(sys.argv[1], 'r')
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
looper(text, regex_list, tokens)

if not tokens:
    print("REJECT")
    sys.exit(0)
else:
    tokens.append("$")

file.close()


def next_token():
    global i
    i += 1


def program():
    declaration_list()
    if tokens[i] == "$":
        print("ACCEPT")
    else:
        print("REJECT")
        sys.exit(0)


def declaration_list():
    declaration()
    declaration_list_prime()


def declaration_list_prime():
    if tokens[i] == "int" or tokens[i] == "void":
        next_token()
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


def declaration_prime():
    if tokens[i] == ";" or tokens[i] == "[":
        var_declaration()
    elif tokens[i] == "(":
        fun_declaration()


def var_declaration():
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
                    print("REJECT")
                    sys.exit(0)
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)


def type_specifier():
    if tokens[i] == "int":
        next_token()
    elif tokens[i] == "void":
        next_token()


def fun_declaration():
    if tokens[i] == "(":
        next_token()
        params()
        if tokens[i] == ")":
            next_token()
            compound_stmt()
        else:
            print("REJECT")
            sys.exit(0)


def params():
    if tokens[i] == "int":
        next_token()
        param_prime()
        param_list_prime()
    elif tokens[i] == "void":
        next_token()
        params_prime()


def params_prime():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        param_prime()
        param_list_prime()
    else:
        return


def param_list_prime():
    if tokens[i] == ",":
        next_token()
        param()
        param_list_prime()
    else:
        return


def param():
    if tokens[i] == "int":
        next_token()
        param_prime()
    elif tokens[i] == "void":
        next_token()
        param_prime()


def param_prime():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        param_d_prime()


def param_d_prime():
    if tokens[i] == "[":
        next_token()
        if tokens[i] == "]":
            next_token()
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def compound_stmt():
    if tokens[i] == "{":
        next_token()
        local_declarations_prime()  # K'
        stmt_list_prime()  # L'
        if tokens[i] == "}":
            next_token()
        else:
            print("REJECT")
            sys.exit(0)


def local_declarations_prime():
    if tokens[i] == "int" or tokens[i] == "void":
        next_token()
        if tokens[i].isalpha() and tokens[i] not in keyword_list:
            next_token()
            declaration_prime()
            local_declarations_prime()
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def stmt_list_prime():
    if tokens[i] == "(" or tokens[i] == ";" or tokens[i] == "if" or tokens[i] == "while" \
            or tokens[i] == "return" or tokens[i] == "{":
        statement()
        stmt_list_prime()
    elif tokens[i].isalpha() and tokens[i] not in keyword_list or tokens[i].isnumeric():
        statement()
        stmt_list_prime()
    else:
        return


def statement():
    if tokens[i] == "(" or tokens[i] == ";":
        exp_stmt()  # N
    elif tokens[i].isalpha() and tokens[i] not in keyword_list or tokens[i].isnumeric():
        exp_stmt()
    elif tokens[i] == "{":
        compound_stmt()  # J
    elif tokens[i] == "if":
        select_stmt()  # O
    elif tokens[i] == "while":
        iter_stmt()  # P
    elif tokens[i] == "return":
        return_stmt()  # Q


def exp_stmt():
    if tokens[i] == "(":
        expression()
    elif tokens[i].isalpha() or tokens[i].isnumeric():
        expression()
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
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)


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
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)


def return_stmt():
    if tokens[i] == "return":
        next_token()
        return_stmt_prime()


def return_stmt_prime():
    if tokens[i] == "!=" or tokens[i] == "(" or tokens[i] == "+" or tokens[i] == "-" or tokens[i] == "<" or \
            tokens[i] == "==" or tokens[i] == ">":
        next_token()
        expression()
    elif tokens[i].isalpha() or tokens[i].isnumeric():
        next_token()
        expression()
        if tokens[i] == ";":
            next_token()
        else:
            print("REJECT")
            sys.exit(0)

    if tokens[i] == ";":
        next_token()


def expression():
    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        expression_prime()
    elif tokens[i] == "(":
        next_token()
        expression()
        if tokens[i] == ")":
            next_token()
            term_prime()
            add_exp_prime()
            simp_exp_prime()
        else:
            print("REJECT")
            sys.exit(0)
    elif tokens[i].isnumeric():
        next_token()
        term_prime()
        add_exp_prime()
        simp_exp_prime()
    elif tokens[i] == "+" or tokens[i] == "-":
        add_exp_prime()
        simp_exp_prime()


def expression_prime():
    var_prime()
    if tokens[i] == "=":
        next_token()
        expression()
    elif tokens[i] == "(" or tokens[i] == "[":
        factor_prime()
        term_prime()
        add_exp_prime()
        simp_exp_prime()


def var_prime():
    if tokens[i] == "[":
        next_token()
        expression()
        if tokens[i] == "]":
            next_token()
        else:
            print("REJECT")
            sys.exit(0)
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
        term()
        add_exp_prime()
    else:
        return


def addop():
    if tokens[i] == "+":
        next_token()
    elif tokens[i] == "-":
        next_token()
    # OR


def term():
    if tokens[i] == "(":
        factor()
        term_prime()
    elif tokens[i].isalpha() or tokens[i].isnumeric():
        factor()
        term_prime()
    else:
        return


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
            return

    if tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        factor_prime()
    elif tokens[i].isnumeric():
        next_token()


def factor_prime():
    # accept [
    if tokens[i] == "[":
        next_token()
        expression()
        if tokens[i] == "]":
            next_token()
        else:
            print("REJECT")
            sys.exit(0)
    elif tokens[i] == "(":
        call()
    else:
        return


def call():
    if tokens[i] == "(":
        next_token()
        args()
        if tokens[i] == ")":
            next_token()
        else:
            print("REJECT")
            sys.exit(0)


def args():
    if tokens[i] == "!=" or tokens[i] == "(" or tokens[i] == "+" or tokens[i] == "-" or tokens[i] == "<" or \
            tokens[i] == "==" or tokens[i] == ">":
        arg_list()
    elif tokens[i].isnumeric() or tokens[i].isalpha():
        arg_list()
    else:
        return


def arg_list():
    if tokens[i] == "[":
        next_token()
        var_prime()
        if tokens[i] == "=":
            next_token()
            expression()
            arg_list_prime()
        else:
            print("REJECT")
            sys.exit(0)
    elif tokens[i] == "(":
        next_token()
        expression()
        if tokens[i] == ")":
            next_token()
            term_prime()
            add_exp_prime()
            simp_exp_prime()
            arg_list_prime()
        else:
            print("REJECT")
            sys.exit(0)
    elif tokens[i].isalpha() and tokens[i] not in keyword_list:
        next_token()
        factor_prime()
        term_prime()
        add_exp_prime()
        simp_exp_prime()
        arg_list_prime()
    elif tokens[i].isnumeric():
        next_token()
        term_prime()
        add_exp_prime()
        simp_exp_prime()
        arg_list_prime()
    else:
        return


def arg_list_prime():
    if tokens[i] == ",":
        next_token()
        expression()
        arg_list_prime()
    else:
        return


program()
