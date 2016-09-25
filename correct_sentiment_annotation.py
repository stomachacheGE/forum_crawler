import numpy as np

# initialize array for storing data
number_data = 338
data = {"id": np.empty([2, number_data], dtype="int32"),
       "thread_id": np.empty([2,number_data], dtype="int32"),
       "sentiment": np.empty([2,number_data], dtype="int32"),
        "whoposts": np.empty([2,number_data], dtype="str"),
       "post_body": np.empty([2,number_data], dtype=object)}

# read annotations from .csv file
import csv
files = ['data/need_correction_posts_excel_deleted.csv', 'data/need_correction_posts_excel_1_deleted.csv']
for i in range(len(files)):
    with open(files[i]) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            # exclude the first row, which are column names
            if count != 0:
                #print("Current line:",count)
                data['id'][i, count-1] = count
                data['thread_id'][i, count-1] = row[0]
                data['sentiment'][i, count-1] = row[1]
                data['whoposts'][i, count-1] = row[2]
                data['post_body'][i, count-1] = row[3]
                #if count<10:
                    #print(row[3])
                    #print(data['post_body'][i, count-1])
            count += 1

def validate(data):
    temp = np.copy(data)
    comp = temp[0,:]!=temp[1,:]
    return np.where(comp)

distinct_id = validate(data['id'])
#print(distinct_id)
if distinct_id[0].size:
    print("Error! There are ", distinct_id[0].size," ids not the same:")
    print("They are:")
    print(data['id'][distinct_id])
    exit(1)

distinct_thread_id = validate(data['id'])
#print(distinct_thread_id)
if distinct_thread_id[0].size:
    print("Error! There are ", distinct_thread_id[0].size," thread_ids not the same:")
    print("They are:")
    print(data['thread_id'][distinct_thread_id])
    exit(1)

# transform the sentiment data so that computeKappa takes it as argument
temp = np.copy(data['sentiment'].T)
#print(temp)
#temp[:,0] = np.random.randint(2,size=temp.shape[0])
#temp[300:,0]=1
comp = temp[:,0]!=temp[:,1]
print("There are ", sum(comp)," annotations not the same:")
print("Indexes are:")
print(data['id'][0,np.where(comp)]+1)
sentiment = np.empty((number_data,2),dtype="int")
sentiment[:,0] = np.sum(temp==0, axis=1)#number of "negative" annotations
sentiment[:,1] = np.sum(temp==1, axis=1)#number of "positive" annotations

input('Press any key to continue to correct the disagreements...')

indexes = np.where(comp)[0]
for index in indexes:
    print('\n\n\n')
    print(data['post_body'][0,index])
    print('\n\n')
    print('Moritz:%d\n' % data['sentiment'][1,index])
    print('Liangcheng:%d\n' % data['sentiment'][0,index])
    while True:
        try:
            var = int(input('Type sentiment for this post (0=negative, 1=positive): \n'))
            if var!=0 and var!=1:
                raise(ValueError)
        except ValueError:
            print("Sorry, please only type 0 or 1.")
            continue
        else:
            break

    data['sentiment'][0,index] = var
    np.save('data/correction_record_sentiment', data['sentiment'][0,:])

print('Now let us correct patient/relative information... \n')

temp = np.copy(data['whoposts'].T)
comp = temp[:,0]!=temp[:,1]
print("There are ", sum(comp)," annotations not the same:")
print("Indexes are:")
print(data['id'][0,np.where(comp)]+1)
whoposts = np.empty((number_data,2),dtype="str")
whoposts[:,0] = np.sum(temp=='P', axis=1)#number of "negative" annotations
whoposts[:,1] = np.sum(temp=='R', axis=1)#number of "positive" annotations

input('Press any key to continue to correct the disagreements...')

indexes = np.where(comp)[0]
for index in indexes:
    print('\n\n\n')
    print(data['post_body'][0,index])
    print('\n\n')
    
    while True:
        try:
            var = input('Type "who posts" information for this post (P=patient, R=relative): \n')
            if var!='P' and var!='R':
                raise(ValueError)
        except ValueError:
            print("Sorry, please only type P or R.")
            continue
        else:
            break
    data['whoposts'][0,index] = var
    np.save('data/correction_record_whoposts', data['whoposts'][0,:])

# save to a file
with open('data/corrected_posts_delete.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(["thread_id","sentiment","who posts","post body"])
    for idx in range(0,number_data) :
        spamwriter.writerow([data['thread_id'][0,idx],data['sentiment'][0,idx],data['whoposts'][0,idx],data['post_body'][0,idx]])

