#!/usr/bin/env python

import operator # for operator.gt() and operator.lt()
import os.path # for os.path.isfile()
import re # for re.split()
import sys # for command line args

variables = {} # program variables

# -------------MATH-------------
# return the number (int or float) representation of the string or `None`
# if the variable doesn't exist
def get_number(num):
    try:
        return float(num) if '.' in num else int(num)
    except ValueError:
        try: # a variable name may have been passed in
            x = variables[num]
            return get_number(x) # going deeper down the rabbit hole will 
                                 # fix any problems... right?
        except KeyError: # the variable doesn't exist
            print 'The variable "{0}" does not exist.'.format(num)
            return None

# the rest of the math functions return strings because it's easier to save
# all the 'variables' as one type

def add(num1, num2):
    return str(get_number(num1)+get_number(num2))

def subtract(num1, num2):
    return str(get_number(num1)-get_number(num2))

def multiply(num1, num2):
    return str(get_number(num1)*get_number(num2))

def divide(num1, num2):
    return str(get_number(num1)/get_number(num2))

def exponentiate(num, power):
    return str(get_number(num)**get_number(power))
# ------------------------------

# input method; used when parsing loops
def user_input():
    return raw_input('>>> ').rstrip()

in_method = None # input method; used when parsing loops
fd = None # holds the program file if one provided

# input method; used when parsing loops
def next_line():
    global fd
    return fd.readline().rstrip()

# performs a loop
def loop(counter, until, step, actions):
    # initial loop index
    count = get_number(variables[counter])
    # final loop index
    upto = get_number(until)

    op = None # holds the comparison operation for the loop
    # there is no reason to loop if the starting and final indecies are equal
    if count == upto:
        return None
    elif count > upto: # use greater-than (>)
        op = operator.gt
    elif count < upto: # use less-than (<)
        op = operator.lt

    # loop while the counter hasn't reached the final index
    while op(get_number(variables[counter]), upto):
        # evaluate each action in the "actions" list
        for action in actions:
            evaluate(action)

        # advance the counter
        evaluate(step)

# list of commands and their purposes
def commands():
    print ('Max 256 variables.'
        '\n\n'
        'Math Opertators:'
        '\n\tADD variable, num1, num2      -- variable = num1+num2'
        '\n\tSUB variable, num1, num2      -- variable = num1-num2'
        '\n\tMUL variable, num1, num2      -- variable = num1*num2'
        '\n\tDIV variable, num1, num2      -- variable = num1/num2'
        '\n\tEXP variable, num, power      -- variable = num**power'
        '\n\n'
        'Looping:'
        '\n\tLOOP counter, until, (step)   -- loop while "counter" (inclusive)'
        'doesn\'t overstep "until" (exclusive) following the rule set by "step"'
        '\n\t                                 "counter" must have a value'
        'before used for "LOOP"'
        '\n\t                                 "step" is an arithmetic operation; '
        'ex. "(ADD counter, counter, 1)" to increment by 1'
        '\n\tEND                           -- signifies the end of the loop'
        '\n\n'
        'Other:'
        '\n\tDEF variable, [content=None]  -- define a variable; default value `None`; variable names cannot contain whitespace'
        '\n\tDEL variable                  -- delete a variable'
        '\n\tHELP                          -- this text'
        '\n\tMOV to, from                  -- copy the value of the variable "from" to the variable "to"'
        '\n\tPRINT variable                -- print the variable'
        '\n\tPRNTVARS                      -- prints all the variables and their contents'
        '\n\tEXIT                          -- signifies the end of the program / exits the interpreter')

def print_vars():
    for var in variables.keys():
        print '{0}:\t\t{1}'.format(var, variables[var])

def max_vars():
    return len(variables) == 256

# evaluate the passed in command
def evaluate(command):
    # tokenize the commmand
    tokens = command.split(', ')
    tokens.insert(1, tokens[0].split()[1])
    tokens[0] = tokens[0].split()[0]

    if tokens[0] == 'HELP': # print the commands
        commands()
            
    global variables

    if not max_vars():
        if tokens[0] == 'DEF': # define a variable
            variables[tokens[1]] = None if len(tokens) == 2 else tokens[2]
        elif tokens[0] == 'DEL': # delete a variable
            try:
                del variables[tokens[1]]
            except KeyError:
                print 'The variable "{0}" does not exist.'.format(tokens[1])
        elif tokens[0] == 'MOV': # copy the value of one variable into another
            variables[tokens[1]] = variables[tokens[2]]
        elif tokens[0] == 'PRINT': # print the value of a variable
            print variables[tokens[1]]
        elif tokens[0] == 'PRNTVARS':
            print_vars()
        elif tokens[0] == 'LOOP': # loop through an enclosed process
            # parse the step of the loop
            step = command.split('(')[1].rstrip()[:-1]

            # check if the step is valid
            if step.split()[0] not in ['ADD', 'SUB', 'MUL', 'DIV', 'EXP']:
                print 'The step in the loop must be an arithmetic operation.'
                return None

            actions = []
            # get the next command in the loop and add it to an array
            command = in_method()
            while command != 'END':
                actions.append(command)
                command = in_method()

            # perform the loop
            loop(counter = tokens[1], until = tokens[2], step = step, actions = actions)
        elif tokens[0] == 'ADD': # add two numbers
            variables[tokens[1]] = add(tokens[2], tokens[3])
        elif tokens[0] == 'SUB': # subtract one number from another
            variables[tokens[1]] = subtract(tokens[2], tokens[3])
        elif tokens[0] == 'MUL': # multiply two numbers
            variables[tokens[1]] = multiply(tokens[2], tokens[3])
        elif tokens[0] == 'DIV': # divide one number by another
            variables[tokens[1]] = divide(tokens[2], tokens[3])
        elif tokens[0] == 'EXP': # raise one number to the power of another
            variables[tokens[1]] = exponentiate(tokens[2], tokens[3])
        else:
            print 'Invalid command.'
    else: # too many variables
        if tokens[0] == 'DEL': # delete a variable
            try:
                del variables[tokens[1]]
            except KeyError:
                print 'The variable "{0}" does not exist.'.format(tokens[1])
        else:
            print 'You have created too many variables. Consider deleting some.'
    return 0

def main(argv):
    global in_method
    
    if argv != None:
        global fd
        # open program
        fd = open(argv)

        # set the input method to read from the file
        in_method = next_line
        
        # read the program line-by-line until 'EXIT' is hit
        command = fd.readline().rstrip()
        while command != 'EXIT':
            # evaluate the line; if `None` is returned terminate the program
            if evaluate(command) == None:
                break
            command = fd.readline().rstrip()
    else:
        print 'Input HELP to see the command list.'

        # set the input method to read from the command line
        in_method = user_input

        # while the inputted line is not 'EXIT'
        command = raw_input('>>> ').rstrip()
        while command != 'EXIT':
            # evaluate the line; if `None` is returned print out the list of commands
            if evaluate(command) == None:
                commands()
            
            command = raw_input('>>> ').rstrip()


if __name__ == "__main__":
    # check if .pysm file is passed
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.pysm'):
        main(sys.argv[1])
    else:
        main(None)
