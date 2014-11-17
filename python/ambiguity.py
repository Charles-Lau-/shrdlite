#there three kind of ambiguities:
#1: there are more than one parse tree for one sentence
#2: there are more than one object in the world
#reverse process of digitalize_the_world
#from coordinate to object
#like: from (0,0) to red large ball
#used for ambiguity
import interpreter
import copy
import planner
d_world=[]
world=[]
world_objects={}
def realize_the_world(coordinates):
      
      map_to_real_world=[]
      if(coordinates==d_world[-1]):
            map_to_real_world.append("the floor")
            return map_to_real_world
      for coord in coordinates:
              
            obj=world[coord[0]][coord[1]]
            discript=world_objects.get(obj)
            signature=discript.get("size","")
            signature=signature+" "+discript.get("color","")
            signature=signature+" "+discript.get("form","")
            signature=signature.split(" ")  
            if(len(map_to_real_world)==0):
                  map_to_real_world=signature
            else:
                  map_to_real_world=interpreter.intersect(map_to_real_world,signature)
      for discript in world_objects.values():
            if(map_to_real_world.count(discript.get("form"))!=0):
                   
                  return map_to_real_world
      map_to_real_world.append("object")
     
      return map_to_real_world
def deal_with_second_case(goal):
      import physical_law
       
      response=[]
      propo=goal.get("preposition")
      action=goal.get("action")
      quantifier=goal.get("quantifier","")
      original_position=goal.get("original_position",[])
      if(quantifier!="every" and quantifier!="all" and quantifier!="any" and len(original_position)>1):
            #remove the original_position that has already been satified 
            
            for ori in  original_position:
                  for tar in goal.get("target_position",[]):
                        if(ori==tar):
                              original_position.remove(ori)
                              break
            if(len(original_position)<2):
                  goal["original_position"]=original_position
                  return (False,"")
            #remove the original_position that violate physical_law:
             
            if(goal.get("target_position",[])!=[]):
                  for ori in copy.deepcopy(original_position):
                        if(ori==[-2,-2]):
                              original_position=[[-2,-2]]
                              break
                              
                        goal_copy=copy.deepcopy(goal)
                        goal_copy['object']=world[ori[0]][ori[1]]
                        if(isinstance(goal.get("target_position"),dict)):
                              goal_copy["target_position"]=goal.get("target_position")[str(ori)]
                        if(goal_copy.get("target_position")[0][1]!=-1 and not physical_law.obey_physical_law(world,world_objects,goal_copy)):
                              if(len(original_position)==1):
                                    pass
                              else:
                                    original_position.remove(ori)

            if(len(original_position)<2):
                  goal["original_position"]=original_position
                  return (False,"")
                
            for i in original_position:
                  response.append(" ".join(realize_the_world([i])))
            return (True,"which one would you like to "+action+","+" or ".join(response))
                
      else:
              
            if(not goal.has_key("target_position") and goal.get("quantifier")=="all"):
                   
                  for i in original_position:
                      response.append(" ".join(realize_the_world([i])))
                  return (True,"which one would you like to "+action+","+" or ".join(response))
  
            else:
                  if([-2,-2] in goal.get("original_position") and not goal.get("quantifier")=="all"):
                         goal["original_position"]=[[-2,-2]]
                  return (False,"")
def generate_sentence(parse_tree):
      sentence=[]
      add_that=False
      for t in parse_tree:
            if(not isinstance(t,str)):
                  if(add_that and t[0]=="relative"):
                        sentence.append("that is")
                  sentence.append(generate_sentence(t))
            else:
                  if(t=="relative_entity"):
                       add_that=True
                  if(t=="-" or t=="relative_entity" or t=="basic_entity" or t=="object" or t=="relative"):
                        pass
                  else:
                        sentence.append(t)
   
      return " ".join(sentence)
def deal_with_first_case(goals,parse_tree):
      sentences=[]
      for tree in parse_tree:
            sentences.append(generate_sentence(tree))
       
      return " or ".join(sentences)
def is_ambiguous(goals,world_parameter,objects,parse_tree):
      
      global d_world,world,world_objects
      world_objects=objects
      world=world_parameter
      d_world=interpreter.digitalize_the_world(world_parameter,objects,None)
        
     
      if(len(goals)>1):
            return (True,deal_with_first_case(goals,copy.deepcopy(parse_tree)))
      else:
            return deal_with_second_case(goals[0])
      

