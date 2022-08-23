# SeekTruth.py : Classify text objects into two categories
#
# User-Ids - adisoni-nsadhuva-svaddi, Names- Aditi Soni, Nidhi Sadhuvala, Sriniavas Vaddi
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

#Implementation of classifier
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    bag_of_words = {}
    
    # set of special characters
    # removing them can help the classier get better
    
    spl = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=',
     ']', '!', '>', ';', '?', '#', '$', ')', '/'}
   
    # while numbers do contribute towards a better classification, they may also falsely influence the classification
    nums = "1234567880"
    
    for i in range(len(train_data["objects"])-1):
        
        for c in spl:
            if c in train_data["objects"][i]:
                train_data["objects"][i] = train_data["objects"][i].replace(c," "+c+ " ")
        for numbers in nums:
            train_data["objects"][i] = train_data["objects"][i].replace(numbers," ")
        
        # this part of the code is to generate bag of words, which will have the word and its respective counts in truthful and deceptive sentences
        for j in train_data["objects"][i].lower().strip().split():
            if j.strip()=="":
                continue
            if j.strip() in bag_of_words and train_data["labels"][i]=="truthful":
                t,f=bag_of_words[j.strip()]
                bag_of_words.update({j.strip():(t+1,f)})
            elif j.strip() in bag_of_words and train_data["labels"][i]=="deceptive":
                t, f = bag_of_words[j.strip()]
                bag_of_words.update({j.strip(): (t, f+1)})
            elif j.strip() not in bag_of_words and train_data["labels"][i] == "truthful":
                bag_of_words.update({j.strip(): (1,0)})
            elif j.strip() not in bag_of_words and train_data["labels"][i] == "deceptive":
                bag_of_words.update({j.strip(): (0,1)})
            else:
                continue
     
    fin_probs = {}
    
    #generating probabilities for bag of words 
    for i in bag_of_words:
        t,f=bag_of_words[i]
        fin_probs.update({i:((t/(t+f)), (f/(t+f)))})
    fin = []
    
    # calculating the probability of truthful and deceptive sentences in the given train data     
    pt_train = train_data["labels"].count("truthful")/(train_data["labels"].count("truthful")+train_data["labels"].count("deceptive"))
    pf_train = train_data["labels"].count("deceptive")/(train_data["labels"].count("truthful")+train_data["labels"].count("deceptive"))
    
    #Prediction of class objects 
    for i in test_data["objects"]:
        # cleaning the reviews         
        for c in spl:
            i = i.replace(c," "+c+" ")
        for numbers in nums:
            i = i.replace(numbers," ")
        
        pa = pt_train
        pb = pf_train
        
        for j in i.lower().strip().split():
            
            # ignoring the words unfound in the training data
            # while we have tried text similarity, laplace smoothening
            # the complexity of the entire code increases multifold             
            if  j.strip() not in list(fin_probs.keys()):
                continue
            else:
                x,y = fin_probs[j.strip()]
                if x!=float(0):
                  pa*=x
                if y!=float(0):
                  pb*=y
        # checking the bayesian threshold         
        if pa/pb>1:
            fin.append("truthful")
        else:
            fin.append("deceptive")
    # returning the labels     
    return  fin


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.

    train_data = load_file(train_file)
    test_data = load_file(test_file)

    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
