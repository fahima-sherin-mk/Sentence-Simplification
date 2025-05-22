import spacy
#import sys
import nltk
import regex as re
#importing libraries to break a text into sentences
from spacy.lang.en import English
def checkComplex(sent,out):
    #print(sent)
    words=sent.split(' ')
    #conjunctions that are usually found in a complex sentence
    complex_conj1=['before','after','when','because','although','though','whenever','as','since','if','but','while','where','who','wherever','until','thus']
    #conjunctions that usually occur toogether and are found in complex sentences
    complex_conj2=['but when','even though','now that','so that']
    new_sent=''                                                 #to store the simple sentences formed from complex sentences

    #we first break sentences containing 2nd type of conjuntions into simple sentences
    for conj in complex_conj2:                  #loop to check each conjunction if it is present in the sentences

        if (sent.lower()).find(conj)>=0:

            if (sent.lower()).find(conj)==0:    #If the conjunction appears in the beginning then we split the sentence at the ','
                broken_sent=sent.split(',')     #e.g Even though he had a lot of money, he was still unhappy
                new_sent=((broken_sent[0].lower()).replace(conj,''))+'.'+'.'.join(b for b in broken_sent[1:])     #joining the broken sentences to form the new text
                out.write("\n"+new_sent)
                #return new_sent                                 #return the new sentence formed

            else:                               #If the conjunction appears in the middle
                broken_sent=sent.split(conj)    #then we split the sentence in the middle
                new_sent=(broken_sent[0].replace(',',''))+'. '+'.'.join(b for b in broken_sent[1:])      #joining the broke sentences to form a new text
                out.write("\n"+new_sent)
                #return new_sent                                                 #returning the new text formed

    for conj in complex_conj1:                  #checking whether the sentence contains any of the conjunction in the first group
        if words[0].lower()==conj:              #If the conjunction is the first word,
            sent=' '.join(word for word in words[1:])    #then we remove the first word, i.e. the conjunction
            broken_sent=sent.split(',')                  #Then we break the sentnce at the ','
            new_sent=broken_sent[0]+'. '+'.'.join(b for b in broken_sent[1:])   #Then we join the broken senteces to form the new text
            out.write("\n"+new_sent)
            #return new_sent                              #Returning the newly formed text from simple sentences

        else:                                  #else we check if the conjunction is in the middle of the sentence
            flag=0                             #flag to check the above
            for word in words:                 #checking each word of the sentence of it is a conjunction
                if word==conj:                 #If it is a conjunciton,
                    flag=1                     #then we set the flag
                    break
            if flag==1:                        #If the flag is set
                broken_sent=sent.split(' '+conj+' ')    #Then we break the sentence into two parts at the conjunction
                new_sent=(broken_sent[0].replace(',',''))+'. '+'.'.join(b for b in broken_sent[1:])   #and make a new text
                out.write("\n"+new_sent)
                #return new_sent                                               #and then return it


    if 'where' in words:                        #If the conjunction is 'where' and comes in the middle of the sentence
        broken_sent=sent.split('where')         #Then we split the sentence at 'where'
        new_sent=broken_sent[0]+'. There '+broken_sent[1]     #And append 'There' to the beginning of the 2nd boken part
        out.write("\n"+new_sent)
#        return new_sent                                       #And return the new text thus formed

    if 'who' in words:                          #If the conjunction is 'who' and comes in the middle of the sentence
        broken_sent=sent.split('who')           #Then we split the sentence at 'who'
        new_sent=broken_sent[0]+'. They '+broken_sent[1]    #And append 'they' to the 2nd part of the broken sentence
        out.write("\n"+new_sent)
        #return new_sent                                     #And return the new text thus formed

    #out.write("\n"+sent)
    return sent                                 #If the sentence is not complex we return the sentence as it is
def get_it_all_spacy(sen):
  doc = nlp(sen)
  count=0
  cclst = list()
  sublst = list()
  verblst = list()
  subjlst = list()
  objlst = list()


#**********Coordinating Conjunction**********

  for token in doc:
    count+=1
    if "CC" in token.pos_ or "for" == " "+str(token)+" " or " so " == " "+str(token)+" ":
      cclst.append([count,str(token)])
  if len(cclst)==0:
    cclst.append([count,"CCab"])
  count = 0

