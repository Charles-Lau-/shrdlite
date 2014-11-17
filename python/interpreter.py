import sys
import copy
#globalvariable,result contains all data that a goal needs
#globalvariable,we use coordinate to discribe the world and use d_world to
#represent it 
world=[]
d_world=[]
world_objects=[]
error_information=""
 
#relatioon: on,inside,beside etc.
#relative_coordinate: the coordinate of object after on,inside or beside etc.
class MyException(Exception):pass
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
def deal_with_relation(relation,relative_coordinate):
      index=0
      coord=list(relative_coordinate)
      if(relation.startswith("on") or relation.startswith("in")):
            for co in coord:
                  co[1]=co[1]+1
                  coord[index]=[co[0],co[1]]
                  index+=1
                 
            return coord
      elif(relation=="above"):
            ab_coord=[]
            for co in coord:
                  for i in range(co[1],len(world[co[0]])):
                        ab_coord.append([co[0],i+1])
            ab_coord.reverse()
            ab_coord_copy=copy.deepcopy(ab_coord)
            for col in ab_coord_copy:
                  if(ab_coord.count(col)>1):
                        ab_coord.remove(col)
            return ab_coord
      elif(relation.startswith("under")):
            un_coord=[]
             
            for co in coord:
                  for i in range(0,co[1]+1):
                        un_coord.append([co[0],i])
            un_coord.reverse() 
          
            return un_coord
      #negative 1 denote that we ignore the value of this dimension
      elif(relation.find("left")>=0):
            le_coord=[]
            for co in coord:
                  for i in range(0,co[0]):
                        le_coord.append([i,-1])
            return le_coord
      elif(relation.find("right")>=0):
            ri_coord=[]
            for co in coord:
                   for i in range(co[0]+1,len(world)):
                         ri_coord.append([i,-1])
            return ri_coord
      elif(relation.startswith("beside")):
            be_coord=[]
            for co in coord:
                  if(co[0]>0):
                        be_coord.append([co[0]-1,-1])
                  if(co[0]+1<len(world)):
                        be_coord.append([co[0]+1,-1])
                  index+=1
            return be_coord
#return the intersection of two coordinate array.
#Like arr1=[(1,2),(2,3)],arr2=[(1,2),(2,4)],we get(1,2)
def intersect(arr1,arr2):
      intersection=[];
      if(len(arr1)==0 or len(arr2)==0):
            if(len(arr1)==0):
                  return []
            else:
                  return []
      for i in arr1:
            for j in arr2:
                  if(i==j):
                        intersection.append(i)
                  if(i[1]==-1 or j[1]==-1):
                        if(i[0]==j[0]):
                              intersection.append(i[1]==-1 and j or i)
                              break
       
      return intersection
#from the signature of the object we could get its or their coordinate
#Like the green ball or the large box, (quantifier,size,color,form) is signature
def signature2position(signature):
      d_world_copy=copy.deepcopy(d_world) 
      coordinate=[]
      if(signature=="floor"):
            coordinate=d_world_copy[-1]
       
            return coordinate
      sig=signature.split(" ")
      quantifier=sig[0]
      
      form=sig[-1]
      #since when quantifier is all the word of object is plural like all boxes,then d_world[2].get("boxes") will return null
      #so that we just for all keys in d_world[2] we check whether they are similar like boxes.contain(box)
      if(quantifier=="all"):
            if(form.find("object")>=0):
                for c in range(0,3):
                      for key in d_world_copy[c].keys():
                             for value in d_world_copy[c].get(key):
                                   if(value not in coordinate):
                                            
                                            coordinate.append(value)       
            else:
                for f in d_world_copy[2].keys():
                    if(form.find(f)>=0):
                        coordinate=d_world_copy[2].get(f)
                        
      else:
            #when it is object, coordinate is equal to the d_world[2]
            if(form=="object"):
                  for value in d_world_copy[2].values():
                            for c in value:
                                  coordinate.append(c) 
            else:
                   
                  coordinate=d_world_copy[2].get(form,[])[:]

                     
      for i in sig[1:-1]:
            s=d_world_copy[0].get(i,[])
            c=d_world_copy[1].get(i,[])
            coordinate=intersect((s==[] and c or s),coordinate)
      
     
      return coordinate
