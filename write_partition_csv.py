import pickle,os
from collections import defaultdict
import pylab as plt
from os import listdir

def get_clusters(part):
    cluster_assignment=defaultdict(list)
    for k,v in part.iteritems():
        cluster_assignment[v].append(k)
    #print out the length of each cluster
    #for k in cluster_assignment.keys():
        #print k,len(cluster_assignment[k])
    return cluster_assignment



def read_csv_data_meta_unigram(data_file):
    f=open(data_file,'r').read().split('\n')
    all_csv_data=[]
    all_lab=[]
    for line in f:
        if line=='':
            continue
        l=line.split(',')[:-1]
        b=line.split(',')[-1]
        #l=[float(i) for i in l]
        all_csv_data.append(l)
        all_lab.append(b)
    return all_csv_data,all_lab


def read_csv_data_meta(data_file):
    f=open(data_file,'r').read().split('\n')
    all_csv_data=[]
    all_lab=[]
    for line in f:
        if line=='':
            continue
        l=line.split(',')[:-4]
        b=line.split(',')[-4:]
        #l=[float(i) for i in l]
        all_csv_data.append(l)
        all_lab.append(b)
    return all_csv_data,all_lab


def plot_clusters(path,pfile,csv_file):
    #pfile='downsample_syl_3_meta_200_421_pkl_part.pkl'
    #path='core_subdata/'
    part=pickle.load(open(path+pfile,'r'))
    clust=get_clusters(part)
    #csv_file='subdata/downsample_syl_3_meta_200_421.csv'
    ngram=csv_file.split('.')[0].split('_')[-1]
    csvdata,lab=read_csv_data_meta(csv_file)
    #print len(csvdata)
    for j in clust.keys():
        inds=clust[j]
        plt.figure()
        for i in inds:
            #print 'i',i
            
            #print len(csvdata[i])
            plt.plot(csvdata[i])
            plt.title(ngram+"|"+str(j))


def get_classes(path,pfile,csv_file):
    part=pickle.load(open(path+pfile,'r'))
    clust=get_clusters(part)
    ngram=csv_file.split('.')[0].split('_')[-1]
    csvdata,lab=read_csv_data_meta(csv_file)
    all_data=[]
    for key in clust.keys():
        inds=clust[key]
        if len(inds)<50:
            #print 'key excluded:',key
            continue
        for i in inds:
            data=csvdata[i]
            labels=lab[i]
            data.extend(labels)
            data.append(str(key))
            all_data.append(data)
    return all_data
            
            
def write_file(data,pfile):
    outfile=pfile.replace('.pkl','_class.csv')
    f=open(outfile,'w').close()
    f=open(outfile,'a')
    num_col=len(data[0])
    header=[str(i+1) for i in range(num_col-1)]
    header.append('label')
    f.write(','.join(header)+'\n')
    for line in data:
        f.write(','.join(line)+'\n')
    f.close()         
    

def main():
    path='community_partition/core_subdata/'
    pfiles = [ f for f in listdir(path) if f.endswith('_part.pkl')]
    #process all
    for pfile in pfiles:
        print pfile
        outfile=pfile.replace('.pkl','_class.csv')
        if os.path.isfile(outfile):
            print 'skipped file '+ pfile
            continue
        csv_file='subdata/'+pfile.replace('_pkl_part.pkl','.csv')
        d=get_classes(path,pfile,csv_file)
        try:
            write_file(d,pfile)
        except:
            print 'error:skipped file'
            continue


if __name__ == '__main__':
    main()