#**********Verb**********

  for token in doc:
    count+=1
    if "VERB" in token.pos_ or "AUX" in token.pos_:
      verblst.append([count,str(token)])
  if len(verblst)==0:
    verblst.append([count,"VBab"])
  count = 0

#**********Subject**********

  for token in doc:
    count+=1
    if "NOUN" in token.pos_ or "PRON" in token.pos_ or "PROPN" in token.pos_:
      sublst.append([count,str(token)])
  if len(sublst)==0:
    sublst.append([count,"SBab"])


  k=0
  r=0
  i=0;
  flag = 0
  ccoccur = cclst[i][0]
  verboccur = verblst[k][0]
  try:
    while verboccur< sublst[r][0]:#If verb is coming before subject
      k+=1
      verboccur = verblst[k][0]
  except:
    k-=1
    verboccur = verblst[k][0]

  try:
    flag = 0
    while (1):
      j = sublst[r]
      ccoccur = cclst[i][0]
      verboccur = verblst[k][0]
      if j[0]<=verboccur:#If noun or pronoun is coming before verb, its subject
        subjlst.append([j[0],j[1]])
      if j[0]>verboccur: #If noun/pron is coming after verb, its object
        objlst.append([j[0],j[1]])
      r+=1
      try:
        j = sublst[r]
      except:
        j = sublst[r-1]
      if j[0]>=verboccur:
        try:
          while(j[0]>verboccur):
            k+=1
            verboccur = verblst[k][0]
        except:
          k-=1
          verboccur = verblst[k][0]
      if(flag==1):
        try:
          objlst.append([sublst[r][0],sublst[r][1]])
        except:
          pass
        break;

      if(sublst[r][0]>=ccoccur):
        try:
          i+=1
          ccoccur = cclst[i][0]
        except:
          i-=1
          flag = 1;

  except:
       pass
  return (subjlst,objlst,verblst,cclst)
    #Data preparation completed
def rule_1(sen):
    subjlst,objlst,verblst,cclst = get_it_all_spacy(sen)
    doc = nlp(sen)
    fin = list()
#     print(subjlst,objlst,verblst,cclst)
    broke = list()
    i =0
    j=0
    count = len(cclst)
    if cclst[0][1] == "CCab" :
        #print("Already Simple --- ",sen)
        exit()
    else:
        try:
            cap = cclst[i][1]
#            print("CAP====",cap)
            while (1):
#               print("fgvbudhfcn",str(doc[j]))
                cap = cclst[i][1]
                if str(cap).strip()==str(doc[j]):
                    broke.append(j)
                    count-=1
                    if count!=0:
                        i+=1
                    else:
                        break
                j+=1
        except:
#             print(sys.exc_info()[0])
            pass
        broke.append(len(str(doc)))
#         print(broke)
#        fin = list()
        fin.append(str(doc[0:broke[0]]))
        try:
            for i in range(len(broke)):
                fin.append(str(doc[broke[i]+1:broke[i+1]]))
        except:
#             print(sys.exec_info()[0])
            pass
    final= list()
    for i in fin:
    #     print(i)
        stri = str()
        for j in i:
            stri+= j
        final.append(stri)
    broke = final
#     print(broke)
    return (subjlst,objlst,broke,0)
def rule_2_3(empsubjlst,allavail,onlyobjlst,onlysubjlst):
    count = 0
    try:
        # The following works on rule 2 or 3 check plus performs
        # the rules on the lists provided it passes rule 1
        while len(empsubjlst)!=0: # If no subject then perform reverse rule 2
            # The following performs rule3
            extract = len(allavail)-1 # Gets the most recently used string to append to the subject.
            subj3lst,obj3lst,verb3lst,cc3lst = get_it_all_spacy(allavail[extract][1])
            #print("CCLST")
#                 finstr= obj3lst[0][1]+" "+i[1] # appends the string to the subject
#                 count=obj3lst[0][0]+1
#                 allavail.append([count,finstr]) # appends the string to the list of simple sentences
# #                 print(finstr)
#                 empsubjlst.remove(i)
            for i in empsubjlst:
                finstr= subj3lst[0][1]+" "+i[1] # appends the string to the subject
                count=subj3lst[0][0]+1
                allavail.append([count,finstr]) # appends the string to the list of simple sentences
