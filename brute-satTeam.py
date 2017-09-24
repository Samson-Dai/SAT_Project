import sys

promb_counter = 0
problem_list = []
problem_info = {"clauses":[]}

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
        problem_list.append(promb_counter)
        promb_counter += 1
    elif (line[0] == "p"):
        line_list = line.split()
        problem_info["var_num"] = line_list[2]
        problem_info["clause_num"] = line_list[3]
    else:
        line_list = line.split(',')
        a_clause = []
        for item in line_list[0: len(line_list)-1]:
            a_clause.append(item)
        problem_info["clauses"].append(a_clause)

def gen_assignment(power,result):
    if (power==0):
        print result
        return
    else:
        new1 = result[:]  #need to creat new variable
        new1.append(1)
        new0 = result[:]
        new0.append(0)
        gen_assignment(power-1, new0)
        gen_assignment(power-1, new1)


print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: ", str(sys.argv)
print "The file name", sys.argv[1]

file_name = sys.argv[1]
test_file = open(file_name, "r")


try:
    for s in test_file:
        read_wff(s)
except:
    print "Cannot read the file"
finally:
    test_file.close()


#print problem_list[0]
#print gen_assignment(4,[])
gen_assignment(4,[])


        
