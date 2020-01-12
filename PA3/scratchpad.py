lines[]
i = 0
for line in lines:
    l = re.split(r'\t+', line)

    if len(l) > 2:
        print(l)
        print(l[0])
        l1 = split(l[1][2:len(l[1])])
        dsl = len(l1)
        print('data string length: ', len(l1))
        if i == 0:
            k1 = np.array(l1)
            k = k1
            label1 = np.array(l[2])
            label = label1
        else:
            k1 = np.array(l1)
            k = np.append(k, k1)
            label1 = np.array(l[2])           
            label = np.append(label, label1)
        print(y)
        i += 1
    print(i)

k2 = k.reshape(i, dsl)

dataframe = pd.DataFrame.from_records(k2)
#return(dataframe, label)


def implement_perceptron(train_data, train_labels, test_data, test_labels):
    ppn = Perceptron(max_iter=50, eta0=0.1, random_state=0, verbose=1)
    ppn.fit(train_data, train_labels)
    t_pred = ppn.predict(test_data)
    print(t_pred)

train = r"ocr_test.txt"
test = r'ocr_train.txt'
train_data, train_labels = pre_process(train)
test_data, test_labels = pre_process(test)
implement_perceptron(train_data, train_labels, test_data, test_labels)