#we use coordinate to discribe the

def digitalize_the_world(world,objects,holding):
      col=-1
      digital_world=[{},{},{},[]]
      #first dictionary contains  the coordinate of specific size
      digital_world[0]={}
      #second dictionary contains  the coordinate of specific color
      digital_world[1]={}
      #third dictionary contains the coordinate of specific form 
      digital_world[2]={}
      #last dictionary contains the coordinate of the floor.we assume they are (i,-1)
      digital_world[3]=[]
      for w in world:
          row=-1
          col=col+1
          digital_world[3].append([col,-1])
          for j in w:
              row=row+1
              for object in objects:
                  o=objects[object]
                  if(object==j):
                      tempt=digital_world[0].get(o["size"],[ ])
                      tempt.append([col,row])
                      digital_world[0][o["size"]]=tempt

                      tempt=digital_world[1].get(o["color"],[ ])
                      tempt.append([col,row]) 
                      digital_world[1][o["color"]]=tempt

                      tempt=digital_world[2].get(o["form"],[ ])
                      tempt.append([col,row])
                      digital_world[2][o["form"]]=tempt
      if(holding):
            h=world_objects.get(holding)
            tempt=digital_world[0].get(h["size"],[ ])
            tempt.append([-2,-2])
            digital_world[0][h["size"]]=tempt

            tempt=digital_world[1].get(h["color"],[ ])
            tempt.append([-2,-2]) 
            digital_world[1][h["color"]]=tempt

            tempt=digital_world[2].get(h["form"],[ ])
            tempt.append([-2,-2])
            digital_world[2][h["form"]]=tempt
     
      return digital_world
def spatial_relation_is_reasonable(preposition,entity):
      category_entity=len(entity)
      if(category_entity==1):
            obj=entity.node["sem"]
      else:
            obj=entity[1][-1]
            obj=obj.node["sem"]
      if(obj=="floor"):
            if(preposition.startswith("on")):
                  return (True,)
            elif(preposition=="above"):
                  return (True,)
            else:
                  return (False,"you can only put object on the floor or above the floor")
      elif(obj.find("box")>=0):
            if(preposition.startswith("in")):
                  return (True,)
            elif(preposition.startswith("on")):
                  return (False,"you can only put objects inside boxes ")
            else:
                  return (True,)
      elif(preposition.startswith("in")):
            return (False,"you can put object in "+obj)
                    
      else:
            return (True,)
#get the coordinate of location like location:on the green box.
#we will return(coordinate(green box).x,coordnate(green box).y+1)
def deal_with_location(location):
     global error_information
     location_relation=location[0]
     location_entity=location[1]
     entity_position=deal_with_entity(location_entity)
     response=spatial_relation_is_reasonable(location_relation.node["sem"],location_entity)
     if([-2,-2] in entity_position):
           entity_position.remove([-2,-2]) 
           if(entity_position==[]):
                 error_information="you are holding it"
                 raise MyException
     if(not response[0]):
           error_information=response[1]
           raise MyException
    
     if(location_entity[0].node.get("sem")=="all" and len(entity_position)>1):
           position=[]
           for p in entity_position:
                position.append(deal_with_relation(location_relation.node["sem"],[p])) 
           coord=[]
           for p in position:  
                coord=coord==[] and p or intersect(coord,p)  
                if(coord==[]):
                     return [[],entity_position]         
           return [coord,entity_position]
     else:
          return [deal_with_relation(location_relation.node["sem"],copy.deepcopy(entity_position)),entity_position]
      
