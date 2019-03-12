# a competle process of dealing with dataset
from PAAfunction import Produce_I_Users,Produce_U_Items
from PAAfunction import Item_Degree_Medium,Item_Degree_Average
from sklearn.model_selection import train_test_split
from Index_data import index_data
import re,os,random
def filter_sample_user(dirname,filename,degree_threshold,filetype):  #easy to read
    user_items_ch=dict()
    links=0
    File_write=open(dirname+'\\'+filename+str(degree_threshold),'w')
    
    lujing=dirname+'\\'+filename                                                
    user_items,user_degree=Produce_U_Items(lujing,filetype)   #chang here if the positions of user and items is exchanged

    for u in user_items:
        if user_degree[u]>=degree_threshold:
            user_items_ch[u]=user_items[u]

    for u,items in user_items_ch.items():                  
        for item in items:
            links+=1  
            File_write.write(u+' '+item+' 1\n')
    File_write.close()
   
    return filename+str(degree_threshold)
def filter_one_degree_item(dirname,filename,filetype,writename):
    lujing=dirname+'\\'+filename
#    na=re.compile(r'(.*?)?(\\)(.*)')
#   mo=na.search(filename)

    houzhui=re.compile(r'(\w*)(.*)')
    hz=houzhui.search(filename)
    print(hz.groups())
    user_items,user_degree=Produce_U_Items(lujing,filetype)
    item_users,item_degree=Produce_I_Users(lujing,filetype)
    print(len(user_items))
    
    for i in item_degree:
        if item_degree[i]==1:                #if u want no 1-item ,  modify here
            for u in item_users[i]:
                user_items[u].remove(i)
                user_degree[u]-=1
    for u in user_degree:                      
        if user_degree[u]<=0:
            del user_items[u]                              # in next for iteration , won't be written
   # file=open('Q:\\datasets3\\'+mo.group(1)+'\\Sone'+mo.group(3),'w')
    file=open(dirname+'\\'+writename,'w')
    print(len(user_items))
    for u,items in user_items.items():
        
        for item in items:
            file.write(u+' '+item+' 1\n')
    file.close()
 
    
def Split_DataSet(dirname,filename):
    file=open(dirname+'\\'+filename,'r')           #remember the suffix
    content=file.readlines() 
    houzhui=re.compile(r'(\w+)(.*)')    
    hz=houzhui.search(filename)

    for i in range(1,6):
        fsample=open(dirname+'\\'+hz.group(1)+'_train'+str(i)+'.txt','w')
        fs=open(dirname+'\\'+hz.group(1)+'_test'+str(i)+'.txt','w')
        train,test = train_test_split(content, test_size = 0.2)
        for length in range(len(train)):
       #     fsample.write(train(length)+'\n')     #'list' object is not callable 
            fsample.write(train[length])                                                # train and test contains '\n'
        for length in range(len(test)):
            fs.write(test[length])
        index_data(dirname+'\\'+hz.group(1)+'_train'+str(i)+'.txt',1)
        fsample.close()
        fs.close()
    file.close() 
def Random_Select(dirname,Filename,samplesize):
    #random selecrt the samplesize of data from object dataset.
    file_lujing=dirname+'\\'+Filename
    File=open(dirname+'\\'+Filename+'_'+str(samplesize),'w')
    user_items,user_degree=Produce_U_Items(file_lujing,1)
    users=random.sample(user_items.keys(),samplesize)
    for user in users:
        for item in user_items[user]:
                File.write(user+' '+item+' 1\n' )
    return Filename+'_'+str(samplesize)
def sprocess_dataset(lujing,file_writename,filetype,degree_threshold,samplesize):   #degree_threshold means user_degree ,those less than this will be deleted
    dirname=os.path.dirname(lujing)
    filename=os.path.basename(lujing)
    print(dirname,filename)
    index_data(lujing,filetype)
    Fn=filter_sample_user(dirname,filename,degree_threshold,filetype) 
  #  Rn=Random_Select(dirname,Fn,samplesize)  # neglect here if any sampling is unneeded
    filter_one_degree_item(dirname,Fn,1,file_writename)         #may not here , only for recommender process it self
    
    index_data(dirname+'\\'+file_writename,1)
    Split_DataSet(dirname,file_writename)

sprocess_dataset('Q:\\ml1m_without1\\ml','ml.txt',1,0,50000)
#filter_one_degree_item('Q:\\ml1m_without1','ml',1,'ml0.txt')
    

