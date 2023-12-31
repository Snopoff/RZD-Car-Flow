# Всероссийский хакатон в Нижнем Новгороде

## Инструкция по запуску приложения
В текущей организации интерфейс использует предложенный файл ```dataset.json```. Для запуска необходимо собрать Docker-образ из Dockerfile. Выполните команды 

```
docker build -t rzd .
docker run -dp 3000:3000 rzd
```

Иначе можно запустить без `Docker`. Для этого в папке с проектом нужно иметь файл ```dataset.json``` и надо выполнить команды
```
pip install pandas
pip install dash
python front.py
```

## Добро пожаловать на кейс РЖД "Координация пропуска вагонопотока"!

В представленом файле ```dataset.json``` вы можете увидеть _ситуации_ (в количестве 100к), происходящие на станциях, где планируется внедрение системы. Каждая _ситуация_ состоит из нескольких частей:
1. Список станций (с порядковыми номерами от 1 до 7), а также массив, описывающий, сколько вагонов на этой станции подлежат к отправке и на какую станцию (по порядковому номеру в массиве __+1__). Не забудьте, что вагоны со станции не могут отправиться на неё же :)
```
"stations": {
    "Златоуст (1)": [0...n],
	...
	"Еманжелинск (7)": [n2...0]
}
```
2. Полное расписание проходящих через все станции поездов.
```
"full_timetable": {
		"train_number": {   <--- номер поезда, в рамках ситуации уникален
			"route": [   <--- маршрут поезда (через станции с каким порядковым номером он проходит). 
				"1",            Тут всегда указан полный маршрут, который касается выбранного для кейса участка
				...
				"2"
			],
			"free_carriage": [  <-- количество вагонов, которые поезд может перевозить на каждом промежутке пути
				"17",       Внимание! Если на каком-то промежутке указано значение, меньшее, чем на предыдущем,
				...         это значит, что на станции к поезду зацепили вагоны, не относящиеся к нашей задаче!
				"14"        Это справедливо и для обратной ситуации (когда вагоны отцепляют).
			],
			"timetable": [   <-- расписание поезда для каждой станции на его пути (прибытие - отбытие)
				"01:00 - 01:52",
				...
				"12:28 - 13:52"
			]
		}
```
***

##### Вашей задачей будет создание модели, которая позволит максимально эффективно перевезти максимальное количество вагонов с грузами, которые того требуют (указаны в п.1). Мы понимаем, что перевезти все грузы таким образом невозможно, поэтому их остатки на различных станциях можно будет "довезти", организовав отдельный (или отдельные) поезда-доставщики. Сможете ли вы сгенерировать не только расписание эффективной перевозки, но и расписание эффективной доставки остатка?
##### Увидим в конце хакатона, а пока что ---
# ЖЕЛАЕМ УДАЧИ!




P.S. Не забудьте посетить экспертные сессии и не стесняйтесь задавать вопросы)