def deal_with_entity(entity):
     global error_information
     category_entity=len(entity)  
     if(category_entity==1):
           ent_position=signature2position(entity.node["sem"])
           #if the coordinate is null then we could just exit and notify users that object does not exist
           if(len(ent_position)==0):
                 error_information= entity.node["sem"]+" does not exist in the world"
                 
                 raise MyException	
          
           return  ent_position
     elif(category_entity==2):
           quantifier=entity[0].node["sem"]
           obj=""
               
           for i in entity[1]:
                obj=obj+" "+i[0]
           
           signature=quantifier+obj
            
           ent_position=signature2position(signature)

           if(len(ent_position)==0):
                 error_information= str(signature+" does not exist in  the world")
                 
                 raise MyException
            
           return ent_position
      
     elif(category_entity==4):
           quantifier=entity[0].node["sem"]
           obj=""

           for i in entity[1]:
                obj=obj+" "+i[0]
           signature=quantifier+obj

           basic_object_position=signature2position(signature)
           
           if(len(basic_object_position)==0):
                 error_information=str(signature+" does not exist in the world")
                	
                 raise MyException

                
           location=entity[3]
           
           rel_position=deal_with_location(location)
          
         
           if(location[0].node["sem"]=="under"):
                 entity_position=rel_position[-1]
                 rel_position_copy=copy.deepcopy(rel_position[0])
                   
                 for e in entity_position:
                       for r in rel_position_copy:
                             if(e==r):
                                   rel_position[0].remove(e)
                                   break
           
           rel_position=rel_position[0] 
            
                   
           compound_object=intersect(basic_object_position,rel_position)
           #check whether the relation exist between to object
           #like the green box on the red table.But there are no green box on the red table.
           if(len(compound_object)==0):
                 error_information="Spatial relationship does not exist "
                  
                 raise MyException
             
           return compound_object
def put(put_command,result):
    global error_information 
    location=put_command[2]
    position_of_target=deal_with_location(location) 
    result["target_position"]=position_of_target[0]
    result["original_position"]=[[-2,-2]]
    #used to deal with ambiguity
    if(location[0].node["sem"]=="under"):
                  position_of_target[1].sort(key=lambda x:-x[1])
                  new_target_position=[]
                  for p in position_of_target[1]:
                        if(p[0] not in [i[0] for i in new_target_position]):
                                  new_target_position.append(p)
                  position_of_target[1]=new_target_position
    elif(location[0].node["sem"]=="above"):
                  position_of_target[1].sort(key=lambda x:x[1])
                  new_target_position=[]
                  for p in position_of_target[1]:
                        if(p[0] not in [i[0] for i in new_target_position]):
                                  new_target_position.append(p)
                  position_of_target[1]=new_target_position    
    elif(location[0].node["sem"].find("left")>=0 or location[0].node["sem"].find("right")>=0 or location[0].node["sem"].find("beside")>=0):
                  new_target_position=[]
                  for p in position_of_target[1]:
                        if(p[0] not in [i[0] for i in new_target_position]):
                                  new_target_position.append(p)

                  position_of_target[1]=new_target_position 
     
     
    if(len(position_of_target[1])>1 and location[1][0].node.get("sem")=="the"): 
		 question=[]
                 for p in position_of_target[1]:
                        question.append(" ".join(realize_the_world([p])))
                 error_information="which one would you like to put "+location[0].node["sem"]+" ? "+" or ".join(question)
                 raise MyException  
     
    result["preposition"]=location[0].node["sem"]
