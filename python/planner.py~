import copy
world=[]
world_objects={}
count_down=0
 
import sys
sys.setrecursionlimit(10000)
def isFloor(position):
      if(isinstance(position,list) and not isinstance(position[0],int) and len(position)==len(world)):
            for i in position:
                  if(i[1]!=0):
                        return False
            return True
      else:
            return False 
def index_of_object(state,obj):
      for col in state:
            for row in col:
                  if(row==obj):
                        return (state.index(col),col.index(row))

def get_sub_path_set(best_path,goal,closed_list):
    import physical_law
    path_set=[]
    leaf=best_path[-1]
     
    for i in range(0,len(leaf)):
        if(len(leaf[i])==0):
            continue
        for j in range(0,len(leaf)):
            if(i==j):
                continue
            available_position=(j,len(leaf[j]))
            
            col=i
            row=len(leaf[i])-1
            
            if(physical_law.obey_physical_law_with_quantifier_on(copy.deepcopy(leaf),world_objects,(col,row),available_position)):
                 
                state=copy.deepcopy(leaf)
                obj=state[col].pop(row)
                state[j].append(obj)
                #check cycle
                if(closed_list.count(state)>0):
                      continue
                else:
                      closed_list.append(state)
                
                new_path=copy.deepcopy(best_path)
                #store command in path array 
                new_path.append("pick "+str(col))
                new_path.append("drop "+str(j))

                new_path.append(state)
                path_set.append(new_path)
    
    return path_set
def heuristical_take(leaf,goal):
      index=index_of_object(leaf,goal.get("object"))

      col=index[0]
      row=index[1]

      return abs(len(leaf[col])-row)
def heuristical_under(leaf,goal):
      index=index_of_object(leaf,goal.get("object"))
      col_1=index[0]
      row_1=index[1]

      target_position=goal["target_position"][0]
      col_2=target_position[0]
      row_2=target_position[1]

      h=0
      if(col_2==col_1 and row_2==row_1):
          
            for p in world[col_2][row_2:]:
                  position_in_world=index_of_object(world,p)
                  position_in_leaf=index_of_object(leaf,p)
                   
                  if(position_in_leaf==(position_in_world[0],position_in_world[1]+1)):
                        continue
                  elif(position_in_leaf[0]==position_in_world[0]):
                        h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1])
                  else:
                        if(position_in_world[1]+1>=len(leaf[position_in_world[0]])):
                              h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1])
                        else:
                              h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1])+abs(len(leaf[position_in_world[0]])-position_in_world[1]-1)
                          
       
      else:
            h+=(abs(len(leaf[col_1])-row_1)+2*(abs(len(leaf[col_2])-row_2)))    
            for p in world[col_2][len(leaf[col_2]):]:
                  position_in_leaf=index_of_object(leaf,p)
                  h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1])
                   
      return h 
def heuristical_on(leaf,goal):
      index=index_of_object(leaf,goal.get("object"))
      col_1=index[0]
      row_1=index[1]

      target_position=goal["target_position"][0]
      col_2=target_position[0]
      row_2=target_position[1]

      return abs(len(leaf[col_1])-row_1)+abs(len(leaf[col_2])-row_2) 
     
def heuristical_floor(leaf,goal):
      index=index_of_object(leaf,goal.get("object"))
      col_1=index[0]
      row_1=index[1]
            
      for col in leaf:
            if(len(col)==0):
                  return len(leaf[col_1])-row_1
      length=[]
      
      for col in leaf:
            length.append(len(col))
      length.sort() 
 
      return abs(len(leaf[col_1])-row_1)+length[0]
