#!/usr/bin/python
import sys
import time


def read_wff(line):
    global promb_counter, problem_list, problem_info
    if (line[0] == 'c'):
        line_list = line.split()
        problem_info = {}
        problem_info["clauses"] = []  # init clauses
        problem_list.append(problem_info)  # append a new problem in the list
        problem_info["promb_num"] = line_list[1]
        problem_info["max_num_literal"] = line_list[2]
        problem_info["test_char"] = line_list[3]
        promb_counter += 1
    elif (line[0] == "p"):
        line_list = line.split()
        problem_info["var_num"] = line_list[2]
        problem_info["clause_num"] = line_list[3]
    else:
        line_list = line.split(',')
        a_clause = []
        for item in line_list[0: len(line_list) - 1]:
            a_clause.append(item)
        problem_info["clauses"].append(a_clause)


def solving_problem(running_mode):
    global promb_counter, problem_list, problem_info
    # running_mode is for test purpose, required by the description
    if (running_mode == '1'):
        for p in problem_list:
            # time_start = time.time() * 1000000

            var_num_int = int(p["var_num"])
            if(var_num_int <= 8 and p["promb_num"] == "1"):
                found = False
                old_wff = p["clauses"]
                literal_dic = {
                    "var_name": "1",
                    "assign": "0",
                }
                stack = [literal_dic]

                while (len(old_wff)>0):
                    print old_wff
                    new_var_name = old_wff[0][0]
                    new_var_name = str(abs(int(new_var_name)))
                    literal_dic = {
                       "var_name": new_var_name,
                        "assign": "0",
                    }
                    stack.append(literal_dic);

                    old_wff = gen_new_wff(old_wff, stack)

                    # found = verify(p["clauses"],init_str)
                    # init_str = gen_next_assign(init_str, var_num_int);

                """
                # time_taken = time.time()*1000000 - time_start
                assgn_list = list(init_str)
                prediction = "U"
                pre_match = "0"
                if (found):
                    prediction = "S"
                if (p["test_char"]!="?"):
                    if(p["test_char"]==prediction):
                        pre_match = "1"
                    else:
                        pre_match = "-1"


                output_info ={
                    "promb_num": p["promb_num"],
                    "var_num" : p["var_num"],
                    "clause_num" : p["clause_num"],
                    "max_num_li": p["max_num_li"],
                    #"total_num_li": todo,
                    "prediction": prediction,
                    "pre_match": pre_match,
                    "time_taken": time_taken,
                    "assignment": assgn_list,
                    "clauses": [["1","2"],["-2","5"]]
                }
        last_line = {
            "last_line": "last",
            "input_file": sys.argv[1],
            "team_name": "satTeam",
            # num of wffs
            # S num
            # U num
            # wff has answer
            # answers correct

        }"""

    elif(running_mode == '0'):
        for p in problem_list:

            time_start = time.time() * 1000000

            var_num_int = int(p["var_num"])
            init_str = bin(0)[2:].zfill(var_num_int)
            found = False
            while (found == False and init_str != "final"):
                found = verify(p["clauses"], init_str)
                init_str = gen_next_assign(init_str, var_num_int)

            time_taken = time.time() * 1000000 - time_start
            assgn_list = list(init_str)
            prediction = "U"
            pre_match = "0"
            if (found):
                prediction = "S"
            if (p["test_char"] != "?"):
                if(p["test_char"] == prediction):
                    pre_match = "1"
                else:
                    pre_match = "-1"

            output_info = {
                "promb_num": p["promb_num"],
                "var_num": p["var_num"],
                "clause_num": p["clause_num"],
                "max_num_li": p["max_num_li"],
                #"total_num_li": todo,
                "prediction": prediction,
                "pre_match": pre_match,
                "time_taken": time_taken,
                "assignment": assgn_list,
                "clauses": [["1", "2"], ["-2", "5"]]
            }


def gen_new_wff(old_wff, stack):
    lit_dic = stack[len(stack) - 1]
    print "Current variable " + lit_dic["var_name"]
    new_wff = []
    for clause in old_wff:
        matched = False
        for variable in clause:
            print "This is the " + str(clause.index(variable)) + " in clause" 
            print clause
            if (variable == lit_dic["var_name"]):
                print variable + " is matched"
                if (lit_dic["assign"] == "0"):
                    indexing = clause.index(variable)
                    clause[indexing] = "delete"
                else:
                    matched = True
            elif (variable == "-" + lit_dic["var_name"]):
                print variable + " is matched for negative"
                if (lit_dic["assign"] == "1"):
                    indexing = clause.index(variable)
                    clause[indexing] = "delete"
                else:
                    matched = True
        clause = list(set(clause))
        if("delete" in clause):
            clause.remove("delete")
        if (len(clause)==0):
            return []
        if (matched == False):
            new_wff.append(clause)
    return new_wff



promb_counter = 0
problem_list = []
problem_info = {"clauses": []}

"""
problem_info ={
    "promb_num": "1",
    "max_num_literal": "4",
    "test_char" : "S",
    "var_num" : "6",
    "clause_num" : "9",
    "clauses": [["1","2"],["-2","5"]]
}
"""


file_name = sys.argv[1]
running_mode = sys.argv[2]
test_file = open(file_name, "r")


try:
    for s in test_file:
        read_wff(s)
except:
    print "Cannot read the file"
finally:
    test_file.close()


# print gen_assignment(4,[])
solving_problem(running_mode)
