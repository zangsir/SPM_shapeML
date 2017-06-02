CMN_mapping/readme.txt
=======================
pipeline for doing network filtering and shape ML

1. build entire networks for a particular tone n-gram[The status of these data are indicated in 'README of network analysis'. Basically in subdata or core_subdata (core subdata without neutral tone) we have .csv file (a subset of the entire trigram csv, for example,all data that is '213' ) and .pkl file (this is a fully connected graph). Therefore, fully connected graphs are built for all subdata trigrams and bigrams. ]


2. apply the CC and thresholding and community detection to derive a unweighted network with communities for each n-gram. 
[so far at 5/30 we've only built five of these for five ngrams. we need to build everything - this will be time and energy consuming. This is done using threshold_CC.py. The community(partition) pickled file is indicated by "_pkl_part.pkl" ending. currently we have five of them stored under core_subdata]
[when you are doing the thresholding, make sure you adjust the experimenting threshold values to fit the data, for instance, for ngrams I've used [1,1.5,2,2.5,3,3.5,4,4.5],but for unigram I've used [0.2,0.4,0.6,0.8]. ]
[we have plotted both example communit graphs and the evolution of the CCs between threshold and random network. Include it in your writing under network_analysis/shape_clust/plots/]


3. then we need to write the partition classes into a class file, indicating the entire time-series and metadata and then the class according to community label. In this process smaller communities are ommitted and we're left with large classes. This process of writing class files is done in network_analysis2.ipynb and will result in files that end with "_pkl_part_class.csv"

4. then we need to map the shape class file onto text domain and extract feature from the merged conll format. All conll files for all speaker texts should be already processed and produced. use build_training.py to do the feature extraction given a shape class csv file. If you need to develop this code more, read the original documentation when developing the ML, mapping_plan.txt. 