def heuristical_with_quantifier_all(path,goal):
      h=0
      leaf=path[-1]
      original_position_copy=copy.deepcopy(goal.get("original_position"))
      target_position_copy=copy.deepcopy(goal.get("target_position"))
        
      if(goal.get("preposition").startswith("on") or goal.get("preposition").startswith("in")):
            flag=False
            for tar in target_position_copy:
                  if(not tar[1]==0):
                        flag=True
            if(not flag):
                  
                  for o in range(0,len(original_position_copy)):
                        ori=index_of_object(leaf,world[original_position_copy[o][0]][original_position_copy[o][1]])
                         
                        if(ori[0]==target_position_copy[o][0] and ori[1]==target_position_copy[o][1]):
                               
                              continue
                        else:
                              h+=abs(len(leaf[ori[0]])-ori[1])+abs(len(leaf[target_position_copy[o][0]])-target_position_copy[o][1])
            else:
                  
                  for o in range(0,len(original_position_copy)):
                        ori=index_of_object(leaf,world[original_position_copy[o][0]][original_position_copy[o][1]])
                        tar=index_of_object(leaf,world[target_position_copy[o][0]][target_position_copy[o][1]-1])     
                          
                        if(ori[0]==tar[0] and ori[1]==tar[1]+1):
                             
                              continue
                        else:
                               
                              h+=abs(len(leaf[ori[0]])-ori[1])+abs(len(leaf[tar[0]])-(tar[1]+1))
                        
      elif(goal.get("preposition")=="under"):
              
             tar_col=[]
             for o  in range(0,len(original_position_copy)):
                    position_in_target_state=index_of_object(goal.get("target_world"),world[original_position_copy[o][0]][original_position_copy[o][1]]) 
                    if(position_in_target_state[0] not in tar_col):
                          tar_col.append(position_in_target_state[0])
                     
             for t in tar_col:
                   col=goal.get("target_world")[t]
                   for obj in col:
                         position_in_leaf=index_of_object(leaf,obj)
                         position_in_target_world=index_of_object(goal.get("target_world"),obj)
                         if(position_in_leaf==position_in_target_world):
                               continue
                         else:
                               position_in_world=index_of_object(world,obj)
                               if([i for  i in position_in_world] in goal.get("original_position")):
                                     h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1])+abs(len(leaf[position_in_target_world[0]])-position_in_target_world[1])
                                     for obj in col[col.index(obj)+1:]:
                                           position_in_world=index_of_object(world,obj)
                                           if([i for  i in position_in_world] in goal.get("original_position")):
                                                 position_in_leaf=index_of_object(leaf,obj)
                                                 h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1]) 
                                           else:
                                                 h+=1
                                     break
                               else:
                                     for obj in col[col.index(obj):]:
                                           position_in_leaf=index_of_object(leaf,obj)
                                           h+=abs(len(leaf[position_in_leaf[0]])-position_in_leaf[1]) 
  
             
      elif(goal.get("preposition").find("left")>=0):
             target_object=goal.get("target_objects") 
             
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_object:
                       target_position=index_of_object(world,tar)
                       if(ori_in_new_world[0]<target_position[0] ):
                              flag=True
                              break
                  if(not flag):      
                       h+=abs(len(leaf[ori_in_new_world[0]])-ori_in_new_world[1])             
      elif(goal.get("preposition").find("right")>=0):
             target_object=goal.get("target_objects") 
             
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_object:
                       target_position=index_of_object(world,tar)
                       if(ori_in_new_world[0]>target_position[0] ):
                              flag=True
                              break
                  if(not flag):      
                       h+=abs(len(leaf[ori_in_new_world[0]])-ori_in_new_world[1])
      elif(goal.get("preposition").find("above")>=0):
             
             target_object=goal.get("target_objects") 
             
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_object:
                       target_position=index_of_object(leaf,tar)
                       if(ori_in_new_world[0]==target_position[0] and ori_in_new_world[1]>target_position[1]):
                              flag=True
                              break
                  if(not flag):      
                       h+=abs(len(leaf[ori_in_new_world[0]])-ori_in_new_world[1])
      elif(goal.get("preposition").find("beside")>=0):
             target_object=goal.get("target_objects") 
             
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_object:
                       target_position=index_of_object(leaf,tar)
                       if(abs(ori_in_new_world[0]-target_position[0])==1):
                              flag=True
                              break
                  if(not flag):      
                       h+=abs(len(leaf[ori_in_new_world[0]])-ori_in_new_world[1])
             
      return h
def heuristical(path,goal):
    leaf=path[-1]
    index=index_of_object(leaf,goal.get("object"))
    col_1=index[0]
    row_1=index[1]
    
    #when there are several targets to be moved            
    if(achieve_goal(path,goal)):           
          return 0
    if(goal.has_key("target_position") and isFloor(goal["target_position"])):
          return heuristical_floor(leaf,goal)
    else:
          if(goal.has_key("target_position")):
                if(goal.get("preposition")=="under"):
                      return heuristical_under(leaf,goal)
                else:
                      return heuristical_on(leaf,goal)
          else:
                return heuristical_take(leaf,goal)
