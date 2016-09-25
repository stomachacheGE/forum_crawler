
# coding: utf-8

# In[2]:

import numpy as np
import re


# In[3]:

import pickle
def save_obj(obj, name ):
    with open('data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# In[4]:

data = load_obj('posts_training_data')


# In[5]:

features = np.array([list(feature.values()) for feature in data['feature']])
target = data['sentiment']
print(features.shape)


# In[8]:

for key in data['feature'][0].keys():
    print(key)


# In[75]:

from sklearn.grid_search import GridSearchCV
import csv
import os.path
from sklearn import preprocessing
def grid_search(clf, features_dict_list, target, param_grid, cv=None, 
                scoring=None, feature_scaled=False, output=True, output_file=None):
    if not cv:
        cv = 10
    if not scoring:
        scoring = 'accuracy'
    if not output_file:
        output_file = 'data/classifier_selection.csv'
    features = np.array([list(feature.values()) for feature in features_dict_list])
    if feature_scaled:
        features = preprocessing.scale(features)
    feature_names = ', '.join(features_dict_list[0].keys())
    gs_clf = GridSearchCV(estimator=clf, param_grid=param_grid,
                   n_jobs=-1, cv=cv,scoring=scoring,verbose=10)
    gs_clf.fit(features, target)
    grid_scores = gs_clf.grid_scores_
    # write training data to .csv
    file_exist = os.path.isfile(output) 
    if not file_exist and output:
        with open(output_file, 'w') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["classifier", "parameters", "features", "feature_scaled", 
                             "cv", "avg_accuracy", "std_accuracy"])
            for score in grid_scores: 
                params = score[0]
                avg_accuracy = score[1]
                std_accuracy = np.std(score[2])
                writer.writerow([type(clf).__name__, params, feature_names,
                                 feature_scaled, cv, avg_accuracy, std_accuracy])
    elif file_exist and output:
        with open(output_file, 'a') as csvfile:
            writer = csv.writer(csvfile)
            for score in grid_scores: 
                params = score[0]
                avg_accuracy = score[1]
                std_accuracy = np.std(score[2])
                writer.writerow([type(clf).__name__, params, feature_names,
                                 feature_scaled, cv, avg_accuracy, std_accuracy])
    else:
        pass
    print(gs_clf.best_score_)
    print(gs_clf.best_params_)
    return gs_clf


# ### Get subsets of feature dictionary

# In[40]:

from itertools import chain, combinations
def all_subsets(ss):
  return(chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1))))


# # In[42]:

# for subset in all_subsets(data['feature'][0].keys()):
#   print(list[sub])


# In[46]:

subsets_tuple = all_subsets(data['feature'][0].keys())
subsets = [subset for idx, subset in enumerate(subsets_tuple)]
subsets.pop(0)



# ### SVM

# In[62]:

# from sklearn import svm
# Cs = np.logspace(-1, 2, 10)
# gammas = [0.001, 0.0001]
# svc = svm.SVC(probability=True)
# #clf = grid_search(svc,data['feature'],data['sentiment'],dict(C=Cs))


# # In[63]:

# clf = grid_search(svc,data['feature'],data['sentiment'],dict(C=Cs), cv=5, feature_scaled=True,output=False)


# # In[58]:

# for subset in subsets:
#     subset_feature = []
#     for feature in data['feature']:
#         subset_feature.append({k:feature[k] for k in subset})
#     subset_feature = np.array(subset_feature)
#     print(subset)
#     grid_search(svc,subset_feature,data['sentiment'],dict(C=Cs))
#     grid_search(svc,subset_feature,data['sentiment'],dict(C=Cs),cv=5)
#     grid_search(svc,subset_feature,data['sentiment'],dict(C=Cs),feature_scaled=True)
#     grid_search(svc,subset_feature,data['sentiment'],dict(C=Cs),cv=5,feature_scaled=True)


# # In[70]:

# clf.predict_proba(list(data['feature'][0].values()))


# ### AdaBoost

# In[77]:

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

base_estimators = [DecisionTreeClassifier(max_depth=1),
                   DecisionTreeClassifier(max_depth=2),
                   DecisionTreeClassifier(max_depth=3)]
n_estimators = np.linspace(1,20,10).astype(int)
# Create and fit an AdaBoosted decision tree
bdt = AdaBoostClassifier(learning_rate = 0.1)


# In[78]:

#clf = grid_search(bdt,data['feature'],data['sentiment'],dict(base_estimator=base_estimators,n_estimators=n_estimators), cv=10, feature_scaled=True,output=False)

for subset in subsets:
    subset_feature = []
    for feature in data['feature']:
        subset_feature.append({k:feature[k] for k in subset})
    subset_feature = np.array(subset_feature)
    print(subset)
    grid_search(bdt,subset_feature,data['sentiment'], output_file = 'data/adaboost_classifier_selection.csv',
                param_grid=dict(base_estimator=base_estimators,n_estimators=n_estimators))
    grid_search(bdt,subset_feature,data['sentiment'], output_file = 'data/adaboost_classifier_selection.csv',
                param_grid=dict(base_estimator=base_estimators,n_estimators=n_estimators),feature_scaled=True)