import pickle
from os import listdir
import codecs
from collections import defaultdict


#is_nasal,is_dipthong,is_high,is_low,is_front,is_back,is_round

def is_nasal(nuclear):
    if 'n' in nuclear:
        return 1
    return 0

def is_high(x):
    high=set(['i','v','u'])
    for i in x:
        if i in high:
            return 1
    return 0

def is_low(x):
    low=set(['a'])
    for i in x:
        if i in low:
            return 1
    return 0

def is_dipthong(x):
    f=set(['a','i','e','v','u','o'])
    for i in range(len(x)-1):
        if x[i] in f:
            if x[i+1] in f and x[i]!=x[i+1]:
                return 1
    return 0


def is_front(x):
    f=set(['a','i','e','v'])
    for i in x:
        if i in f:
            return 1
    return 0


def is_back(x):
    f=set(['u','o'])
    for i in x:
        if i in f:
            return 1
    return 0



def is_round(x):
    f=set(['o','u','v'])
    for i in x:
        if i in f:
            return 1
    return 0


def parse_conll(conll_file):
    """returns a dictionary from sentence id to the rows of conll files belonging to that sentence"""
    f=open(conll_file,'r').read().split('\n')
    cdict=defaultdict(list)
    clist=[]
    for line in f:
        if line.startswith('#') or line=='':
            continue
        l=line.split('\t')
        clist.append(l)
    for line in clist:
        sent_id=line[0]
        #print sent_id
        cdict[int(sent_id)].append(line)
    return cdict

#after you found the sentence file (e.g., CHJ00008.txt) you build this map on the fly, 
#so syl 12_13_14 can map to tok id 6,7,8, then you use the map to find the corresponding lines in conll.
def map_syl_tok(tokenized_sent):
    syl2tok={}
    syl_id=0
    tokenized_sent=codecs.decode(tokenized_sent,'utf-8')
    toks=tokenized_sent.split(' ')
    stripped=tokenized_sent.replace(' ','').replace('\n','')
    #print stripped
    num_syl=len(stripped)
    #print num_syl
    #print toks
    for i in range(len(toks)):
        tok_id=i
        tok=toks[i]
        #print tok
        if tok=='' or tok=='\n':
            #print 'skip'
            continue
        for char in tok:
            #print char
            syl2tok[syl_id]=i
            syl_id+=1
            if syl_id>num_syl:
                break    
    return syl2tok



def map_fname_sentID(suffix,path):
    all_txt=[f for f in listdir(path) if f.endswith(suffix)]
    all_speaker=set([s[:3] for s in all_txt])
    print all_speaker
    global_dict={}
    
    for spk in all_speaker:
        sent_id=1
        local_dict={}
        spk_txts=[f for f in all_txt if f.startswith(spk)]
        for i in range(len(spk_txts)):
            local_dict[spk_txts[i]]=sent_id
            sent_id+=1
        global_dict[spk]=local_dict
    return global_dict
        

def reverse_dict(tag_dict):
    rdict={}
    for k,v in tag_dict.iteritems():
        for i in v:
            rdict[i]=k
    return rdict


def map_to_conll(ngram):
    """taking one line of ngram file, map it onto relevant token lines in the target conll file"""
    #for an example of input ngram, see the ngram variable defined above. it is one line from a ngram file, such as 
    #bigram file, where the line is the TS of tone ngrams and then meta attributes
    ngram_list=ngram.split(',')
    tones=ngram_list[-4]
    fname=ngram_list[-2].split('/')[1].split('_')[0]
    syl_ids=ngram_list[-1].split('_')
    
    merge_conll_path='merged_conll/'
    txt_file='text_cmn/data/'+fname+'.txt'
    phons_file='text_cmn/data/'+fname+'.phons'
    fname_ID_map=pickle.load(open('fname_ID_map.pkl','r'))
    conll_merged_file=merge_conll_path+fname[:3]+'_all.txt_merge.conll'

    # TODO:we need a function to verify tones
    sent_id=fname_ID_map[fname[:3]][fname+'.txt']

    # syl to tok id
    tokenized_sentence=open(txt_file,'r').read()
    syl2tok_map=map_syl_tok(tokenized_sentence)
    tok_ids=[syl2tok_map[int(i)] for i in syl_ids]

    # parse conll
    conll_dict=parse_conll(conll_merged_file)

    #get to targeted lines in conll
    target_conll_sentence=conll_dict[sent_id]
    #print target_conll_sentence
    #print 'tok_ids',tok_ids
    target_toks=[target_conll_sentence[i] for i in tok_ids]
    return target_toks, syl2tok_map


#steps: take a ngram (bigram, e.g.) file, then process one line at a time. for each line, convert to text domain token,
#and then extract features.

#we can write a function that extracts feature (a feature extractor) from one line of ngram. 

#pos1,pos2,po3,func1,func2,func3,starting_pitch,ending_pitch,sent_position2, is_entity, tok_bound, 
#has_antecedent, has_anaphor, singleton


