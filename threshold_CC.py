import pickle
import networkx as nx
import community
import matplotlib.pyplot as plt
import numpy as np
from random import choice
import time
from os import listdir
import random,os

def randomize_graph(g, NSwap):
    while NSwap > 0:
        node_1 = choice(g.nodes())
        node_2 = choice(g.nodes())
        if g.has_edge(node_1,node_2):
            continue
        #select a neighbor of node_1 
        node_1n = choice(g[node_1].keys())
        if g.has_edge(node_1n, node_2):
            continue
        node_2n = choice(g[node_2].keys())
        if g.has_edge(node_1n, node_2n):
            continue
        if g.has_edge(node_1, node_2n):
            continue
        #now we need to cut edges (node_1,node_1n), (node_2,node_2n) and reconnect (node_1, node_2), (node_1n,node_2n)
        g.add_edge(node_1,node_2)
        g.add_edge(node_1n,node_2n)
        g.remove_edge(node_1,node_1n)
        g.remove_edge(node_2,node_2n)
        NSwap-=1
    return g




def threshold_experiment(G_fully_connected,threshold):
    
    esmall=[(u,v) for (u,v,d) in G_fully_connected.edges(data=True) if d['weight'] <=threshold and d['weight']>0.01]
    print "num edges left:",len(esmall)

    H=nx.Graph(esmall)
    H_rand=randomize_graph(H,len(esmall))
    H_ori=nx.Graph(esmall)
    #print 'average thresholded cc:'+str(nx.average_clustering(H_ori))
    #print 'average random cc:'+str(nx.average_clustering(H_rand))
    try:
        thres_cc=nx.average_clustering(H_ori)
        rand_cc=nx.average_clustering(H_rand)
        return thres_cc,rand_cc
    except ZeroDivisionError:
        print 'zero division error'
        #continue
    


def run_threshold_exp(pfile):
    #loading
    print 'loading graph...'
    start_time = time.time()
    #pfile='subdata/downsample_syl_2_meta_100_11.pkl'
    G = nx.read_gpickle(pfile) 
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print 'experimenting with CC...'
    all_thres_cc=[]
    all_rand_cc=[]
    #threshold_options=[1.5,2,2.5,3]
    threshold_options=np.arange(1,5,0.5)
    for thres in threshold_options:
        print thres,
        tcc,rcc=threshold_experiment(G,thres)
        all_thres_cc.append(tcc)
        all_rand_cc.append(rcc)

    #print all_thres_cc, all_rand_cc
    diff=np.array(all_thres_cc)-np.array(all_rand_cc)
    best_threshold=threshold_options[np.argmax(diff)]
    print 'best_threshold:',best_threshold


    #plot evolution of threshold
    plotting=False
    if plotting:
        print 'plotting evolution of CC...'
        plt.figure()
        plt.plot(threshold_options,all_thres_cc,'o-',label='thresholded network CC')
        plt.plot(threshold_options,all_rand_cc,'x-',label='randomized network CC')
        plt.plot(threshold_options,diff,'>-',label='CC difference')
        plt.plot((best_threshold,best_threshold),(0,0.9),'r')
        plt.legend()
        plt.title('Evolution of clustering coefficients for bigram 100p 0-1 dataset')
        plt.xlabel('Threshold')
        evolution_plot_name = pfile.replace('.','_') + '_CC.pdf'
        plt_path='plots/'
        plt.savefig(plt_path+evolution_plot_name)



    #let's apply best_threshold and derive the final unweighted network

    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=best_threshold and d['weight']>0.1]
    print len(esmall)
    H=nx.Graph(esmall)
    print 'average cc:'+str(nx.average_clustering(H))

    #community detection
    print 'community detection...'
    part = community.best_partition(H)
    #mod = community.modularity(part,H)
    if plotting:
        plt.figure(num=None, figsize=(15, 12), dpi=120, facecolor='w', edgecolor='k')
        #plot, color nodes using community structure
        values = [part.get(node) for node in H.nodes()]
        nx.draw_spring(H, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=True)
        commu_plot_name = pfile.replace('.','_') + '_community.pdf'
        plt.savefig(plt_path+commu_plot_name)
    pickle_path='community_partition/'
    partition_pickle_file=pfile.replace('.','_') + '_part.pkl'
    pickle.dump(part,open(pickle_path+partition_pickle_file,'w'))


def main():
    random=False
    subdata_path='core_subdata/'
    #subdata_path='subdata/'
    pickle_path='community_partition/'
    end_string='pkl'
    #this will take the pickled graphs as input, and will generate and serialize a community partition pickle file as output.

    #doing tone recognition task
    #subdata_path='tone-rec-network/'
    #end_string='gpickle'

    subdata_pkls = [ f for f in listdir(subdata_path) if f.endswith(end_string)]
    print 'total num of files:', len(subdata_pkls)
    if random:
        num_random=5
        subdata_pkls = random.sample(subdata_pkls,num_random)
        print 'random test:',subdata_pkls


    for pfile in subdata_pkls:
        partition_pickle_file=pfile.replace('.','_') + '_part.pkl'
        if os.path.isfile(pickle_path+subdata_path+partition_pickle_file):
            print 'skipped file '+ pfile
            continue
                         
        print "+++++++++++++++++++++++++++++++++++++++++++++++"
        print pfile
        try:
            run_threshold_exp(subdata_path+pfile)
        except:
            continue
        


if __name__ == '__main__':
    main()


