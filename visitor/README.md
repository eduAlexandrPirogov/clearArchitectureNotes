#Observer to Visitor

Истинное наследование.

Далее описанная ситуация будут основана на учебном примере книги "Паттерны проектирования" Фрименов, а именно пример с Паттерном Наблюдатель.
В книге описывается следующая ситуация: имеются метеорологические станции, которые присылают нам данные. У нас же имеется три сервиса, которые
воспроизводят различные действия над пришедшими данными (просто показать, показать статистику, показать прогноз). Наблюдатель в данном примере позволяет 
нам решить проблему связи "один-ко-многим", а также, если один из сервисов получит обновление, то обновятся все сервисы.

У данного паттерна имеются две основные единицы: тип данных "Наблюдатель-контейнер" и тип данных "Наблюдаемый". Контейнер сервисов реализует "Наблюдатель-контейнер", а сервисы -- тип данных "Наблюдаемый".

Код Паттерна "Наблюдатель": https://github.com/eduAlexandrPirogov/clearArchitectureNotes/blob/main/visitor/observer.cpp

У данного паттерна также имеются ограничения:
1. Все производные объекты типа данных "Наблюдаемый" имеют метод update(). Проблема в том, что могут быть сервисы, для которых название метода update() может быть неподходящим (например, просто показ погоды).
2. При изменений спецификаций, скажем, нам нужно получить количество обращений к сервисам за текущий период. (Допустим, нам нужно понять, к какому сервису обращались наибольшее количество раз). Если сервис закрыт для изменений, то придется наследовать сервис и переопределять метод update().

Но существует паттерн, который действует как "Наблюдатель", но также устраняет ограничения "Наблюдателя" -- паттерн "Посетитель".
Перепишем наш пример с сервисами погоды в паттерн "Посетитель":

Код Паттерна "Посетитель" на основе "Наблюдателя": https://github.com/eduAlexandrPirogov/clearArchitectureNotes/blob/main/visitor/observer_to_visitor.cpp

В чем суть данной "переделки". 
У нас имеется также  контейнер сервисом, погодные сервисы и "Посетители". На каждую операцию сервисов мы создаем посетителей "WeatherVisitor" "WetWeatherVisitor". Присваиваем сервисам "Посетитель", тем самым мы не трогаем ни контейнер сервисом, ни переопределяем никакие методы сервисов.

В случае реализации через "Наблюдатель" мы столкнулись бы со следующей диллемой:
1. Либо переопределять update()
2. Либо добавлять в метод update() доп вычисления, но это нарушение SRP.

Плюсы:
Во-первых, у нас также сохраняется в данном контексте решением проблемы связи "один-ко-многим", а также при обновлении обновятся все сервисы.
Во-вторых, если нам потребуется добавить в сервисы количество обращений к нему, то все, что нам нужно -- расширить соответствующие сервисы, но при  этом 
не нужно переопределять никакие операций, так как мы сделаем все в соответствующем "Посетитель".
В-третьих, невероятная гибкость; если нам понадобится выполнить какую-то операцию над конейтнером сервисов (например, получить суммарное количество запросов к сервисам), то мы не создаем метод именно в "посетителе". 

Это один из случаев, когда паттерн можно переделать в паттерн "Посетитель" и "Наблюдатель" слишком хорошо подошел в данном контексе и изменения вышли недорогими.
Но стоит проверить с другими паттернами. 
