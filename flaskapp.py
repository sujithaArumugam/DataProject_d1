from flask import Flask, request #import main Flask class and request object
import pandas as pd
import json
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    df = pd.read_csv ('flights.csv')
    count_nan = df['YEAR'].isnull().sum()
    print ('Count of NaN: ' + str(count_nan))
    dli= list(df.columns.values)
    jsonString = json.dumps(dli)
    return jsonString 


@app.route('/rules', methods=['GET'])
def rule():
    df = pd.read_csv ('flights.csv')
    count_nan = df['YEAR'].isnull().sum()
    data1 = {}
    data1['YEAR'] = 'The column year should not be null'
    data = {}
    data['key'] = json.dumps(data1)
    data['key1'] = json.dumps(data1)
    json_data = json.dumps(data)    
    return json_data 

@app.route('/getrules', methods=['POST']) #GET requests will be blocked
def getrules():
    req_data = request.get_json()
    df = pd.read_csv ('flights.csv')    
    rules=[]
   
    for k in req_data:       
        Dict = {}
        rules_list=[]
        count_nan = df[k].isnull().sum()
        if count_nan == 0:            
            rules_list.append( 'The column '+ k + ' should not be null')            
        else:
            rules_list.append( 'The column '+ k + ' can be null')       
        
        if is_string_dtype(df[k]):            
            rules_list.append( 'The column '+ k + ' should be alphabets')
            if (df[k].str.len().min())== (df[k].str.len().max()):
                rules_list.append( 'The column '+ k + ' should be of '+ str(df[k].str.len().min())+' Characters')
        if is_numeric_dtype(df[k]):            
            rules_list.append( 'The column '+ k + ' should be numeric')            
       
        
        Dict[k] = rules_list 
        rules.append(Dict)
  
    json_data = json.dumps(rules)    
    return json_data


@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None

    return '''<h1>The language value is: {}</h1>'''.format(language)

@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()

    language = req_data['language']
    framework = req_data['framework']
    python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
    example = req_data['examples'][0] #an index is needed because of the array
    boolean_test = req_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)




app.run()
