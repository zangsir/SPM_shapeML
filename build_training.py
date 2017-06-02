from feature_extr_modules import *
import sys,pickle
import csv
import re

def parse_phons_file(phons_file):
    """read a phons file and return a list of vowels that carry tone marks"""
    all_lines=open(phons_file,'r').read().split('\n')
    all_nuclear=[]
    for l in all_lines:
        if l!="":
            line=l.split(' ')
            m = re.search(r'\d+$', line[-1])
            if m:
                all_nuclear.append(line[-1])
    return all_nuclear


def expand_vowel_features(vowel_features):
    #is_nasal,is_dipthong,is_high,is_low,is_front,is_back,is_round
    #7*N features, N as in N-gram
    feature_vectors=[]
    for f in vowel_features:
        vec=[is_nasal(f),is_dipthong(f),is_high(f),is_low(f),is_front(f),is_back(f),is_round(f)]
        feature_vectors.extend(vec)
    return feature_vectors



def extract_phons_feature(ngram,phons_path):
    "given a ngram line, extract phonological features"
    #features: nuclear of all vowels in the ngram; (2 or 3)
    #features: previous and following tone mark of the ngram; (2)
    ngram_list=ngram.split(',')
    tones=ngram_list[-4]
    fname=ngram_list[-2].split('/')[1].split('_')[0]
    syl_ids=ngram_list[-1].split('_')
    #phons_path='text_cmn/data/'
    phons_file=fname+'.phons'
    all_nuclear=parse_phons_file(phons_path+phons_file)
    #this is a list of all nuclears
    vowel_features=[all_nuclear[int(i)][:-1] for i in syl_ids]
    #print vowel_features
    #print all_nuclear
    evf=expand_vowel_features(vowel_features)

    #prev, next tones
    try:
        prev_tone=all_nuclear[int(syl_ids[0])-1][-1]
    except:
        prev_tone=-1
    try:
        next_tone=all_nuclear[int(syl_ids[-1])+1][-1]
    except:
        next_tone=-1
    evf.extend([prev_tone,next_tone])
    return evf

def get_data_label(ngram_file):
    lines=open(ngram_file,'r').read().split('\n')
    all_data,all_label=[],[]
    for l in lines:
        if l=='':
            continue
        line=l.split(',')
        data=line[:-1]
        label=line[-1]
        all_data.append(data)
        all_label.append(label)
    return all_data,all_label


def build_train(ngram_file,N,phons_path):
    """given one ngram_file, return a matrix of features and including label"""
    all_data,all_label=get_data_label(ngram_file)
    all_features=[]
    for i in range(1,len(all_data)):
        data=all_data[i]
        label=all_label[i]
        ngram_line=','.join(data)
        #print ngram_line[-4:]
        features=feature_extractor(ngram_line,N)
        phons_features=extract_phons_feature(ngram_line,phons_path)
        features.extend(phons_features)
        features.append(label)
        all_features.append(features)
    return all_features




def main():
    #f='shape_class_csv/downsample_syl_3_meta_200_134_pkl_part_class.csv'
    shape_class_path='shape_class_csv/'
    phons_path='text_cmn/data/'
    shape_class_files=[f for f in listdir(shape_class_path) if f.endswith('_class.csv')]
    #print shape_class_files
    for f in shape_class_files:
        print f
        N=int(f.split('downsample_syl_')[1][0])
        train_data=build_train(shape_class_path+f,N,phons_path)
        outfile=f.replace('pkl_part_class.csv','train.pkl')
        pickle.dump(train_data,open(outfile,'w'))
        outcsv=f.replace('pkl_part_class.csv','.csv')
        trigram_features='pos1,pos2,pos3,func1,func2,func3,starting_pitch,ending_pitch,sent_position,is_entity,tok_bound1,tok_bound2,tok_bound3,singleton,is_nasal1,is_dipthong1,is_high1,is_low1,is_front1,is_back1,is_round1,is_nasal2,is_dipthong2,is_high2,is_low2,is_front2,is_back2,is_round2,is_nasal3,is_dipthong3,is_high3,is_low3,is_front3,is_back3,is_round3,prev_tone,next_tone,label'

        bigram_features='pos1,pos2,func1,func2,starting_pitch,ending_pitch,sent_position,is_entity,tok_bound1,tok_bound2,singleton,is_nasal1,is_dipthong1,is_high1,is_low1,is_front1,is_back1,is_round1,is_nasal2,is_dipthong2,is_high2,is_low2,is_front2,is_back2,is_round2,prev_tone,next_tone,label'
        if N==3:
            features=trigram_features
        if N==2:
            features=bigram_features

        feature_list=features.split(',')
        with open(outcsv, 'wb') as f:
            csv.writer(f).writerow(feature_list)
            csv.writer(f).writerows(train_data)
        #print "Len: ",len(train_data)
        #print "data3: ", train_data[3]
        #print 'data2: ', train_data[2]
        #sys.exit()



if __name__ == '__main__':
    main()