def get_cost(path):
      return len(path)%3==0 and len(path)/3 or len(path)/3+1
def get_the_best_path(frontier,goal):
     
    least=10000
    least_cost=10000
    best_path=[] 
    for p in frontier:
        
        cost=get_cost(p) 
        if(goal.get("quantifier")=="all"):
              h=heuristical_with_quantifier_all(p,goal)
               
        else:
              h=heuristical(p,goal)
            
        if(cost+h<least):
            least=cost+h
            best_path=p
            least_cost=cost
        elif(cost+h==least):
            if(cost>least_cost):
                least=cost+h
                best_path=p
                least_cost=cost
      
    return best_path
def achieve_goal_with_preposition_under(leaf,goal):
      target_position=goal["target_position"][0]
      col=target_position[0]
      row=target_position[1]
      if(len(leaf[col])-1>=row and leaf[col][row]==goal["object"]):
            if(goal.get("original_position")[0][0]!=col and leaf[col][row+1:]==world[col][row:]):
                  return True
            elif(goal.get("original_position")[0][0]==col):
                  if(leaf[col][row+1:]==world[col][row:goal.get("original_position")[0][1]]):
                        return True
                  else:
                        return False
            else:
                  return False
                              
      else:
            return False
      
def achieve_goal_with_target_floor(leaf,goal):
      
      for col in leaf:
            if(len(col)>0 and col[0]==goal["object"]):
                  return True
      return False

def achieve_goal_with_quantifier_all(leaf,goal):
      
      original_position_copy=copy.deepcopy(goal.get("original_position"))
      if(goal.get("preposition").startswith("in") or goal.get("preposition").startswith("on")): 
            target_position_copy=copy.deepcopy(goal.get("target_position"))
             
            
            flag=True
     
            for position in original_position_copy:
                  goal_copy=copy.deepcopy(goal)
                  goal_copy["object"]=world[position[0]][position[1]]

                  flag2=False
                  for t in target_position_copy:
                        goal_copy["target_position"]=[t]
                        if(achieve_goal([leaf],goal_copy)):
                              flag2=True
                              break
                  if(flag2):
                        continue
                  else:
                        flag=False
                        break
      
            return flag
      elif(goal.get("preposition")=="under"):
            tar_col=[]
            for o  in range(0,len(original_position_copy)):
                  position_in_target_state=index_of_object(goal.get("target_world"),world[original_position_copy[o][0]][original_position_copy[o][1]]) 
                  if(position_in_target_state[0] not in tar_col):
                        tar_col.append(position_in_target_state[0])
            flag=True
            for t in tar_col: 
                  if(not leaf[t]==goal.get("target_world")[t]):
                        flag=False
            return flag
      elif(goal.get("preposition").find("left")>=0):
             target_position=goal.get("target_position") 
              
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_position: 
                       if(ori_in_new_world[0]==tar[0]):
                              flag=True
                              break
                  if(not flag):      
                       return False
             
              
             return True 
      elif(goal.get("preposition").find("right")>=0):
             target_position=goal.get("target_position") 
             
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_position: 
                       if(ori_in_new_world[0]==tar[0]):
                              flag=True
                              break
                  if(not flag):      
                       return False
             return True 
      elif(goal.get("preposition").find("above")>=0):
             target_object=goal.get("target_objects") 
             
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_object:
                       target_position=index_of_object(leaf,tar)
                       if(ori_in_new_world[0]==target_position[0] and ori_in_new_world[1]>target_position[1]):
                              flag=True
                              break
                  if(not flag):      
                       return False
             return True 
      elif(goal.get("preposition").find("beside")>=0):
             target_position=goal.get("target_position") 
              
             for ori in goal.get("original_position"):
                  flag=False
                  ori_in_new_world=index_of_object(leaf,world[ori[0]][ori[1]])
                  for tar in target_position:
                        if(ori_in_new_world[0]==tar[0]):
                              flag=True
                              break
                  if(not flag):      
                       return False
             return True 


