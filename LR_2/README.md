# Лабораторная работа №2 
Выполнил студент группы 6133-010402D Гудков Сергей

1.	Сформулируем задачу машинного обучения для БД и выберем наиболее интересные нам параметры.

В таблицу book исходной базы данных добавим бинарный признак recommend, который будет отражать будет ли интернет-магазин рекомендовать книгу пользователям сайта.
Задача машинного обучения будет состоять в определении флага рекомендации, показывающего необходимость рекомендации конкретной книги самим магазином. Мол: Book_stor рекомендует!
Выберем интересные нам параметры: 
- Жанр
- Количество продаж
- Цена
- Рейтинг книги
- Рейтинг Автора

Составим SQL запрос: 
```SQL
WITH BookInfo AS (
    SELECT 
        b.genre, 
        b.num_sales, 
        b.price, 
        b.rating, 
        a.rating AS author_rating,
        b.recommend
    FROM 
        public.book b
    INNER JOIN 
        public.book_author ba ON b.book_id = ba.book_book_id
    INNER JOIN 
        public.author a ON ba.author_author_id = a.author_id
)
SELECT 
    bi.genre,
    bi.num_sales,
    bi.price,
    bi.rating,
    bi.author_rating,
    bi.recommend
FROM 
    BookInfo bi;
```
Считаем базу данных и закодируем критериальные признаки

```Python
df = pd.read_csv('data.csv')

from sklearn.preprocessing import LabelEncoder
labelEncoder = LabelEncoder()
categ_for_lable_encode = ['genre', 'recommend']
for category in categ_for_lable_encode:
    df[category] = labelEncoder.fit_transform(df[category])
df.head()

| genre | num_sales | price   | rating | author_rating | recommend |
|-------|-----------|---------|--------|---------------|-----------|
| 14    | 266559    | 68.32   | 9      | 5             | 1         |
| 17    | 676405    | 94.12   | 6      | 5             | 1         |
| 5     | 53434     | 44.66   | 10     | 10            | 0         |
| 10    | 294583    | 79.50   | 1      | 5             | 1         |
| 11    | 973221    | 84.86   | 9      | 5             | 0         |
```

Разделим данные на обучающую и тестовую выборки: 
```Python
data = df.drop('recommend', axis = 1)
target_data = df['recommend']

# Разделим на обучающую и тестовую выборки
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
                data, target_data, test_size=0.33, random_state=42)
```

Следующим шагом я выбрал классификатор RandomForest и попробовал провести GridSearch для определения оптимальных параметров. 
Так вот... па.. па... пам... сижу уже 2-ой час и жду результатов. Надеюсь не зря жду и ничего сейчас у меня тут не умрёт.    
...   
...   
Ещё пол часа прошло, ждём...   
...    
...   
Ещё два часа... Что-то мне подсказывает, что ждать уже нет смысла. Ладно, попробуем иначе...    
Решил уменьшить объём данных, так как при имеющихся 4999999 - обучение происходит крайне медленно.   
Оставим ко-во строк = 4999

```Python
df = df[1:4999]
```
Далее создадим модель классификатора и обучим её:
```Python
forest_model = RandomForestClassifier()
forest_model.fit(X_train, y_train)
preds = forest_model.predict(X_test)

print(classification_report(y_test, preds))

              precision    recall  f1-score   support

           0       0.60      0.62      0.61      8198
           1       0.61      0.58      0.60      8302

    accuracy                           0.60     16500
   macro avg       0.60      0.60      0.60     16500
weighted avg       0.60      0.60      0.60     16500
```
Качество не такое хорошее, но нужно понимать, что данные были созданы совершенно рандомно и они никак не связаны.

```Python
crossval_score = []

for i in range(1, data.shape[1] + 1):
    skb = SelectKBest(score_func=f_classif, k=i)
    Xreduced = skb.fit_transform(data, target_data)
    scores = cross_val_score(forest_model, Xreduced, target_data, cv = 5)
    crossval_score.append(scores.mean())

plt.plot(range(1, data.shape[1] + 1), crossval_score)
plt.grid()
plt.scatter(crossval_score.index(max(crossval_score)) + 1, max(crossval_score), c='r')
```
Посмотрим на оптимальное ко-во параметров:   
![изображение](https://github.com/DekartVan/Corporate-databases-LR/assets/60447026/ef142e8b-1394-4fc2-b496-4314eb1da4f9)   

И подберём остальные гиперпараметры: 
```Python
grid = {
    'n_estimators': list(range(10, 100, 5)),
    'max_features': list(range(1, X_new.shape[1] + 1)),
    'min_samples_leaf': list(range(1, 15))
}

clf = RandomizedSearchCV(forest_model, grid, random_state=42)
search = clf.fit(X_new, target_data)

search.best_params_
```
По итогу: {'n_estimators': 30, 'min_samples_leaf': 2, 'max_features': 2}   

Взглянем на метрики:
```Python
model = RandomForestClassifier(n_estimators=30, min_samples_leaf=2, max_features=2,)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print(classification_report(y_test, preds))

              precision    recall  f1-score   support

           0       0.63      0.64      0.63      8198
           1       0.64      0.63      0.64      8302

    accuracy                           0.63     16500
   macro avg       0.63      0.63      0.63     16500
weighted avg       0.63      0.63      0.63     16500
```

После всех опираций метрики улучшились, но совсем немного. Всё же найти логику в данных, логики в которых не было... Трудновато. 

