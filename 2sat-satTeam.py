#!/usr/bin/python
import sys
import time
from copy import deepcopy

def read_wff(line):
    global promb_counter, problem_list, problem_info
    if (line[0] == 'c'):
        line_list = line.split()
        problem_info = {}
        problem_info["clauses"] = []  # init clauses
        problem_info["total_num_li"] = 0
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
        problem_info["total_num_li"] += len(line_list) - 1
        a_clause = []
        for item in line_list[0: len(line_list) - 1]:
            a_clause.append(item)
        problem_info["clauses"].append(a_clause)


def solving_problem(running_mode):
    global promb_counter, problem_list
    # running_mode is for test purpose, required by the description
    s_wff = 0
    u_wff = 0
    a_wff = 0
    c_wff = 0
    for p in problem_list:
        var_num_int = int(p["var_num"])
        if (running_mode=="0" or (running_mode=="1" and var_num_int<=15)):
            print "Problem " + p["promb_num"]
            time_start = time.time() * 1000000
            current_wff = p["clauses"]
            assign_list = ["-1"]*int(p["var_num"])
            stack = []
            new_var_name = current_wff[0][0]
            new_var_name = str(abs(int(new_var_name)))
            literal_dic = {
               "var_name": new_var_name,
                "assign": "0",
                "pre_wff": deepcopy(current_wff),
            }
            stack.append(literal_dic)
            update_assign(assign_list, deepcopy(stack),True)

            finished = False
            found = False
            while (not finished):
                gen_new_wff(current_wff, assign_list)

                if ("Failed" in current_wff):
                    #This assignment fails, generate new stack by recursion, reset wff
                    stack = gen_new_stack(stack)
                    if (len(stack) > 0):
                        current_wff = stack[len(stack)-1]["pre_wff"]
                        update_assign(assign_list, deepcopy(stack),True)
                elif(len(current_wff) == 0):
                    # All clauses are satisfied. We found love!!!!!!!
                    finished = True
                    found = True
                else:
                    #This assignment is ok, add new variable and do continue
                    if ("-1" in assign_list):
                        new_var_name = assign_list.index("-1") +1
                        new_var_name = str(new_var_name)
                        literal_dic = {
                           "var_name": new_var_name,
                            "assign": "0",
                            "pre_wff": deepcopy(current_wff),
                        }
                        stack.append(literal_dic) 
                        update_assign(assign_list, deepcopy(stack), False)
                    
                if (len(stack)==0):
                    #The stack is empty, game over
                    finished = True

            time_taken = time.time()*1000000 - time_start
            out_assign = []
            prediction = "U"
            pre_match = "0"
            if (found):
                prediction = "S"
                s_wff += 1
                out_assign = assign_list
                for node in stack:
                    index = int(node["var_name"])-1
            else:
                u_wff += 1
            if (p["test_char"]!="?"):
                a_wff += 1
                if(p["test_char"]==prediction):
                    pre_match = "1"
                    c_wff += 1
                else:
                    pre_match = "-1"

            output_info ={
                "promb_num": p["promb_num"],
                "var_num" : p["var_num"],
                "clause_num" : p["clause_num"],
                "max_num_literal": p["max_num_literal"],
                "total_num_li": p["total_num_li"],
                "prediction": prediction,
                "pre_match": pre_match,
                "time_taken": time_taken,
                "assignment": out_assign,
            }
            gen_output_row(output_info)
    #end of all problem
    last_line = {
        "input_file": sys.argv[1].replace(".cnf",""),
        "team_name": "satTeam",
        "total_wff": len(problem_list),
        "s_wff" : s_wff,
        "u_wff" : u_wff,
        "a_wff" : a_wff,
        "c_wff" : c_wff,
    }
    gen_last_row(last_line)


def update_assign(assign_list, stack,init):
    if (init == True):
        for i in range(len(assign_list)):
            assign_list[i] = "-1"
    for literal_dic in stack:
        index = int(literal_dic["var_name"]) -1 
        assign_list[index] = literal_dic["assign"]
    


# direct amend on current_wff ["Failed"] if there is one clause that is unsatifiable  [] enpty list if all pass
def gen_new_wff(current_wff, assign_list):   
    working_wff = deepcopy(current_wff)
    for clause in working_wff:
        gen_new_clause(clause, assign_list,current_wff)

        if (current_wff==["Failed"]):
            break;
    
# this function only work for clause that contains one literal
def force_assign(clause, assign_list,current_wff):
    n_clause = deepcopy(clause)
    literal = n_clause[0]

    neg = ("-" in literal)
    if (neg):
        new_assign = "0"
    else:
        new_assign = "1"
    index = abs(int(literal)) -1

    if (assign_list[index] =="-1"):
        assign_list[index] = new_assign
        current_wff.remove(clause)
    elif(assign_list[index]==new_assign):
        current_wff.remove(clause) 
    else:
        current_wff[:] = ["Failed"]
        


# return empty list if fail, return ["true"] if success, which should not be append to the new wff
def gen_new_clause(clause, assign_list,current_wff):
    for literal in clause:
        if (len(current_wff)==0):
            break
        elif (len(clause) == 1):
            force_assign(clause, assign_list,current_wff)
        else:
            index = abs(int(literal))-1
            if((assign_list[index]=="1" and "-" not in literal) or (assign_list[index]=="0" and "-" in literal)):
                if (clause in current_wff):
                    current_wff.remove(clause)
                    break  #jump to next clause if we remove this one 
            elif ((assign_list[index]=="1" and "-" in literal) or (assign_list[index]=="0" and "-" not in literal)):
                c_location = current_wff.index(clause)
                current_wff[c_location].remove(literal)
                clause.remove(literal)
                force_assign(clause, assign_list,current_wff)

def gen_new_stack(stack):
    if (len(stack)<=0):
        return []
    else:
        top_index = len(stack)-1
        top = stack[top_index]
        if (top["assign"]=="0"):
            stack[top_index]["assign"] = "1"
            return stack
        else:
            stack.pop()
            return gen_new_stack(deepcopy(stack))

def gen_output_row(output_info):
    global output_file
    output_file.write(output_info["promb_num"] + ",")
    output_file.write(output_info["var_num"] + ",")
    output_file.write(output_info["clause_num"] + ",")
    output_file.write(output_info["max_num_literal"] + ",")
    output_file.write(str(output_info["total_num_li"]) + ",")
    output_file.write(output_info["prediction"] + ",")
    output_file.write(output_info["pre_match"] + ",")
    output_file.write(str(output_info["time_taken"]) + ",")
    for i in output_info["assignment"] :
        output_file.write(str(i) + ",")
    output_file.write("\n")

def gen_last_row(last_line):
    global output_file
    output_file.write(last_line["input_file"] + ",")
    output_file.write(last_line["team_name"] + ",")
    output_file.write(str(last_line["total_wff"])+ ",")
    output_file.write(str(last_line["s_wff"]) + ",")
    output_file.write(str(last_line["u_wff"]) + ",")
    output_file.write(str(last_line["a_wff"]) + ",")
    output_file.write(str(last_line["c_wff"]) )


promb_counter = 0
problem_list = []
problem_info = {"clauses": []}
file_name = sys.argv[1]
running_mode = "0"
if (len(sys.argv) >2):
    running_mode = sys.argv[2]
test_file = open(file_name, "r")

try:
    for s in test_file:
        read_wff(s)
except:
    print "Cannot read the file"
finally:
    test_file.close()
    output_file = open(sys.argv[1].replace(".cnf",".csv"), "w")

solving_problem(running_mode)
output_file.close()