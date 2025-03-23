"""
Script: Signatur.py
Description: [ADD DESCRIPTION HERE]
Usage: python Signatur.py
"""

#Функции активации
relu = lambda x: (x>=0) * x
relu2deriv = lambda x: x >= 0

def softmax(x):
    tmp = np.exp(x)
    return tmp / np.sum(tmp, axis=1, keepdims=True)
    
alpha, hidden_size, pixels_per_image, num_labels, epochs = (0.005, 40, 784, 10, 2)

#Инициализация весовых коэффицентов
weights_1 = 0.2*np.random.random((pixels_per_image, hidden_size))-0.1
weights_2 = 0.2*np.random.random((hidden_size, num_labels))-0.1
    
#Обучаем нейронную сеть
for epoch in range(epochs):
    error, test_error, test_corrent_cnt, corrent_cnt = 0.0, 0.0, 0, 0

    for i in range(len(images)):
        layer_0 = images[i:i+1] #входной слой берем изображение из БД для обучения
        layer_1 = relu(np.dot(layer_0, weights_1)) #считаем результат для скрытого слоя и применяем к нему функцию ReLu
        layer_2 = softmax(np.dot(layer_1, weights_2)) #считаем выходом нейронной сети и применяем функцию SoftMax
        
        error += np.sum((labels[i:i+1] - layer_2) ** 2) #вычисляем ошибку, в данном случае она нужна только для статистики
        corrent_cnt += int(np.argmax(layer_2) == np.argmax(labels[i:i+1])) #количество правильных ответов, также нужно для статистики
        
        layer_2_delta = (labels[i:i+1] - layer_2) #вычисляем дельту выходного слоя
        layer_1_delta = layer_2_delta.dot(weights_2.T) * relu2deriv(layer_1) #вычисляем дельту скрытого слоя

        weights_2 += alpha * layer_1.T.dot(layer_2_delta) #изменяем весовой коэффицент
        weights_1 += alpha * layer_0.T.dot(layer_1_delta) #изменяем весовой коэффицент
    
    #вычисление результата на тестовой выборке
    for i in range(len(test_images)):
        layer_0 = test_images[i:i+1]
        layer_1 = relu(np.dot(layer_0, weights_1))
        layer_2 = softmax(np.dot(layer_1, weights_2))
        test_corrent_cnt += int(np.argmax(layer_2) == np.argmax(test_labels[i:i+1]))
        test_error += np.sum((test_labels[i:i+1] - layer_2) ** 2)
    
    #вывод результата обучения на каждой интерации
    print(f"Epoch: {epoch}/{epochs};",
        f"Error: {str(error/float(len(images)))[0:5]};",
        f"Acc: {corrent_cnt/float(len(images))};",
        f"Test_Error: {str(test_error/float(len(test_images)))[0:5]};",
        f"Test_Acc: {test_corrent_cnt/float(len(test_images))}")