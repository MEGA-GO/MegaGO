from goatools.obo_parser import GODag
import os
from goatools.associations import dnld_assc
from goatools.semantic import deepest_common_ancestor
from goatools.semantic import semantic_similarity
from goatools.semantic import TermCounts, get_info_content
from goatools.semantic import lin_sim
from goatools.anno.idtogos_reader import IdToGosReader


def read_input(file_path):

  """"
  This function reads a csv with two columns of GO terms, coming from two datasets
  Returns two lists of GO terms
  """

  GO_list1, GO_list2 = list(), list()
  
  with open(file_path, "r", encoding='utf-8-sig') as in_f: #other files might require other encoding?
    for line in in_f:
      if not line.startswith("GO"): # skip header
        continue
      GO1, GO2, _ = line.strip().split(",", maxsplit=2)
      
      # add GO1 to GO_list1
      GO1_sub = list()
      if ";" in GO1:
        mGO = GO1.split(";")
        for GO in mGO:
          GO1_sub.append(GO)
      else:
        GO1_sub.append(GO1)
      GO_list1.append(GO1_sub)
      

      # add GO2 to GO_list2
      GO2_sub = list()
      if ";" in GO2:
        mGO = GO2.split(";")
        for GO in mGO:
          GO2_sub.append(GO)
      else:
        GO2_sub.append(GO2)
      GO_list2.append(GO2_sub)
    
    return GO_list1, GO_list2
	
def compare_tools():
	godag = GODag("go-basic.obo")
	associations = IdToGosReader("data/associations-uniprot-sp-20200116.tab", godag=godag).get_id2gos('all')

	# First get the counts of each GO term.
	termcounts = TermCounts(godag, associations)
	GO_list1, GO_list2 = read_input('data/example_input-compare_goa.csv')
	for i in range(0,len(GO_list1)):
	  BMA_test = BMA(GO_list1[i],GO_list2[i],termcounts,godag)
	  print(BMA_test)

def BMA(GO_list1,GO_list2,termcounts,godag,similarity_method=None):
    summationSet12 = 0.0
    summationSet21 = 0.0
    for id1 in GO_list1:
        similarity_values = []
        for id2 in GO_list2:
            similarity_values.append(Rel_Metric(id1,id2,godag,termcounts))
        summationSet12 += max(similarity_values)
    for id2 in GO_list2:
        similarity_values = []
        for id1 in GO_list1:
            similarity_values.append(Rel_Metric(id2,id1,godag,termcounts))
        summationSet21 += max(similarity_values)
    return (summationSet12+summationSet21)/(len(GO_list1)+len(GO_list2))

def Rel_Metric(id1,id2,godag,termcounts):
    if id1 =='' or id2 =='':
      return -1
    goterm1 = godag[id1]
    goterm2 = godag[id2]
    if goterm1.namespace == goterm2.namespace:
      mica_goid = deepest_common_ancestor([id1, id2], godag)
      freq = termcounts.get_term_freq(mica_goid) 
      infocontent = get_info_content(mica_goid, termcounts)
      infocontent1 = get_info_content(id1, termcounts)
      infocontent2 = get_info_content(id2, termcounts)
      return (2*infocontent*(1-freq))/(infocontent1+infocontent2)
    else:
      return -1


if __name__ == '__main__':
    compare_tools()




