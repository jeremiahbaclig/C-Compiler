# Jeremiah Baclig - Lexer (2/18/2020)

import re, sys


def looper(split_txt, regexes):
    for characters in split_txt:
        temp = characters
        for index in regexes:
            for index in regexes:
                if index.match(temp) is not None:
                    match_string = index.match(temp).group()
                    if regexes[0] is index:
                        print("KW: " + match_string)
                        temp = temp.replace(match_string, '', 1)
                    elif regexes[1] is index:
                        print(match_string)
                        temp = temp.replace(match_string, '', 1)
                    elif regexes[2] is index:
                        print("ID: " + match_string)
                        temp = temp.replace(match_string, '', 1)
                    elif regexes[3] is index:
                        print("NUM: " + match_string)
                        temp = temp.replace(match_string, '', 1)
                    elif regexes[4] is index:
                        print("ERROR: " + match_string)
                        temp = temp.replace(match_string, '', 1)

                if temp == "":
                    break


# regexes & appending to list
keywords = re.compile('return|while|else|void|int|if')
special = re.compile('-|\+|\/\*|\*\/|\*|\/|<=|<|>=|>|==|!=|=|;|,|\)|\(|]|\[|{|}')
id = re.compile('[a-z]+|[A-Z]+')
num = re.compile('[0-9]+')
singComments = re.compile('//.*')
multiComments = re.compile('(?s)/\*.*?\*/')
errors = re.compile('@|\!|\_')
regex_list = [keywords, special, id, num, errors]

# open file and remove comments
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

# split at white space - test print
text = rComments.split()

# call looper func to iterate through list and apply regex list
looper(text, regex_list)

file.close()
