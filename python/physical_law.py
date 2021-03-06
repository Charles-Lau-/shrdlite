import copy
world=[]
world_objects={}
def isFloor(position):
      if(isinstance(position,list) and not isinstance(position[0],int) and len(position)==len(world)):
            for i in position:
                  if(i[1]!=0):
                        return False
            return True
      else:
            return False
def isLargeBrick(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="brick" and signature.get("size")=="large"):
            return True
      else:
            return False
def isLargeBox(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="box" and signature.get("size")=="large"):
            return True
      else:
            return False
def isTable(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="table"):
            return True
      else:
            return False
def isSameSize(obj,object_lying_below):
      signature1=world_objects.get(obj)
      signature2=world_objects.get(object_lying_below)
      if(signature1.get("size")==signature2.get("size")):
            return True
      else:
            return False
def isPlank(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="plank"):
            return True
      else:
            return False
def isPyramid(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="pyramid"):
            return True
      else:
            return False
def size(obj):
      signature=world_objects.get(obj)
      if(signature.get("size")=="small"):
            return 0
      else:
            return 1
def isBox(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="box"):
            return True
      else:
            return False
def isBall(obj):
      signature=world_objects.get(obj)
      if(signature.get("form")=="ball"):
            return True
      else:
            return False
def obey_physical_law(world_parameter,objects,goal):
      global world,world_objects
      world=world_parameter
      world_objects=objects
      if(goal.get("preposition").startswith("on") or goal.get("preposition").startswith("in")):
            target_position=copy.deepcopy(goal.get("target_position"))
            
            for target in target_position:
                  if(not obey_physical_law_with_quantifier_on(world,world_objects,goal.get("object"),target)):
               
                        goal.get("target_position").remove(target)
            
            if(len(goal.get("target_position"))==0):
                  return False
            else:
                  return True
      elif(goal.get("preposition")=="under"):
           target_position=copy.deepcopy(goal.get("target_position"))
            
           for p in target_position:
                  if(not obey_physical_law_with_quantifier_under(world,world_objects,goal.get("object"),[p])):
                        goal.get("target_position").remove(p) 
           if(len(goal.get("target_position"))==0):
                  return False
           else:
                  return True

      elif(goal.get("preposition")=="above" or goal.get("preposition")=="beside" or goal.get("preposition").find("left")>=0 or goal.get("preposition").find("right")>=0):
            
            target_position=copy.deepcopy(goal.get("target_position"))
             
            for p in target_position:
                  if(not obey_physical_law_with_quantifier_on(world,world_objects,goal.get("object"),[p])):
                        goal.get("target_position").remove(p) 
            if(len(goal.get("target_position"))==0):
                  return False
            else:
                  return True
       
def obey_physical_law_with_quantifier_under(state,objects,position_or_object,target_position):
      global world_objects
      world_objects=objects
      
      if(isinstance(target_position,list) and not isinstance(target_position[0],int)):
            target_position=target_position[0]
     
      if(target_position[1]==0 or obey_physical_law_with_quantifier_on(state,world_objects,position_or_object,target_position)):
            if(len(state[target_position[0]])>=target_position[1]+1):
                  if(not isinstance(position_or_object,unicode)):
                        position_or_object[1]+=1
                   
                  if(obey_physical_law_with_quantifier_on(state,world_objects,state[target_position[0]][target_position[1]],position_or_object)):
                  
                        return True
                  else:
                          
                        return False
            else:
                  return True
      else:
             
            return False
def obey_physical_law_with_quantifier_on(state,objects,position_or_object,target_position):
    global world_objects
    world_objects=objects
    object_lying_below=None 
    if(isFloor(target_position)):
          return True
    if(isinstance(target_position,list) and not isinstance(target_position[0],int)):
          target_position=target_position[0]
    if(isinstance(target_position,unicode)):
        
          object_lying_below=target_position
    else: 
          col=target_position[0]
          row=target_position[1]
    if(isinstance(position_or_object,unicode)):
          obj=position_or_object
    else: 
          obj=state[position_or_object[0]][position_or_object[1]]
    #check whether it is floor
      
    if(not isinstance(target_position,unicode) and target_position[1]==0):
          return True
     
    if(isinstance(target_position,unicode) or len(state[col])>0):
       object_lying_below=object_lying_below==None and  state[col][row-1] or object_lying_below 
           
       if(isBall(object_lying_below)):
              
             return False
       elif(size(object_lying_below) < size(obj)):
              
             return False
       elif(isBall(obj)):
             if(not isBox(object_lying_below)):
                   return False
             else:
                   return True
        
       elif(isBox(object_lying_below)):
             if(isPyramid(obj) or isPlank(obj)):
                   if(isSameSize(obj,object_lying_below)):
                         return False
                   else:
                         return True
             else:
                   return True
       elif(isBox(obj)):
             if(isTable(object_lying_below) or isPlank(object_lying_below)):
                   if(isSameSize(obj,object_lying_below)):
                         return True
                   else:
                         return False
                        
             elif(isLargeBox(obj) and isLargeBrick(object_lying_below)):
                   return True
             else:
                   return False
       else:
            return True
    
    else:
            return True
