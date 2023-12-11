import pandas as pd
import numpy as np
import os
from sklearn.svm import OneClassSVM
import matplotlib.pyplot as plt
import matplotlib.font_manager 
from matplotlib.font_manager import FontProperties
from flask import Flask , request,jsonify
from flask_cors import CORS
import json
import base64
import traceback


app = Flask(__name__)
CORS(app, resources={r"/DAS_OCSVM": {"origins": ["http://localhost:7238", "http://localhost:5036"]}})

input_train_data  =  [
                       app.root_path + '/train_data/2022-07-13-DAS-101.csv',
                       app.root_path + '/train_data/2022-07-13-DAS-102.csv',
                       app.root_path +'/train_data/2022-07-13-DAS-103.csv'
                        ] 

input_error_data  = [app.root_path +'/error_data/errordata-01.csv']

@app.route('/DAS_OCSVM', methods=['POST'])
def das_ocsvm():
    

    try:
        excel_file = request.form.get('excelData')
        excel_df = json.loads(excel_file)
        data_list =pd.json_normalize(excel_df)
        normal_file = 'normal_csv.csv'
        data_list.to_csv(normal_file, index=False)
        normal_file_local = [app.root_path +'/normal_csv.csv']
        #將json轉換為csv
        train_threshold=0.1
        #閥門
        df = pd.DataFrame()
        for i in input_train_data:
            path_scv = i
            read_df = pd.read_csv(path_scv)
            df = pd.concat([df,read_df])

            train_n = len(df) -2
            valid_n = 2

            name_index = df.columns

            df = df[:train_n+valid_n]

            train_rate = []
            para_nu = []
            n = np.arange(0.01 , 1 , 0.01)
            valid_rate = -1
            #設定訓練集和測試集長度
        for i in  n :
            train_data = df[name_index[1:3]][:train_n]
            valid_data = df[name_index[1:3]][:valid_n]
            svm_model = OneClassSVM(nu=i,kernel='rbf').fit(train_data)
            svm_model_fit = svm_model.predict(train_data)
            svm_model_fit[svm_model_fit == 1] = 0
            svm_model_fit[svm_model_fit == -1] = 1
            train_rate_local = sum(svm_model_fit) / (len(svm_model_fit))

            svm_model_predict = svm_model.predict(valid_data)
            svm_model_predict[svm_model_predict == 1] = 0
            svm_model_predict[svm_model_predict == -1] = 1
            valid_rate_local = sum(svm_model_predict) / (len(svm_model_predict))
            train = [train_rate_local,valid_rate_local,svm_model]
            print("nu =", i ,"train_rate =", train_rate_local, "valid_rate =", valid_rate_local)
            if valid_rate == -1:
                if train[0] < train_threshold:
                    para_nu = i
                    train_rate = train[0]
                    valid_rate = train[1]
                    svm_model = train[2]
            if valid_rate != -1:
                if train[0] < train_threshold:
                    if train[1] < valid_rate:
                        para_nu = i
                        train_rate = train[0]
                        valid_rate = train[1]
                        svm_model = train[2]
        print("best nu:", para_nu )
        #自動找尋最佳nu參數
        error_df = pd.read_csv(path_scv)
        error_df = pd.DataFrame()
        for i in input_error_data:
            path_scv = i
            reg_df = pd.read_csv(path_scv)
            error_df = pd.concat([error_df,reg_df])

        name_index = error_df.columns
        
#--------------------------------------------------------------------------
        normalcsv_df = pd.read_csv(path_scv)
        normalcsv_df = pd.DataFrame()
        for i in normal_file_local:
            path_scv = i
            test_df = pd.read_csv(path_scv)
            normalcsv_df = pd.concat([normalcsv_df,test_df])
        name_index = normalcsv_df.columns
        #print(normalcsv_df[name_index])
        #return jsonify (normal_file_local)
  
        x_bound = 10
        y_bound = 10

        xx , yy = np.meshgrid(np.linspace(0,x_bound,1000),np.linspace(0,y_bound,1000))
        Z = svm_model.decision_function(np.c_[xx.ravel(),yy.ravel()])
        Z =Z.reshape(xx.shape)

        plt.title("abnormal detection  Error rate :" +str(para_nu))
        plt.contour(xx,yy,Z,levels = np.linspace(Z.min(),0,7),cmap=plt.cm.PuBu)
        a = plt.contour(xx,yy,Z,levels = [0, Z.max()], colors='palevioletred')

        
        
        b1 = plt.scatter(normalcsv_df[name_index[1]],normalcsv_df[name_index[2]],c = 'blue',s = 40 )
        c = plt.scatter(error_df[name_index[1]], error_df[name_index[2]], c='red', s=40, edgecolors='k') 

        plt.axis('tight')
        plt.xlim(0,x_bound)
        plt.ylim(0,y_bound)
        plt.legend([a.collections[0], b1,c],
                        ["learned frontier", 'training(' + str(train_n+valid_n) + ')','noise(' + str(len(error_df)) +')'],
                        loc="upper left",
                        prop=matplotlib.font_manager.FontProperties(size=11),
                        bbox_to_anchor=(1.05, 1))

        plt.xlabel(name_index[1])
        plt.ylabel(name_index[2])
        plt.savefig("plot.png")
        #將繪製的圖形匯出
        with open("plot.png", "rb") as image_ans:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
            image_data = image_ans.read()

        base64_data  = base64.b64encode(image_data).decode('utf-8')

        image_json = {
                "image": base64_data,
                "width": plt.gcf().get_size_inches()[0],
                "height": plt.gcf().get_size_inches()[1]
                }
        return  jsonify(image_json)
        #將圖形格式轉換成Json再回傳
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


    