def achieve_goal_with_preposition_left_right_beside(leaf,goal):
      obj=goal.get("object")
      ori_in_new_world=index_of_object(leaf,obj)
      target_position=goal.get("target_position")
      for tar in target_position:
            if(tar[0]==ori_in_new_world[0]):
               return True
      return False                                     
def achieve_goal(path,goal):
      leaf=path[-1]
      #if(goal.get("quantifier")=="all"):
            #return achieve_goal_with_quantifier_all(leaf,goal)
      if(goal.has_key("target_position")):
            if(isFloor(goal["target_position"])):
                return achieve_goal_with_target_floor(leaf,goal)
            elif(goal.get("preposition")=="under"):
                return achieve_goal_with_preposition_under(leaf,goal)
            elif(goal.get("preposition").find("left")>=0 or goal.get("preposition").find("right")>=0 or goal.get("preposition").find("beside")>=0):
                return achieve_goal_with_preposition_left_right_beside(leaf,goal)
             
            else:
                   
                  target_position=goal["target_position"][0]
                   
                  if(target_position[1]!=0):
                          
                        target_position=index_of_object(leaf,world[target_position[0]][target_position[1]-1])
                        target_position=[target_position[0],target_position[1]+1]
                  col=target_position[0]
                  row=target_position[1]
                   
                  if(len(leaf[col])-1>=row and leaf[col][row]==goal["object"]):
                         return True
                   
      elif(goal.get("action")=="take"):
            target_position=goal["original_position"][0]
            col=target_position[0]
            row=target_position[1]
            if(len(leaf[col])==row+1):
                  path.append("pick "+str(col))
                  return True
                  
             
      return False
def put_down_holding(frontier,closed_list,goal):
    import physical_law
    path_set=[]
    leaf=frontier[0][0]
    obj=goal.get("object")
    for i in range(0,len(leaf)):
            available_position=(i,len(leaf[i]))
            
            col=i
            row=len(leaf[i])-1
              
            if(physical_law.obey_physical_law_with_quantifier_on(copy.deepcopy(leaf),world_objects,obj,available_position)):
                 
                state=copy.deepcopy(leaf)
                state[i].append(obj)
                 
                #check cycle
                if(closed_list.count(state)>0):
                      continue
                else:
                      closed_list.append(state)
                
                new_path=copy.deepcopy(frontier[0])
                #store command in path array 
                new_path.append("drop "+str(i))

                new_path.append(state)
                path_set.append(new_path)
    
    return path_set
def get_least_cost_path(frontier,goal):
      least=10000
      least_path=None
      for p in frontier:
            cost=get_cost(p)
            if(least>cost):
                  least=cost
                  least_path=p
      return p
 
             
 
def solve(frontier,closed_list,goal):
    global count_down
    count_down+=1
    if(count_down>3000):
         count_down=0
         return "Unsolvable task"
    best_path=get_the_best_path(frontier,goal)
    frontier.remove(best_path)
         
    sub_path_set=get_sub_path_set(best_path,goal,closed_list)

    if(len(sub_path_set)==0 and len(frontier)==0):
          return "Unsolvable task"
     
    if(goal.get("quantifier")=="all"):
          for path in sub_path_set:
                if(achieve_goal_with_quantifier_all(path[-1],goal)):
                      
                      return path
          for path in sub_path_set:
                frontier.append(path)
          return solve(frontier,closed_list,goal)
     
    else:
          for path in sub_path_set:
                if(achieve_goal(path,goal)):
                      return path
          for path in sub_path_set:
                      frontier.append(path)
          return  solve(frontier,closed_list,goal)
    
def get_command(path):
      if(not isinstance(path,list)):
            return path
       
      command=[]
       
      plan=[]
      for p in path:
            if(isinstance(p,str)):
                  command.append(p)

      for i in range(0,len(command)):
              plan.append("I "+command[i])
              plan.append(command[i])
              
      return plan
def solve_multiple_target_position(frontier,closed_list,goal):
       
       if(isFloor(goal.get("target_position")) or goal.get("quantifier")=="all"):
             return solve(frontier,closed_list,goal)
       for p in goal.get("target_position"):
                  goal_copy=copy.deepcopy(goal)
                  goal_copy["target_position"]=[p]
                  response=solve(frontier,closed_list,goal_copy)
                
                  if(isinstance(response,list)):
                        return response
                  elif(goal.get("target_position").index(p)==len(goal.get("target_position"))-1):
                        return response
                  else:
                            path=[]
                            frontier=[]
                            closed_list=[]
                            path.append(copy.deepcopy(world))
                            frontier.append(path)
                            closed_list.append(copy.deepcopy(world))
