from copy import deepcopy


def update_assign(assign_list, literal_dic):
    index = int(literal_dic["var_name"]) -1 
    assign_list[index] = literal_dic["assign"]
    update_two (assign_list)

def update_two(assign_list):
	assign_list.remove("-1")

assign_list = ["-1"]*int("5")
stack = []
new_var_name = "-4"          #current_wff[0][0]
new_var_name = str(abs(int(new_var_name)))
literal_dic = {
   "var_name": new_var_name,
    "assign": "0",
    "pre_wff": [1,2,3,4],
}
stack.append(literal_dic)

print "Original assign_list" + str(assign_list)

update_assign(assign_list,deepcopy(literal_dic))

print "After changes " + str(assign_list)