def get_pitch_features(ngram_line):
    ngram_list=ngram_line.split(',')
    start_pitch=ngram_list[0]
    end_pitch=ngram_list[-5]
    return start_pitch,end_pitch

def is_entity_unit(entity):
    return 0 if entity=='O' else 1

def is_entity(entity_list):
    for ent in entity_list:
        if is_entity_unit(ent):
            return 1
    return 0


def is_tok_bound(ngram_line,syl2tok_map):
    #basically the first character in a token is always a boundary (following a boundary), the non-firsts are not.
    ngram_list=ngram_line.split(',')
    #tones=ngram_list[-4]
    fname=ngram_list[-2].split('/')[1].split('_')[0]
    syl_ids=ngram_list[-1].split('_')
    txt_file='text_cmn/data/'+fname+'.txt'
    tokenized_sentence=open(txt_file,'r').read()
    tokenized_sentence=codecs.decode(tokenized_sentence,'utf-8')
    untok_sentence=tokenized_sentence.replace(' ','')
    #print tokenized_sentence
    #print untok_sentence
    decisions=[]
    #print syl_ids
    for syl in syl_ids:
        #print syl
        tok=tokenized_sentence.split(" ")[int(syl2tok_map[int(syl)])]
        #print untok_sentence[int(syl)]
        #print tok
        if untok_sentence[int(syl)]==tok[0]:
            bound=1
        else:
            bound=0
        decisions.append(bound)
        
    return decisions
    


def extract_coref_chains(conll_merged_file):
    f=open(conll_merged_file,'r').read().split('\n')
    all_coref=[]
    for line in f:
        if line.strip().startswith('#'):
            continue
        if line.strip()!='':
            l=line.strip().split('\t')
            all_coref.append(l[-1])
    return all_coref
    

    
def has_antecedent(ngram_line,tok_id_spk_list):    
    #tok_id_spk_list is the list of tok_id_spk for the N tokens under consideration
    ngram_list=ngram_line.split(',')
    fname=ngram_list[-2].split('/')[1].split('_')[0]
    conll_merged_file=fname[:3]+'_merge.conll'
    coref_chain=extract_coref_chains(conll_merged_file)
    for tok_id_spk in tok_id_spk_list:
        pass
    
def is_singleton(coref_values):
    for c in coref_values:
        if c!='_':
            return 1
    return 0
    


def feature_extractor(ngram_line, N):
    # N as in N-gram
    # for bigram we'll have pos1 and pos2, for trigram, pos1, 2, 3; so basically we have a variable number of features
    # depending on N
    conll_indexes={'coref':-1,'func':-2,'head':-3,'entity':-4,'pos':-5,'text':3,'sent_id':0,'tok_id_spk':1,\
                   'tok_id_sent':2}

    target_toks, syl2tok_map = map_to_conll(ngram_line)
    assert len(target_toks)==N
    
    #get postag dict to collapse tags
    tagset_dict={'VADJ':['VA','VC','VE','VV'],'NOUN':['NR','NT','NN','PN'],'DETN':['DT','CD','OD'],\
            'OTRO':['LC','M','P','CC','CS','DEC','DEG','DER','DEV','SP','AS','ETC','MSP',   \
                   'IJ','ON','PU','JJ','FW','LB','SB','BA'], 'AD':['AD']}
    rdict=reverse_dict(tagset_dict)
    
    #tok_bound1 means if tok 1 is following a word boundary or is it word-internal(0)
    trigram_features='pos1,pos2,po3,func1,func2,func3,starting_pitch,ending_pitch,sent_position,is_entity,tok_bound1,\
    tok_bound2,tok_bound3,singleton'
        
    bigram_features='pos1,pos2,func1,func2,starting_pitch,ending_pitch,sent_position,is_entity,tok_bound1,tok_bound2,\
    singleton'
    #for now we've ommitted - has_antecedent,has_anaphor,
    pos_features=[i[conll_indexes['pos']] for i in target_toks]
    pos_features=[rdict[i] for i in pos_features]
    func_features=[i[conll_indexes['func']] for i in target_toks]
    func_features=[i.split(':')[0] for i in func_features]
    start_pitch,end_pitch=get_pitch_features(ngram_line)
    sent_position=float(target_toks[0][int(conll_indexes['tok_id_sent'])])/max(syl2tok_map.keys())
    is_ngram_entity=int(is_entity([i[conll_indexes['entity']] for i in target_toks]))
    is_bound=is_tok_bound(ngram_line,syl2tok_map)#this is a group feature, a list of features
    #tok_id_spk_list=[i[conll_indexes['tok_id_spk']] for i in target_toks]
    is_ngram_singleton=is_singleton([i[conll_indexes['coref']] for i in target_toks])#we'll collapse into one singleton feature
    
    features=[]
    features.extend(pos_features)
    features.extend(func_features)
    features.extend([start_pitch,end_pitch,sent_position,is_ngram_entity])
    features.extend(is_bound)
    features.append(is_ngram_singleton)

    return features