def precessing_of_all_quantifier_goal(goal):
      import physical_law
      
      target_position_copy=copy.deepcopy(goal.get("target_position"))
      for t in target_position_copy:
            flag=False
            goal_copy=copy.deepcopy(goal)
            for ori in goal.get("original_position"):
                  goal_copy["object"]=world[ori[0]][ori[1]]
                  goal_copy["target_position"]=[t]
                  if(physical_law.obey_physical_law(world,world_objects,goal_copy)):
                        flag=True
                        break
            if(not flag):
                  goal.get("target_position").remove(t)
def get_path_with_least_heuristic_value(csp_graph,current_path,least_path):
      flag=False
      for node in csp_graph:
            if(isinstance(node[1],list)):
                  if(node[2]+current_path[1]<least_path[1]):
                        current_path_copy=copy.deepcopy(current_path)
                        current_path_copy[0].append(node[0])
                        
                        current_path_copy[1]=current_path_copy[1]+node[2]
                        children=get_path_with_least_heuristic_value(node[1],current_path_copy,least_path)
                        if(len(children)==2):
                              flag=True
                              least_path=children
                               
                       
            else:
                  
                  if(node[1]+current_path[1]<least_path[1]):

                        current_path_copy=copy.deepcopy(current_path)
                        current_path_copy[0].append(node[0])
                        
                        current_path_copy[1]=current_path_copy[1]+node[1] 
                         
                        least_path=current_path_copy
                        flag=True 
                    
      if(flag):
            return least_path
      else:
            return []
def set_the_least_heuristical_assignment(csp_graph,goal): 
            
      path=get_path_with_least_heuristic_value(csp_graph,[[],0],[[],10000])
      goal["target_position"]=path[0]
def generate_csp_graph(variable_and_domain,used_list,original_position,index):
       
      if(not variable_and_domain):
             
            return []
      variable=str(original_position[index])
      nodes=[] 
      for value in variable_and_domain.get(variable):
             
            if(used_list.count(value)>0):
                  continue
            else:
                  ori=original_position[index]
                  if(ori==value):
                        heuristical=0
                  else:
                        heuristical=abs(len(world[ori[0]])-ori[1])+abs(len(world[value[0]])-value[1])
                  used_list.append(value)
                  vd_copy=copy.deepcopy(variable_and_domain)
                  del vd_copy[variable]
                  children=generate_csp_graph(vd_copy,used_list,original_position,index+1)
                   
                  if(children==[]):
                        nodes.append([value,heuristical])
                  elif(children==False):
                        
                        continue
                  else:
                         
                        nodes.append([value,children,heuristical])
                  used_list.remove(value)
      if(nodes==[]):
            return False
      else:
            return nodes
def is_possible_to_plan_all_objects(goal):
      import physical_law
      
      target_position_copy=copy.deepcopy(goal.get("target_position"))
      original_position_copy=copy.deepcopy(goal.get("original_position"))
      variable_and_domain={}
      for ori in original_position_copy:
            domain=[]
            for t in target_position_copy:
                  goal_copy=copy.deepcopy(goal)
                  goal_copy["object"]=world[ori[0]][ori[1]]
                  goal_copy["target_position"]=[t]
                  if(physical_law.obey_physical_law(world,world_objects,goal_copy)):
                        domain.append(t)

            variable_and_domain[str(ori)]=domain
      used_list=[] 
      csp_graph=generate_csp_graph(variable_and_domain,used_list,original_position_copy,0)
       
      if(csp_graph==False):
            return False
      else:
            set_the_least_heuristical_assignment(csp_graph,goal)
            return True
def execu_command(command,state):
      obj=""
      for i in range(0,len(command),2):
             
            if((i%4)!=0):
                  
                  state[int(command[i][-1])].append(obj)
            else:
                  
                  obj=state[int(command[i][-1])].pop()
      return state
 
def sort_from_easy_to_hard(position,world):
      tar=[]
     
      for p in position:
            tar.append([p,len(world[p[0]])-p[1]])
       
      tar.sort(key=lambda x:x[1])
      return [i[0] for i in tar]