#                 print(finstr)
                empsubjlst.remove(i) # removes the string from the incomplete sentence list
        while len(onlyobjlst)!=0:
            # For normal rule2 usecase
            # extract finds the most recently used string
            # appends to that string the object
            # removes the incomplete clause and adds the complete simple sentence to the
            # list of simple sentences.
            extract = len(allavail)-1
#             print(extract,len(allavail))
            subj3lst,obj3lst,verb3lst,cc3lst = get_it_all_spacy(allavail[extract][1])
            objlen=len(obj3lst)-1
            prestr = allavail[extract][1].replace(obj3lst[objlen][1],"")
        #     print(prestr)
            for i in onlyobjlst:
                finstr = prestr+" "+i[1]
                count=allavail[extract][0]+1
                allavail.append([count,finstr])
#                 print(finstr)
                onlyobjlst.remove(i)
        while len(onlysubjlst)!=0:
            # When only subject exists:
            # This is the reverse rule2 case:
            # gets the next complete sentence between which the subject exists.
            # appends this subject to the predicate and object of the corresponding found sentence
            # appends the final simple complete sentence to list of complete sentences
            # removes the incomplete sentence/ subject from the onlysubjlist.
            for i in onlysubjlst:
                extract = i[0]+1
                for j in range(len(allavail)):
                    if allavail[j][0] == extract:
                        extract = j
                        break
#                 print(extract)
                subj3lst,obj3lst,verb3lst,cc3lst = get_it_all_spacy(allavail[extract][1])
                subjlen = len(subj3lst)-1
                prestr = allavail[extract][1].replace(subj3lst[subjlen][1],"")
                finstr = i[1]+" "+prestr
                count=allavail[extract][0]+1
                allavail.append([count,finstr])
#                 print(finstr)
                onlysubjlst.remove(i)
        return (allavail)
    except:
#         print(sys.exc_info())
        pass
    
# Rule 1 check
def main(sen,fw):
    subjlst,objlst,broke,check = rule_1(sen)
#     print("\n------\n")
    ## Check denotes whether the sentence is already simple or not.
    if(check):
        fw.write(sen)
        for i in broke:
            fw.write(sen)
        #fw.write("\n----\n")
        return
    ## The following lists are used to segregate rule 1 complete/incomplete..
    ## if incomplete then prepares data for rule2 and 3
    allavail = list()
    empsubjlst = list()
    empobjlst = list()
    empverblst = list()
    onlyobjlst = list()
    onlysubjlst = list()
    count=0;
    total = len(broke)
    for i in broke:
        ## Checks all sentences of the conjunction broke sentences.
        subj=1;
        verb=1;
        obj=1;
        count+=1
        ## The following line gets the broken sentence's predicate subject and object.
        subj2lst,obj2lst,verb2lst,cc2lst = get_it_all_spacy(i.strip())
        #print("New stripped sentence = ",subj2lst,obj2lst,verb2lst,cc2lst)
        #print("Origial sentence connotation= ",subjlst,objlst)
        ## if no subject: turn variable of subj 0 to denote.. no subject.
        if len(subj2lst)==0:
            subj=0
            if len(obj2lst)!=0:
                ## it is possible that object of the sentence may not be an object in the
                ## original sentence before breaking by conjunction instead could be a subject
                ## in such case it finds the whether subject or object of original sentence
                ## and makes subj variable 1 and obj variable 0
                if any(obj2lst[0][1] in ls for ls in subjlst):
                    print("Check",obj2lst[0][1],subjlst)
                    subj=1
                    obj=0
        if len(obj2lst)==0:
            obj=0;
            ## Similarly performs similar checking for subject of the sentence and makes
            ## necessary variables show it.
            if len(subj2lst)!=0:
                if any(subj2lst[0][1] in ls for ls in objlst):
                    print("Check",subj2lst[0][1],objlst)
                    subj=0
                    obj=1
        ## If there is no verb in the sentence.. in case of dependent clauses.
        if verb2lst[0][1]=="VBab":
            verb=0;
        if subj==0 and verb!=0 and obj!=0:
            ## empsubjlst is for the dependant clauses.. - rule 3
            empsubjlst.append([count,i])
        if subj==0 and verb==0 and obj!=0:
            ## onlyobjlst is for the independant clauses -- rule2
            onlyobjlst.append([count,i])
        if subj!=0 and verb!=0:
            ## allavail -- clauses that are simple and independent
            lstnew = list()
            it = i
            try:
                if verb2lst[0][0]==1:
                    lstnew = i.split()
                    temp = lstnew[0]
                    lstnew[0]=lstnew[1]
                    lstnew[1] = temp
                    i=""
                    for word in lstnew:
                        i+=word+ " "
                print(i)
            except:
                i = it;
            allavail.append([count,i])
        if subj!=0 and verb==0 and obj==0:
            ## For reverse rule 2 case where only subject exists in the dependant clause.
            onlysubjlst.append([count,i])
        print(empsubjlst,onlysubjlst,onlyobjlst,allavail)
    # Check for case in Rule2 or Rule3:
    if len(broke)==len(allavail):
        fw.write(sen)
        for i in allavail:
            print(re.sub(' +', ' ',i[1]).strip())
            fw.write("\t"+re.sub(' +', ' ',i[1]).strip()+"\n")
        #fw.write("\n-----\n")
    else:
        try:
            allavail = rule_2_3(empsubjlst,allavail,onlyobjlst,onlysubjlst)
            #fw.write(sen+"\n")
            for i in allavail:
                print(re.sub(r'\b(.+)\s+\1\b', r'\1', re.sub(' +', ' ',i[1]).strip()))
                fw.write(+re.sub(r'\b(.+)\s+\1\b', r'\1', re.sub(' +', ' ',i[1]).strip()))
            #fw.write("\n-----\n")
        except:
            fw.write(sen)
            #print(sys.exc_info()[0])
            #fw.write("\tAlready Simple\n")
            #fw.write("\n-----\n")
