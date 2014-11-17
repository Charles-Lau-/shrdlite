#!/usr/bin/env python

# Test from the command line:
# python shrdlite.py < ../examples/medium.json

from __future__ import print_function

import sys
import json
import copy
GRAMMAR_FILE = "shrdlite_grammar.fcfg"

# IMPORTANT NOTE:
# 
# If you are using NLTK 2.0b9 (which is the one that is installed 
# by the standard Ubuntu repository), then nltk.FeatureChartParser
# (in the parse function) fails to parse some sentences! In this 
# case you can use nltk.FeatureTopDownChartParser instead.
# You can check if it is working by calling this:
# 
#   python shrdlite.py < ../examples/small.json
# 
# The program should return "Ambiguity error!". If it instead
# returns "Parse error!", then the NLTK parser is not correct, 
# and you should change to nltk.FeatureTopDownChartParser instead.

def get_tree_label(result):
    """Returns the label of a NLTK Tree"""
    try:
        # First we try with NLTKv3, the .label() method:
        return result.label()
    except AttributeError, TypeError:
        # If that doesn't work we try with NLTKv2, the .node attribute:
        return result.node

def get_all_parses(parser, utterance):
    """Returns a sequence of all parse trees of an utterance"""
    try:
        # First we try with NLTKv2, the .nbest_parse() method:
        return parser.nbest_parse(utterance)
    except AttributeError, TypeError:
        try:
            # Then we try with NLTKv3, the .parse_all() method:
            return parser.parse_all(utterance)
        except AttributeError, TypeError:
            # Finally we try with NLTKv3, the .parse() method:
            return parser.parse(utterance)

def parse(utterance):
    import nltk
   
     
    grammar = nltk.data.load("file:" + GRAMMAR_FILE, cache=False)
    parser = nltk.FeatureChartParser(grammar)
     
    try:
      
        do_parse = getattr(parser, 'nbest_parse', 
                       getattr(parser, 'parse_all', parser.parse))
        return do_parse(utterance)
         
    except ValueError:
        return []

def main(utterance, world, holding, objects, **_):
    result = {} 
    result['utterance'] = utterance
    trees = parse(utterance)
    if not trees:
        result['output'] = "Parse error!"
        return result
    
    result['trees'] = [str(t[2].node["sem"]) for t in trees] 
    
    import interpreter
    result['goals'] = goals =[interpreter.interpret(tree,world,objects,holding) for tree in trees]
   
    if not goals:
        result['output'] = "Interpretation error!"
        return result
    #if there are several parse tree, we check every one and see how many works, we just
    #ignore the one that does not work, and if there is only one left, then it is good
    #if there are several left, we should ask question and let the user decide which one
    #he want
    parse_tree_for_ambiguity=[t[2].node["sem"] for t in trees]
    flag=False
    error_information=[]
    goals_copy=copy.deepcopy(goals)
    for i in range(0,len(goals_copy)):
         
        if(isinstance(goals_copy[i],dict)):
           flag=True
        else: 
           error_information.append(goals_copy[i])
           goals.remove(goals_copy[i])
           try:
               del parse_tree_for_ambiguity[i]
           except:
               pass  
    if(not flag):
           del result['goals']
           if(len(error_information)>1):
               error=[]
               for i in range(0,len(error_information)):
                   error.append(" In No."+str(i+1)+" parse tree , "+error_information[i])
                    
               result['output']="There are "+str(len(error_information))+" different way to interpret this sentence ~!"+" and ".join(error) 
           else:
               result['output']=error_information.pop()
           return result
    #We use this module to solve these ambiguity problems
    #First: there are several plannable goal, we ask questions
    #Second: there are one plannable goal, but there are several objects to be moved and
    #the quantifier is not all or any, we should tell the user
      
    import ambiguity 
    response=ambiguity.is_ambiguous(goals,world,objects,parse_tree_for_ambiguity)
    
    if response[0]:
        del result['goals']
        result['output']=response[1]
        return result
    #after check of ambiguity,then,there are only one element in the goals and it is a unambiguious goal
    goal = goals[0]
    #update the parse_trees,to exclude the trees that are not possible
    result['trees']=[str(i) for i in parse_tree_for_ambiguity]
    
    import planner 
    result['plan'] =plan=planner.plan(goal,world,holding,objects)
    if not plan:
        result['output'] = "Planning error!"
        return result
    elif isinstance(plan,str):
        del result['plan']
        result['output']=plan
        return result

    result['output'] = "Success!"

    return result


if __name__ == '__main__':
    input = json.load(sys.stdin)
    output = main(**input)
    # json.dump(output, sys.stdout)
    # json.dump(output, sys.stdout, sort_keys=True, indent=4)
    print("{", ",\n  ".join('%s: %s' % (json.dumps(k), json.dumps(v))
                            for (k, v) in output.items()), "}")