def is_possible_to_plan_all_objects_with_preposition_under(goal):
      original_position=goal.get("original_position")
      #delete the replicate one  
      target=[]
      for t in goal.get("target_position"):
            if(t not in target and t[0] not in [i[0] for i in target]):
                  target.append(t)
      goal["target_position"]=target  
      flag=False
      if(len(goal.get("target_position"))>=1):
            global world
            
            world_copy=copy.deepcopy(world)
            
            for ori in original_position:
                  goal_copy=copy.deepcopy(goal)
                  goal_copy["object"]=world_copy[ori[0]][ori[1]]
                  goal_copy["quantifier"]="the"

                  tar=[] 
                  for t in goal.get("target_position"):
                        
                        position_in_new_world=index_of_object(world,world_copy[t[0]][t[1]])
                        
                        tar.extend([[position_in_new_world[0],i] for i in range(0,position_in_new_world[1]+1)])
                  
                  goal_copy["target_position"]=tar       
                  tar=[]
                  for t in goal_copy.get("target_position"):
                        tar.append([t,len(world_copy[t[0]])-t[1]])
                  tar.sort(key=lambda x:x[1])
                   
                  goal_copy["target_position"]=[i[0] for i in tar]
                  
                  if(ori in goal_copy.get("target_position")): 
                        continue
                   
                  response=move_plan(goal_copy)
                  
                  if(isinstance(response,str)):
                        
                        return False
                  else:
                        flag=True
                         
                        world=execu_command(response,world)
            if(not flag):
                  return "Nothing needed to be done"
            t=[]
            for ori in original_position:
                  obj=index_of_object(world,world_copy[ori[0]][ori[1]])
                  t.append([ori,[obj[0],obj[1]]])
                  
                  
            t.sort(key=lambda x:x[1][1])
            goal["original_position"]=[i[0] for i in t] 
            goal["target_position"]=[i[1] for i in t]
            
            goal["target_world"]=world
  
            world=world_copy
             
            return True
      else:
            return False
def is_possible_to_plan_all_objects_with_preposition_above(goal):
      import physical_law
      if(goal.get("target_position")==[]):
               
              return False
      return True
def is_possible_to_plan_all_objects_with_preposition_left_and_right(goal):
      if(goal.get("target_position")==[]):
            return (False,"Physical law is not allowed") 
       
      objects=goal.get("target_objects")
      for o in objects:
           position=index_of_object(world,o)
           if([i for i in position] in goal.get("original_position")):
                   return(False,"How could you lift up yourself? you can not put an object to the left or right of itself~!")
      
       
      return (True,"")
      
def is_possible_to_plan_all_objects_with_preposition_beside(goal):
      if(goal.get("target_position")==[]):
            return (False,"Physical law is not allowed") 
      else:
            return (True,"")
      
def move_plan(goal):
      
      if(goal.get("quantifier")=="all"):
              
            if(goal.get("preposition").startswith("on") or goal.get("preposition").startswith("in")):
                  precessing_of_all_quantifier_goal(goal)
                  
                  if(not goal.get("target_position") or len(goal.get("target_position")) < len(goal.get("original_position"))):
                        return "physical law is not allowed"

                  if(not is_possible_to_plan_all_objects(goal)):
                        return "physical law is not allowed"
                   
            elif(goal.get("preposition")=="under"):
                  response=is_possible_to_plan_all_objects_with_preposition_under(goal)
                  if(isinstance(response,str)):
                        return response
                  if(not response):
                        return "physical law is not allowed"
            elif(goal.get("preposition")=="above"):
                  response=is_possible_to_plan_all_objects_with_preposition_above(goal)
                   
                  if(not response):
                        return "physical law is not allowed"
            elif(goal.get("preposition").find("left")>=0 or goal.get("preposition").find("right")>=0):
                  response=is_possible_to_plan_all_objects_with_preposition_left_and_right(goal)
                  if(not response[0]):
                        return response[1]
            elif(goal.get("preposition").find("beside")>=0):
                  response=is_possible_to_plan_all_objects_with_preposition_beside(goal)
                  if(not response[0]):
                        return response[1]
                  
      else:
            if(not goal.has_key("object")):
                  position=goal["original_position"][0]
                  goal["object"]=world[position[0]][position[1]]
                   
            #check whether physical law is obeyed between
          
            import physical_law
            if(not physical_law.obey_physical_law(world,world_objects,goal)):
                  return "physical law is not allowed"
     
      path=[]
      frontier=[]
      closed_list=[]
      
      path.append(copy.deepcopy(world))
      frontier.append(path)
      closed_list.append(copy.deepcopy(world))
       
      #since we asssume that, there could be a lot of target_positions, 
      return get_command(solve_multiple_target_position(frontier,closed_list,goal)) 
            