def sep_semi(input):
    rw = open(input)
    fw = open("tempoutput.txt","w")
    for line in rw:
        line = re.sub("[^\P{P}\.;]|","",str(nlp(line)))
        fw.write(line)
#         r = line.split(". ")
#         for i in r:
#             if i==" ":
#                 r.remove(i)
# #         fw.write(line+"\n")
#         if(len(r)!=0):
#             for i in r:
#                 fw.write(i+"\n")
    rw.close()
    fw.close()
    rw = open("tempoutput.txt")
    lst = list()
    for line in rw:
        lst.append(line.split(";"))
    rw.close()
    rw = open("tempoutput.txt","w")
    for i in lst:
        if(len(i)>1):
            for sep in i:
                rw.write(sep.strip())
                rw.write("\n")
        else:
            rw.write(i[0])
#                 print(sep.strip())
    fw.close()
    rw.close()
    nlp = spacy.load("en_core_web_sm")
from spacy.lang.en import English
inp=input("Enter the location of the input file: ")
with open(inp, 'r', encoding='utf-8') as file:
    text = file.read()
#breaking a text into sentences
nlp=English()
nlp.add_pipe('sentencizer')
doc = nlp(text)
sentences = [sent.text.strip() for sent in doc.sents]
#print('Count:',len(sentences))
out=open("cox_output.txt","w")
for sent in sentences:
    checkComplex(sent,out)
out.close()
sep_semi('/content/cox_output.txt')
rw = open("tempoutput.txt")
fw = open("output.txt","w")
for i in rw:
    main(i,fw)
rw.close()
fw.close()
from rouge import Rouge

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def compute_rouge(system_file, reference_file):
    system_summary = read_file(system_file)
    reference_summary = read_file(reference_file)

    rouge = Rouge()
    score = rouge.get_scores(system_summary.strip(), reference_summary.strip())
    return score[0]

def print_rouge_scores(scores):
    for rouge_type, metrics in scores.items():
        print(f"{rouge_type.upper()} scores:")
        print(f"  F1-score: {metrics['f']:.4f}")
        print(f"  Precision:d {metrics['p']:.4f}")
        print(f"  Recall: {metrics['r']:.4f}")
        print()
system_file = 'output.txt'
reference_file = 'New_randomcoco_out.txt'
scores = compute_rouge(system_file, reference_file)
print_rouge_scores(scores)