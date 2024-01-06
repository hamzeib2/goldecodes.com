from . util import get_orders_from_text_file,get_orders_category_from_text_file
from .models import *
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def process_association(items):
    this_transaction=set()
    try:
        for item in items:
            if not item.get('product').get('name') == "":
                this_transaction.add(item.get('product').get('name'))
        transactions=get_orders_from_text_file()
    except:
        for item in items:
            if not item.product.name == "":
                this_transaction.add(item.product.name)
        transactions=get_orders_from_text_file()

    final_result = [] 
    consequents_list=[]
    antecedents_list=[]

    try:
        te = TransactionEncoder()
        te_ary =te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary,columns=te.columns_)

        frequent_itemsets = apriori(df,min_support=0.1,use_colnames=True)
        strong_rules  = association_rules(frequent_itemsets,metric="confidence",min_threshold=0.1)
    
        for k in strong_rules['consequents']:
            consequents_list.append(set(k))
        for l in strong_rules['antecedents']:
            antecedents_list.append(set(l)) 

        for index,iitem in enumerate(consequents_list):
            if iitem == this_transaction:
                print(index)
                final_result.append(antecedents_list[index])
    except:
        pass

    print(final_result)

    final_result_set =set()

    if not final_result == []:
        for i in final_result:
                for j in i:
                    final_result_set.add(j)
        print(final_result_set)

    print(consequents_list)
    print(antecedents_list)
    print(final_result_set)
    return final_result_set
######################################################################
def process_association_categories(items):
    this_transaction=set()
    try:
        for item in items:
            if not item.get('product').get('category') == "":
                this_transaction.add(item.get('product').get('category'))
        transactions=get_orders_category_from_text_file()
    except:
        for item in items:
            if not item.product.category == "":
                this_transaction.add(item.product.category)
        transactions=get_orders_category_from_text_file()

    final_result = [] 
    consequents_list=[]
    antecedents_list=[]

    try:
        te = TransactionEncoder()
        te_ary =te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary,columns=te.columns_)

        frequent_itemsets = apriori(df,min_support=0.1,use_colnames=True)
        strong_rules  = association_rules(frequent_itemsets,metric="confidence",min_threshold=0.01)
    
        for k in strong_rules['consequents']:
            consequents_list.append(set(k))
        for l in strong_rules['antecedents']:
            antecedents_list.append(set(l)) 

        for index,iitem in enumerate(consequents_list):
            if iitem == this_transaction:
                print(index)
                final_result.append(antecedents_list[index])
    except:
        pass

    print(final_result)

    final_result_set =set()

    if not final_result == []:
        for i in final_result:
                for j in i:
                    final_result_set.add(j)
        print(final_result_set)

    print(consequents_list)
    print(antecedents_list)
    print(final_result_set)
    return final_result_set


    #if you want to see the results in template"test.html" undo the comment
    # # return render (request,'test.html',{'tran':transactions ,'test1':ex_list1 , 'test2':ex_list2}) 