def take_plan(goal):
       
      position=goal["original_position"][0]
      goal["object"]=world[position[0]][position[1]]

      path=[]
      frontier=[]
      closed_list=[]
      
      path.append(copy.deepcopy(world))
      frontier.append(path)
      closed_list.append(copy.deepcopy(world))
      if(achieve_goal(path,goal)):
            path_to_goal=path
      else:
            path_to_goal=solve(frontier,closed_list,goal)
            
      return get_command(path_to_goal)


def put_plan(goal,holding):
  
     goal["object"]=holding
     path=[] 
     frontier=[]
     closed_list=[]
     #check physical law
     import physical_law
     if(not physical_law.obey_physical_law(world,world_objects,goal)):
           return "physical law is not allowed"
     path.append(copy.deepcopy(world))
     frontier.append(path)
     closed_list.append(copy.deepcopy(world))

     path_set=put_down_holding(frontier,closed_list,goal)
     frontier.remove(path)
     for path in path_set:
           if(achieve_goal(path,goal)):
                 return get_command(path)
            
     for path in path_set:
           frontier.append(path)
      

         #since we asssume that, there could be a lot of target_positions, 
     return get_command(solve_multiple_target_position(frontier,closed_list,goal)) 

def plan(goal, world_parameter, holding, objects):
     
      global world
      global world_objects
 
      world=world_parameter
      world_objects=objects
      if(goal.has_key("target_position")):
            if(not goal.get("target_position")):
                 return "physical law is not allowed" 
      if(holding!=None and goal.get("action")!="put"):
            if(goal.get("action")=="take" or not goal.get("original_position")[0]==[-2,-2] or goal.get("quantifier")=="all"):
                  return "you are holding some stuff"
      command=[]
      #we set the target_position of these preposition as [x,-1],so you need to do transformation
      if(goal.has_key("target_position") and (goal.get("preposition")=="beside" or goal.get("preposition").find("left")>=0 or goal.get("preposition").find("right")>=0)):
            
            target=[]
            be_col=goal.get("target_position")
            #del the duplicate element 
            be_col_copy=copy.deepcopy(be_col)
            for col in be_col_copy:
                  if(be_col.count(col)>1):
                        be_col.remove(col)
                  
            for p in be_col:
                  col=[]
                  for i in range(0,len(world[p[0]])+1):
                                 col.append([p[0],i])
                  
                  target.append(col)
            if(goal.get("preposition").find("left")>=0):
                  target.reverse()
            #to sort the target_positions in a order from easier solved to harder solved 
             
            after_order=[]
            while(target):
                  for t in target:
                        if(t):
                              after_order.append(t.pop())
                        else:
                              target.remove(t)
             
            goal["target_position"]=after_order
            
 
      elif(goal.has_key("target_position")):

            #to sort the target_position from easier to harder solve whihc is judged by underestimation of cost of target_position
            if(isinstance(goal.get("target_position"),dict)):
                  for  key in goal.get("target_position").keys():
                        goal.get("target_position")[key]=sort_from_easy_to_hard(goal.get("target_position").get(key),world)
            else:
                  target_position=goal.get("target_position")
                  for i in range(0,len(target_position)):
                        index=len(world[target_position[i][0]])-target_position[i][1]
                        target_position[i]=[target_position[i],index]
                  target_position.sort(key=lambda x:x[1])
                  for i in range(0,len(target_position)):
                        target_position[i]=target_position[i][0]
                  goal["target_position"]=target_position
            
             

                  
      if(not goal.has_key("original_position") or goal.get("original_position")==[[-2,-2]]):
            
            command=put_plan(goal,holding)
             

      elif(not goal.has_key("target_position")):
            
            if(goal.get("quantifier")=="any"):
                  #sort the original_positions
                  goal.get("original_position").sort()
                  order=[]
                  for o in goal.get("original_position"):
                        order.append([len(world[o[0]])-o[1],o])
                  order.sort(key=lambda x:x[0])
                  after_order=[]
                  for o in order:
                        after_order.append(o[1])
                  goal["original_position"]=after_order
                  original_position_copy=goal.get("original_position")
                  #retrieve them one by one and test
                  for o in original_position_copy:
                         goal_copy=copy.deepcopy(goal)
                         goal_copy["original_position"]=[o]
                         command=take_plan(goal_copy)
                         if(isinstance(command,list)):
                               return command
                         else:
                               goal.get("original_position").remove(o)
                         if(not goal.get("original_position")):
                               return response
            else:
                  command=take_plan(goal)
      else:
            
            goal_copy=copy.deepcopy(goal)
            original_position=copy.deepcopy(goal.get("original_position"))
            counter=0
            if(goal.get("quantifier")=="any"):
                  for o in original_position:
                        if(isinstance(goal["target_position"],dict)):
                              
                              for p in goal.get("target_position").get(str(o)):
                                    goal_copy["target_position"]=[p]
                                    goal_copy["object"]=world[o[0]][o[1]]
                                    if(achieve_goal([world],goal_copy)):
                                          goal.get("original_position").remove(o)
                                          break
                               
                        else:
                              for p in goal["target_position"]:
                                    goal_copy["target_position"]=[p]
                                    goal_copy["object"]=world[o[0]][o[1]]
                                    if(achieve_goal([world],goal_copy)):
                                          goal.get("original_position").remove(o)
                                          break
                  if(len(goal.get("original_position"))==0):
                        return "Nothing needed to be done"
            elif(goal.get("quantifier")=="all"):
                  for o in original_position:
                        for p in goal["target_position"]:
                              goal_copy["target_position"]=[p]
                              goal_copy["object"]=world[o[0]][o[1]]
                               
                              if(achieve_goal([world],goal_copy)):
                                    counter+=1
                                    break
                  if(len(original_position)==counter):
                       
                        return "Nothing  needed to be done"
             
            else:
                         
                              
                  for p in goal["target_position"]:
                        goal_copy["target_position"]=[p]
                        goal_copy["object"]=world[original_position[0][0]][original_position[0][1]]
                        if(goal_copy.get("preposition")=="under"):
                              if(p==original_position[0]):
                                    return "Nothing  neeeded to be done"
                        else:
                             
                              if(achieve_goal([world],goal_copy)):
                                    return "Nothing  needed to be done"
            if(goal.get("quantifier")=="any"):
                 #sort the original_positions
                  goal.get("original_position").sort()
                  order=[]
                  for o in goal.get("original_position"):
                        order.append([len(world[o[0]])-o[1],o])
                  order.sort(key=lambda x:x[0])
                  after_order=[]
                  for o in order:
                        after_order.append(o[1])
                  goal["original_position"]=after_order
                  original_position_copy=goal.get("original_position")
                  #retrieve them one by one and test
                  any_position=[]  
                  for o in original_position_copy:
                         goal_copy=copy.deepcopy(goal) 
                         if(isinstance(goal_copy.get("target_position"),dict)):
                               goal_copy["target_position"]=goal_copy.get("target_position")[str(o)]
                         
                             
                         goal_copy["target_position"]=sort_from_easy_to_hard(goal_copy.get("target_position"),world)
                         for p in goal_copy.get("target_position"):
                                    any_position.append([o,p,abs(len(world[o[0]])-o[1])+abs(len(world[p[0]])-p[1])])
                  any_position.sort(key=lambda x:x[2])
                  for p in copy.deepcopy(any_position):
                      goal_copy=copy.deepcopy(goal)
                      goal_copy["original_position"]=[p[0]]
                      goal_copy["target_position"]=[p[1]]
                      goal_copy["object"]=world[p[0][0]][p[0][1]]
                      
                      command=move_plan(goal_copy)
                        
                      if(isinstance(command,list)):
                          return command
                      else:
                          any_position.remove(p)
                  if(len(any_position)==0):
                          return response
            else:
                  command=move_plan(goal) 
            
          
      
      return command
