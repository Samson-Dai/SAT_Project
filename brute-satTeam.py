import sys

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
        for item in line_list[0: len(line_list)-1]:
            a_clause.append(item)
        problem_info["clauses"].append(a_clause)

def solving_problem(running_mode):
    global promb_counter, problem_list, problem_info
    #running_mode is for test purpose, required by the description
    if (running_mode=='1'):
        for p in problem_list:
            #print "index is " + str(problem_list.index(p))
            #print p 
            var_num_int = int(p["var_num"])
            if(var_num_int<=8):
                init_str = bin(0)[2:].zfill(var_num_int)
                # use gen_next_assign() and verify() functions to verify clsuses
                print init_str

    elif(running_mode =='0'):
        print "not"



#use binary string to represent the assignment
def gen_next_assign(bin_str):
    #transform bin_str to decimal numbers, add 1 and transfer back
    # should stop if we come to all 1 , like "1111" for v=4
    print "hi"



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

print "This is the name of the script: ", sys.argv[0]
print "The arguments are: ", str(sys.argv)
print "The file name", sys.argv[1]

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


#print gen_assignment(4,[])
solving_problem(running_mode)
    
