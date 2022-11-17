1) Было:

В нижеприведенном коде можно выделять два повторяющихся управленческих шаблона:
1. Пройти  циклом for по словарю
2. Выполнить определенное действие в элементов в зависимости от условий

```cpp
void ComparePanel::updateCompareView(std::map<std::string, int>& colored_items)
{
	int i = 0;
	for (const auto& myPair : colored_items) {
		if (myPair.second == 0)
			difference->SetItem(i, 1, "Да");
		else
			difference->SetItem(i, 1, "Нет");
		i++;
	}
	i = 0;
	for (const auto& myPair : colored_items) {
		if (myPair.second == 0)
			difference->SetItemBackgroundColour(i, wxColor(104, 244, 106));
		else
			difference->SetItemBackgroundColour(i, wxColor(254, 255, 55));
		i++;
	}
};
```

Стало:
```cpp

//Определяем лямбда-функции в хедере класса
std::function<void(wxColour, int row, std::string)> setDifferenceItems = [this](wxColour colour, int row, std::string arg)
{
     this->difference->SetItem(row, 1, arg);
     this->difference->SetItemBackgroundColour(row, colour);
}

//Определяем абстракцию управленческого шаблона
template<typename Iterable = std::map<std::string, int>, typename Function>
myAbstractFor(Iterable& iterableMap, Function& func)
{
  int i = 0;
	for (const auto& myPair : iterableMap) {
		 myPair.second == 0 ? func(wxColour(104, 244, 106), i, "Да") :func(wxColor(254, 255, 55), i, "Нет");
		 i++;
	}
}

void ComparePanel::updateCompareView(std::map<std::string, int>& colored_items)
{
	myAbstractFor<std::map<std::string, int>, std::function<void(wxColour, int, std::string&)>>(colored_items, setDifferenceItems);
};
```
Мы заменили в методе 15 строчек кода на одну. 

2) Рабочий проект, код немного упрощен.

В одном из проектов по коду разбросаны подобные инструкции:
Было:
```php
public someFunction1()
{
   try {
       //Пытаемся некие данные из БД
       query->...
   } catch(\Exception $e) 
   {
      \Log::debug(...);
   }
}

public someFunction2()
{
   try {
       //Пытаемся некие данные из БД
       query->...
   } catch(\Exception $e) 
   {
      \Log::debug(...);
   }
}
```

Стало:
```php
public function tryQuery($query)
{
    try { 
       //Берем данные
       query->...
   } catch(\Exception $e) 
   {
      \Log::debug(...);
   }
}

//--------------

public someFunction1()
{
   tryQuery($query);
   //...
}

public someFunction2()
{
   tryQuery($query);
   //...
}
```

Также, подобные try catch блоки можно улучшить до следующего уровня -- выделяем try и catch в отдельные функции:

```php
$logDebug = function($message)
{
  //Проводим некотороую манипуляцию с логгированием, сообщением и т.п.
   \Log::debug($message);
}

$logInfo = function($message)
{
  //Проводим некотороую манипуляцию с логгированием, сообщением и т.п.
   \Log::info($message);
} 

//И теперь функции с try-catch логированием могут выглядеть следующим образом:

public function tryQuery($query, $logType)
{
   try{
      query->...
   } catch(\Exception $e)
   {
       $someMessage = ...
       $logType($someMessage);
   }
}

//Вызов функции

public function someFunction()
{
    $query = ....
    tryQuery($query, $logDebug);
    tryQuery($query, $logInfo);
}
```

------------------
3) Не нашел хорошо подходящего примера, поэтому больше теоретичский пример, который обнаружил для себя:
Зачастую бывает ситуация, в коде мы итерируем контейнер, и совершаем над его элементами какие-либо вещи.

И по проекту часто размазывается подобная ситуация:

```cpp
void increaseNumbers(std::vector<int>& numbers)
{
    auto begin = numbers.begin();
    auto end = numbers.end();
    for(; begin != end; +=begin)
    {
        //Далее могут идти произвольные кострукции и вложения
        if(*begin % 2 == 0)
        {
              
        } else {
        
        }
    };
}


void eraseSpaces(std::list<std::string>& carOwners)
{
    auto begin = carOwners.begin();
    auto end = carOwners.end();
    for(; begin != end; +=begin)
    {
        //Исполняем некую операцию над данными..
    };
}
```

Подобные итерации занимают минимум 3 строчки кода.

Но это можно улучшить, если мы обернем итерацию в отдельную абстркцию:

```cpp
//Создаем абстракцию для итераций
template<typename Iterable, typename LambdaFunc>
void iterate(Iterable& iterable, Lambda lambda)
{
   auto begin = iterable.begin();
   auto end = iterable.end();
   for(; begin != end; begin++)
      lambda(*begin);
}

//Как это будет работать
int main()
{
    std::vector<int> numbers = {1,2,3,4,5};
    iterate(numbers, [](int& items) { item *= 10};
    iterate(numbers, [](int& items) { printf("%d ", items};
    
    
    std::list<std::string> names = {"Alex", "Ivan", "Anton"};
    iterate(numbers, [](std::string& name) { name[0] = 'O';});
    iterate(numbers, [](std::string& name) { printf("%s\n", name});
}


---------------------------

Если подумать, то применяя данную технику, очень напоминает программирование на F# и после него такие вещи кажутся более видимыми:
1. Конструкция for -- функция for(start, end, condition, accumulator), где condition -- предикат. Также можно добавить функцию в параметры, для манипуляции над данными.
2. if -- функции предикаты.
3. try-catch -- конструкция, которую можно выразить в следующем виде:
```
function try(Lambda)
{
    if(Lambda throws)
        catch(Exception)
}

function catch(Exception)
{

}
```
И вот подобные конструкции мы можем дополнять своими функциями.

Но возникает вопрос, как часто использовать подобную технику. Например, в PHP подобное не очень удобно, в силу того, что нельзя задать тип параметра функции и не понятно,
будет ли передана функция или примитивный тип данных. 
Но в С++ такое более удачно, за счет <functional> и шаблонов. Один раз создаем функцию, которая применима для многих контейнеров (используем специализацию) и добавляем
в качестве параметра свою lambda-функцию. Да, можно сказать, что в C++ есть <algorithm>, которые реализует итерации и те же lambda-функции, но они зачастую длинные и 
громоздкие. Да и <algorithm> больше про то, что нам нужно сделать некоторую вещь над контейнером, в том время, как вышеприведенные техники направленны на блоки кода.

