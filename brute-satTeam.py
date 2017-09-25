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
                found = False
                
                while (found==False and init_str!="final"):
                    found = verify(p["clauses"],init_str)
                    init_str = gen_next_assign(init_str, var_num_int);
                
                print "Question No " + p["promb_num"]
                print "Correct Answer is "+ p["test_char"]
                if (found):
                    print "Our Answer is S\n\n"
                else:
                    print "Our Answer is U\n\n"
                
                # use gen_next_assign() and verify() functions to verify clsuses
                #print init_str

    elif(running_mode =='0'):
        print "not"

def verify (wff,assignment):
    for clause in wff:
        verified = False
        for value in clause:
            v_int = int(value)
            v_abs = abs(v_int)
            ass_value = int (assignment[v_abs-1])
            if (v_int<0):
                ass_value = 1-ass_value
            if (ass_value == 1):
                verified = True
                break
        if (verified == False):
            return False
    return True



#use binary string to represent the assignment
def gen_next_assign(bin_str, var_num_int):
    if ("0" not in bin_str):
        return "final"
    else:
        int_str = int(bin_str,2)
        int_str += 1 
        new_str = bin(int_str)[2:].zfill(var_num_int)
        return new_str



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
    