def move(move_command,result):
     global error_information,d_world
     entity=move_command[1]
      
     position_of_entity=deal_with_entity(entity)

      
     location=move_command[2]
     #special use for all-quantifier
     
     if(True):
            objects=[]
            coordinates=deal_with_entity(location[1])
          
            if(coordinates==d_world[-1]):
                  objects.append("floor")
                   
            else:
                   for coord in coordinates:
                         objects.append(world[coord[0]][coord[1]])
            result["target_objects"]=objects
    
     
     if(position_of_entity==d_world[-1]):
            error_information="Stupid human beings, you can not move the floor"
            raise MyException
     target={}

     if(len(position_of_entity)==1):
            for p in copy.deepcopy(position_of_entity):
                  if(world[p[0]][p[1]] in result.get("target_objects")):
                          position_of_entity.remove(p)
     if(len(position_of_entity)==0):
            error_information="Physical law is not allowed"
            raise MyException  
     
     result["original_position"]=position_of_entity
     if(location[1][0].node.get("sem")=="any" and entity[0].node.get("sem")!="all"):
           digital_world=copy.deepcopy(d_world)
           for o in position_of_entity:
                 d_world=copy.deepcopy(digital_world)
                 for c in range(0,3):
                       for key in d_world[c].keys():
                             values=d_world[c].get(key)
                             if(o in values):
                                   values.remove(o)
                                   d_world[c][key]=values
                                      
                                  
                                                                                   
                  
                 try:
                     position_of_target=deal_with_location(location)[0]
                 except:
                     position_of_target=[] 
                 target[str(o)]=position_of_target
           d_world=digital_world
           if(len(target)==1):
                  
                 result["target_position"]= target.values()[0]
           
            
       
           else:
                 result["target_position"]=target
           
     else:
           position_of_target=deal_with_location(location)
            
           if(location[0].node["sem"]=="under"):
                  position_of_target[1].sort(key=lambda x:-x[1])
                  new_target_position=[]
                  for p in position_of_target[1]:
                        if(p[0] not in [i[0] for i in new_target_position]):
                                  new_target_position.append(p)
                  position_of_target[1]=new_target_position
           elif(location[0].node["sem"]=="above"):
                  position_of_target[1].sort(key=lambda x:x[1])
                  new_target_position=[]
                  for p in position_of_target[1]:
                        if(p[0] not in [i[0] for i in new_target_position]):
                                  new_target_position.append(p)
                  position_of_target[1]=new_target_position    
           elif(location[0].node["sem"].find("left")>=0 or location[0].node["sem"].find("right")>=0 or location[0].node["sem"].find("beside")>=0):
                  new_target_position=[]
                  for p in position_of_target[1]:
                        if(p[0] not in [i[0] for i in new_target_position]):
                                  new_target_position.append(p)

                  position_of_target[1]=new_target_position
           if(len(position_of_target[1])>1 and location[1][0].node.get("sem")=="the"): 
		 question=[]
                 
                 for p in position_of_target[1]:
                        
                        question.append(" ".join(realize_the_world([p])))
                 error_information="which one would you like to put "+location[0].node["sem"]+" ? "+" or ".join(question)
                 raise MyException   

           result["target_position"]=position_of_target[0]
             
     #used to deal with ambiguity
     result["preposition"]=location[0].node["sem"]
     result["quantifier"]=entity[0].node["sem"]
     
     #used for all-quantifier 
     #resutl["objects"]=objects
def take(take_command,result):
      global error_information
      entity=take_command[1]
      position_of_entity=deal_with_entity(entity) 
      result["original_position"]=position_of_entity
      
      if(position_of_entity==d_world[-1]):
            error_information="Stupid human beings, you can not take the floor"
            raise MyException
      result["quantifier"]=entity[0].node["sem"]
def interpret(tree,world_parameter,objects,holding):
    global world,world_objects,d_world
    world=world_parameter
    world_objects=objects
    d_world=digitalize_the_world(world,world_objects,holding)
    result={}
    opt_will_you=tree[0]
    opt_please=tree[1]
    basic_command=tree[2]
    action=basic_command.node["sem"][0]
    result["action"]=action
    try:
        if(action=="take"):
          take(tree[2],result)
        elif(action=="put"):
          if(holding!=None):
               put(tree[2],result)
          else:
               return "Hey man,U are not holding anything"
        elif(action=="move"):
          move(tree[2],result)	
    except MyException:
        return error_information   
        
    return result

