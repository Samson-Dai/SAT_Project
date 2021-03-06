#!/usr/bin/python
import sys
import time


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
    
    s_wff = 0
    u_wff = 0
    a_wff = 0
    c_wff = 0

    for p in problem_list:
        var_num_int = int(p["var_num"])
        if (running_mode=="0" or (running_mode=="1" and var_num_int<=8 )):
            #print "For promblem" + p["promb_num"]
            time_start = time.time() * 1000000
            
            init_str = bin(0)[2:].zfill(var_num_int)
            found = False
            
            while (found==False and init_str!="final"):
                found = verify(p["clauses"],init_str)
                init_str = gen_next_assign(init_str, var_num_int);
           
            time_taken = time.time()*1000000 - time_start
            assgn_list = []
            prediction = "U"
            pre_match = "0"
            if (found):
                prediction = "S"
                s_wff += 1
                assgn_list = list(init_str)
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
                "assignment": assgn_list,
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


def verify(wff, assignment):
    for clause in wff:
        verified = False
        for value in clause:
            v_int = int(value)
            v_abs = abs(v_int)
            ass_value = int(assignment[v_abs - 1])
            if (v_int < 0):
                ass_value = 1 - ass_value
            if (ass_value == 1):
                verified = True
                break
        if (verified == False):
            return False
    return True


# use binary string to represent the assignment
def gen_next_assign(bin_str, var_num_int):
    if ("0" not in bin_str):
        return "final"
    else:
        int_str = int(bin_str, 2)
        int_str += 1
        new_str = bin(int_str)[2:].zfill(var_num_int)
        return new_str


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
    output_file_title = sys.argv[1].replace(".cnf",".csv")
    output_file_title = "brute_"+output_file_title 
    output_file = open(output_file_title, "w")

solving_problem(running_mode)
output_file.close()
