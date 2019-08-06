# ArcGIS Geocoder
![Main view](https://github.com/fugrusha/blackhole/blob/master/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/mainview.png)

## Инструкция пользователя

### 1. Выберите excel-файл 
Первая строка должна содержать названия полей, следующие строки — значения полей: 
+ 1-й вариант названия полей **ID_TT**, **Client**, **Address**

Поле **Address** содержит полный адрес с доп. информацией, например:

*Львівська обл., Миколаївський р-н, м.Миколаїв, вул. Данила Галицького 1, приміщення №1, Аптека №1 "Економ"*
![Required fields-1](https://github.com/fugrusha/blackhole/blob/pyqt_gui/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/Required%20fields-1.png)

 + 2-й вариант названия полей **ID_TT**, **Client**, **Region**, **City**, **Street**, **NoHouse**

![Required fields-2](https://github.com/fugrusha/blackhole/blob/pyqt_gui/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/Required%20fields-2.png)

### 2. Определите настройки поиска
* Индекс начальной строки - определяет с какой строки файла начинать обрабатывать файл (0 - первая строка таблицы)
* Сохранять файл каждые N адресов - определяет как часто программа сохраняет файл резервной копии
* Количетсво попыток найти координаты - определяет сколько раз программа пытается геокодировать адрес, прежде чем перейти к следующему адресу

![Settings view](https://github.com/fugrusha/blackhole/blob/master/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/settingsview.png)

### 3. Нажмите кнопку ***Поиск***
Файл с кооридинатами создается на вашем рабочем столе

![Result view](https://github.com/fugrusha/blackhole/blob/master/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/geocoder_mainwindow.png)

