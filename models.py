import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MaxAbsScaler
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split,   \
                                    learning_curve,     \
                                    validation_curve,   \
                                    cross_val_score,    \
                                    RandomizedSearchCV

def normalize(X, ignore_columns=['ip_ent', 'port_ent', 'silence_ratio'], scaler=None):
    # ignore already normalized features and get remaining features
    X_to_norm = X[[c for c in X.columns if c not in ignore_columns]]
    
    if not scaler:
        # get scaler
        scaler = MaxAbsScaler().fit(X_to_norm)  # divide by feature's max
    
    # normalize
    X_norm = scaler.transform(X_to_norm)
    
    # add ignore columns
    X_ignore = X[ignore_columns]
    X_norm = np.append(X_norm, X_ignore, axis=1)
    
    return X_norm, scaler

def prep_data(attack_data, normal_data):
    """
        Args:
            attack_data: DataFrame
            normal_data: DataFrame
    """
    # add class labels
    attack_data['class'] = 1
    normal_data['class'] = 0
    # join datasets
    data = attack_data.append(normal_data, ignore_index=True)
    data.describe()
    
    # get features and labels
    X = data.iloc[:, 1:10].copy()
    y = data['class'].copy()
    # split the data into train (70%) and test (30%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # feature scaling (divide by max)
    ignore_columns=['ip_ent', 'port_ent', 'silence_ratio']
    X_train, scaler = normalize(X_train, ignore_columns=ignore_columns)
    X_test, scaler = normalize(X_test, ignore_columns=ignore_columns, scaler=scaler)

    return X_train, X_test, y_train, y_test, scaler

def performanceEvaluation(y, pred_val):
    accuracy = metrics.accuracy_score(y, pred_val) * 100
    precision = metrics.precision_score(y, pred_val) * 100
    recall = metrics.recall_score(y, pred_val) * 100
    f1 = metrics.f1_score(y, pred_val) * 100
    confusion_matrix = metrics.confusion_matrix(y, pred_val)
    return accuracy, precision, recall, f1, confusion_matrix

def plots():
    pass

def save_conf_matrix_img(fname, confusion_matrix):
    tn, fp, fn, tp = confusion_matrix.ravel()
    cell_text = [[str(tp) + ' (tp)', str(fn) + ' (fn)'], [str(fp) + ' (fp)', str(tn) + ' (tn)']]
    row_labels = ['Actual Class = 1', 'Actual Class = 0']
    col_labels = ['Predict Class = 1', 'Predict Class = 0']
    plt.clf()
    ytable = plt.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels, loc="center", cellLoc="center")
    plt.axis("off")
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(fname)

if __name__ == '__main__':
    plots_dir = 'imgs'
    data_dir = 'dataset'

    # load data
    attack_data = pd.read_csv('{}/attack_dataset.csv'.format(data_dir))
    normal_data = pd.read_csv('{}/normal_dataset.csv'.format(data_dir))
    # add classes, split and normalize
    X_train, X_test, y_train, y_test, scaler = prep_data(attack_data=attack_data, normal_data=normal_data)

    #
    # train SVM with rbf kernel
    #

    svc = svm.SVC(kernel='rbf').fit(X_train, y_train)

    # evaluate
    y_pred = svc.predict(X_test)
    accuracy, precision, recall, f1, confusion_matrix = performanceEvaluation(y_test, y_pred)
    save_conf_matrix_img('{}/svm_confusion_matrix'.format(plots_dir), confusion_matrix)
    
    print('SVM results\n')
    print(' accuracy {:.2f}%\n precision {:.2f}%\n recall {:.2f}%\n f1 {:.2f}%\n'.format(accuracy, precision, recall, f1))
    print(classification_report(y_test, y_pred))

    #
    # train logistic regression
    #

    logreg = LogisticRegression().fit(X_train, y_train)

    # evaluate
    y_pred = logreg.predict(X_test)
    accuracy, precision, recall, f1, confusion_matrix = performanceEvaluation(y_test, y_pred)
    save_conf_matrix_img('{}/logreg_confusion_matrix'.format(plots_dir), confusion_matrix)

    print('Logistic Regression results\n')
    print(' accuracy {:.2f}%\n precision {:.2f}%\n recall {:.2f}%\n f1 {:.2f}%\n'.format(accuracy, precision, recall, f1))
    print(classification_report(y_test, y_pred))