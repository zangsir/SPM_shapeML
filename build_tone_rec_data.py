import sys
from collections import defaultdict
import random



def read_csv(input_file,num_meta):
    f=open(input_file,'r').read().split('\n')
    outfile=input_file.split('.csv')[0]+'_np.csv'
    data,label,all_data=[],[],[]
    for line in f:
        if line!='':
            dl=line.split(',')
            #dl=[float(i) for i in dl]
            d=line.split(',')[:num_meta]
            #d=[float(i) for i in d]
            l=line.split(',')[num_meta:]
            data.append(d)
            assert len(l)==1
            label.append(l[0])
            all_data.append(dl)
            
            
    return data,label,all_data


#output_path='tone_rec_test_data/'
def serialize_data(test_data,dataset):
    if len(test_data[0])==30:
        print 'len of data is:',len(test_data[0])
        output_file=dataset.replace('.csv','_subset.csv')
    else:
        print 'len of data is:',len(test_data[0])
        output_file=dataset.replace('.csv','_subset_wlabel.csv')
    f=open(output_file,'w').close()
    f=open(output_file,'a')
    for i in test_data:#no label only data, this is for conveniently compute distance matrix later in graph
        f.write(','.join(i)+'\n')
    f.close()


def build_dataset(n,path,dataset):
    #n is the number of samples from each tone category
    data,label,alldata=read_csv(dataset,-1)

    #divide data into tone subsets (with label)
    tone_dict_wlabel=defaultdict(list)
    for tone in set(label):
        if tone=='6':
            continue
        tone_dict_wlabel[tone]=[alldata[i] for i in range(len(alldata)) if label[i]==tone]


    #data no label
    #tone_dict=defaultdict(list)
    #for tone in set(label):
     #   if tone=='6':
      #      continue
       # tone_dict[tone]=[data[i] for i in range(len(data)) if label[i]==tone]

    for k in tone_dict_wlabel.keys():
        print k,len(tone_dict_wlabel[k])


    #randomly select n from each tone cat and form a test dataset
    #with label
    test_data_wlabel=[]
    test_data=[]
    for k in tone_dict_wlabel.keys():
        this_data_wlabel=random.sample(tone_dict_wlabel[k],n)
        test_data_wlabel.extend(this_data_wlabel)
        this_data=[i[:-1] for i in this_data_wlabel]
        test_data.extend(this_data)
    #no label    
    


    #write to both data files
    serialize_data(test_data,dataset)
    serialize_data(test_data_wlabel,dataset)



def main():
    path='tone-rec-network/'
    dataset='tone-rec-network/downsample_syl_noneut.csv'
    n=250
    print 'number of samples from each tone cat is ', n
    build_dataset(n,path,dataset)

if __name__ == '__main__':
    main()