from typing import Any
import pandas
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


class NpEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if  isinstance(o,np.integer):
            return int(o)
        if isinstance(o,np.floating):
            return float(o)
        if isinstance(o,np.ndarray):
            return o.tolist()
        return super(NpEncoder,self).default(o)


def normalize_value_gender(raw_value):
    male_value = [
        'm',
        'male',
        'pria',
        'laki-laki'
    ]
    female_value = [
        'f',
        'female',
        'wanita',
        'perempuan'
    ]
    raw_value = str(raw_value)
    if raw_value.lower() in male_value:
        return 1
    elif raw_value.lower() in female_value:
        return 2
    return raw_value


def normalize_y_n(raw_value):
    raw_value = str(raw_value)
    if raw_value.lower() == 'yes' or raw_value.lower() == 'y':
        return 1
    elif raw_value.lower() == 'no' or raw_value.lower() == 'n':
        return 2
    return raw_value


def normalize_datasets(dataset:pandas.DataFrame)->pandas.DataFrame:
    num_attributes = dataset.shape[1]
    attribute_names = ["A{}".format(i+1) for i in range(num_attributes)]
    dataset.columns = attribute_names
    for column in dataset.columns:
        dataset[column] = dataset[column].apply(normalize_y_n)
        dataset[column] = dataset[column].apply(normalize_value_gender)
        dataset = dataset.fillna(dataset.mode().iloc[0])
        dataset = dataset.astype(str)
        strip_decimals = lambda x: str(x).split(".")[0]
        dataset = dataset.applymap(strip_decimals)
    return dataset
    

class DataTrainer(object):

    def __init__(self,df_feature:pandas.DataFrame,column_mapping:dict):
        self.df_feature = df_feature
        self.last_column_name = list(df_feature.keys())[-1]
        self.column_mapping = column_mapping
        self.train = {
            "accuracy": None,
            "prediction_result": None,
            "prediction_count": {},
            "evaluation": None
        }
        self.test = {
            "accuracy": None,
            "prediction_result": None,
            "prediction_count": {},
            "evaluation": None
        }
        self.evaluation = {
            "confusion_matrix": {
                "true_positive": None,
                "true_negative": None,
                "false_positive": None,
                "false_negative": None
            },
            "report": None
        }

    def revert_data_column(self,dataset:pandas.DataFrame)->pandas.DataFrame:
        """
        Mengembalikan dataset ke nama kolom asli
        """
        change_column = dict()
        for col in dataset.columns:
            if col not in self.column_mapping.keys():
                change_column[col] = col
            else:
                change_column[col] = self.column_mapping[col]
        result = dataset.rename(columns=change_column)
        return result
    

    def repack_data(self):
        packed_test_result = self.revert_data_column(self.test['prediction_result'])
        packed_train_result = self.revert_data_column(self.train['prediction_result'])
        self.test['prediction_result'] = packed_test_result.to_dict('records')
        self.train['prediction_result'] = packed_train_result.to_dict('records')

    def rfe_feature_selection(self):
        # Create instance of RandomForestClassifier
        model_rf = RandomForestClassifier()

        # Get last column
        sr_lastcolumn = self.df_feature[self.last_column_name]

        # Perform feature selection with RFE
        rfe = RFE(estimator=model_rf, n_features_to_select=5)
        fit = rfe.fit(self.df_feature, sr_lastcolumn)
        df_selected_features = self.df_feature.iloc[:,fit.support_]
        df_selected_features.head()

        return df_selected_features

    def split_data(self,df_selected_features:pandas.DataFrame):

        x = df_selected_features.iloc[:, :4].values
        y = df_selected_features.iloc[:, 4].values
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 0)
        
        return x_train,x_test,y_train,y_test

    def __convert_keys(self,k):
        if k == '1':
            return 'yes'
        elif k == '2':
            return 'no'
        else:
            return k.replace(" ","_")


    def get_classification_report(self,y_true,y_pred):
        report = classification_report(y_true, y_pred,output_dict=True)
        result = {}
        ## Convert keys
        for k,v in report.items():
            new_key = self.__convert_keys(k)
            result[new_key] = v
        return result
    
    @property
    def training_result(self):
        """
        Training result summary
        """
        data = {
            "train": self.train,
            "test": self.test,
            "evaluation": self.evaluation
        }

        return data


    def train_data(self,df_feature:pandas.DataFrame)->pandas.DataFrame:

        # Extract last column name and row
        lastcolumn_name = list(df_feature.keys())[-1]

        # Perform feature selection
        df_selected_features = self.rfe_feature_selection()

        # Split Data
        x_train, x_test, y_train, y_test = self.split_data(df_selected_features)
        
        classifier = GaussianNB()
        classifier.fit(x_train, y_train)

        # Lakukan prediksi pada data uji
        y_pred = classifier.predict(x_test)

        # Hitung akurasi pada data uji
        self.test['accuracy'] = accuracy_score(y_test, y_pred)

        # Lakukan prediksi pada data latih
        y_pred_train = classifier.predict(x_train)

        # Hitung akurasi pada data latih
        self.train['accuracy'] = accuracy_score(y_train, y_pred_train)

        y_pred = classifier.predict(x_test)
        unique, counts = np.unique(y_pred, return_counts=True)
        # Convert unique to string
        convert_keys = lambda x: "yes" if x == '1' else "no"
        unique_keys = [convert_keys(i) for i in unique]
        # Pack to dictionary and save to train set
        predcount = dict(zip(unique_keys,counts))
        self.test['prediction_count'].update(predcount)

        # Same as above test set
        y_pred_train = classifier.predict(x_train)
        unique_train, counts_train = np.unique(y_pred_train, return_counts=True)
        unique_keys = [convert_keys(i) for i in unique_train]
        predtrain = dict(zip(unique_keys,counts_train))
        self.train['prediction_count'].update(predtrain)

        df_column = df_selected_features.columns.to_list()[0:-1]
        
        # Rebuild table for train data
        df_result = pandas.DataFrame(x_train,columns=df_column)
        df_result[lastcolumn_name] = y_train
        df_result["output"] = y_pred_train

        self.train['prediction_result'] = df_result

        # Rebuild table for test data
        df_test_result = pandas.DataFrame(x_test,columns=df_column)
        df_test_result[lastcolumn_name] = y_test
        df_test_result["output"] = y_pred

        self.test['prediction_result'] = df_test_result

        # Evaluasi hasil prediksi pada data uji
        self.test['evaluation'] = self.get_classification_report(y_test, y_pred)

        # Evaluasi hasil prediksi pada data latih
        self.train['evaluation'] = self.get_classification_report(y_train, y_pred_train)

        cm = confusion_matrix(y_test, y_pred)
        self.evaluation['confusion_matrix'].update({
            "true_positive": cm[0][0],
            "false_positive": cm[0][1],
            "true_negative": cm[1][0],
            "false_negative": cm[1][1]
        })
        # Gabungkan data latih dan data uji
        
        X = np.concatenate((x_train, x_test))
        y = np.concatenate((y_train, y_test))

        # Inisialisasi dan latih model Naive Bayes
        model = GaussianNB()
        model.fit(X, y)

        # Lakukan prediksi pada data gabungan
        y_pred = model.predict(X)

        # Evaluasi hasil prediksi pada data gabungan
        self.evaluation['report'] = self.get_classification_report(y, y_pred)

        # Repack data
        self.repack_data()
