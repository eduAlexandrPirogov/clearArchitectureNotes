# Правила простого дизайна


Изначально рассмотрим исходный пример, а затем два варианта его улучшения.
Имеется класс `TimerDisplayWidget`, который отражает пользователю таймеры: таймер работы и таймер отдыха. Пользователь может установить количество часов и минут в на каждый таймер. Код выглядел, примерно, следующим образом:

```cpp
class TimerDisplayWidget : public BaseTimerTrackerWidget
{
    Q_OBJECT
    QVBoxLayout* layout = 0;
    
    QTime*  workTime =0;
    QTime* restTime = 0;
    QTimer* workTimerWidget = 0;
    QTimer* restTimerWidget = 0;
    //...
public:
    TimerDisplayWidget()
    {
       workTimer = new QTime(0, 30);
       restTime = new QTime(0, 10);
       ...
    }; // Инициализация объектов и размещение их в Widget


public slots:

    void startTimerSlot()
    {
        workTimerWidget->startTimer();
    }
       
    void updateWorkTimer()
    {
        workTime = new QTime(workTime->addSecs(-1));
        label->setText(workTime->toString("hh:mm:ss"));
        if(workTime->toString("hh:mm:ss") == QString("00:00:00"))
            workTime->stopTimer();
    }
    
    ...

};

```
У данного дизайна имеются следующие проблемы:
1. QTime принимает в качестве параметров любые целочисленные значения (и отрицательные).
2. Несмотря на то, что QTime -- непримитивный тип, но с точки зрения проекта его можно считать примитивным, т.к. нам точно потребуются дополнительное поведения для данного класса.

1.Избегаем использования примитивных типов

1.1 Наличие QTime и QTimer в классе дает нам довольно негибкое решение. Что если нам понадобится, скажет DeepWorkTimer, PomodoroTimer и т.п.?
Вынесем QTime и QTimer в отдельный класс:

```cpp
class QWorkTimerWidget : public QTimerWidget
{
    Q_OBJECT

    QTime* passedTime = 0;
    QTimer* timer = 0;

    QLabel* label = 0;
    QVBoxLayout* layout = 0;
public:
    QWorkTimerWidget();

void startTimer()
{
    timer->start();
};

void stopTimer()
{
    timer->stop();
};

void setDeepWorkTimer(int hours, int minutes)
{
    passedTime = new QTime(hours, minutes);
    label->setText(passedTime->toString("hh:mm:ss"));
};

void setPomodoroTimer(int hours, int minutes)
{
    passedTime = new QTime(hours, minutes);
    label->setText(passedTime->toString("hh:mm:ss"));
};
signals:
    void stopWorkStartRest();

protected slots:
    void updateDisplayTimer()
    {
        //TODO optimize this
        passedTime = new QTime(passedTime->addSecs(-1));
        label->setText(passedTime->toString("hh:mm:ss"));
        if(passedTime->toString("hh:mm:ss") == QString("00:00:00"))
        {
            this->stopTimer();
            emit this->stopWorkStartRest();
        }
    }

};
```

1.2 Рассмотрим методы setDeepWorkTimer и setPomodoroTimer. Оба принимают в качестве параметров целочисленный примитивный тип. Лучше обернуть 
данные тип в enum mintes:

```cpp
enum TIMEFORTIMER
{
    FIFTEENMINUTS = 15, THIRTYMINUTES=30, FOURTYFIVEMINUTS=45, HOUR = 60, HOURANDFIFTEENMINUTES=75, HOURANDHALF=90,
    TWOHOURS=120
};
```

И установить в качестве параметров не int, а тип TIMEFORTIMER (учитывая, что для таймера преимущественно понадобится 15,30,45 и т.д. минут.


-------------------------------------------------------
2. Избавляемся от дефолтных конструкторов
В большинстве случаев, которые я встретил, если в классе имеются setter'ы, то их можно убирать и смело добавлять в конструктор. Таким образом, мы 
не нарушаем инкапсуляцию. Делая так, мы избавляемся от надобности дефолтного конструктора.

2.1 Реальный код в рабочем проекте: :)

```php
class Serviсe
{
   private string $name;
   private string $line;
   //Еще несколько внутренних полей
   
   public function __construct__()
   {
      //установка дефолтных значений на поля
   }
   
   public function setName($name)
   {
      $this->name = name;
   }
   
   public function setLine($line)
   {
       $this->line = line;
   };
   
   //Еще несколько сеттеров с проверкой на валидность данных
};
```
Тут можно сделать так:
1. Вынести часть полей в отдельные классы. Например, поля $name и $id можно вынести в класс ServiceMeta.
2. Установить конструктор, который валидирует данные

```php
class ServiceMeta
{
    private string $name;
    private string $line;
   
    public function __construct__ ($name, line)
    {
        private string $name;
        private string $line;
        //...
    }
};

class Serviсe
{
   private ServiceMeta $meta;
   //Еще несколько внутренних полей
   
   public function __construct__ ($meta, ...)
   {
      $this->meta = $meta;
      //...
   }
   
   //Удаляем из кода все сеттеры
};
```

-------------------------------------------------------
2.2
Также имеются варианты, когда нам нужно создать объект с заранее верными параметрами, чтобы не приходилось делать каждый раз проверку в различных методах:

```php
class Converter
{

    //Поля класса
    
    public function __construct__()
    {
       //... Установка некоторых значений полей класса
    };
   //Имеется несколько сеттеров на поля класса
   
   public function setDelimeter($delimeter)
   {
       $this->delimeter = $delimeter;
   };
   
   //....
   
   //И имеется метод, который содержит следующие строки
   
   public function convertingToCsv($file)
   {
       //...
       if(!isset($this->delimeter))
       {
           //Устанавливаем на поле дефолтное значение
       }
       if(!isset($this->anotherParam))
       {
           //Устанавлаем на поле дефолтное значение
       }
   };
};
```
В вышеприведенном примере, если имеется n setter'ов, то у нас будет n! вариантов развитий событий, что довольно тяжело будет "отлаживать".

Тут можно сделать следующим образом:
1. Вынести часть сеттеров в конструктор
2. Соответствующая часть сеттеров в вызываемый метод

```php
class Converter
{

    //Поля класса
    
    public function __construct__($delimeter, $someParam1 = defaultValue, $someParam2= defaultValue)
    {
       $this->delimeter = $delimeter;
       //...
    };
   
   //Устанавливаем остальные значения в метод
   public function convertingToCsv($file, ...)
   {
       //Тем самым избавляемся от проверки, установлен ли тот или иной параметр
   };
};
```
-------------------------------------------------------
3. Избавляемся от выброса исключений. 
3.1

```php

class Converter
{
    public function convertTo(string $format)
    {
        if($format != 'csv' || $format != 'xlsx')
            throw new \Exception ("...");
    };
};
```
Тут можно сделать перечисление форматов, тем самым избавляемся от возможного исключения:



```php
enum FORMATS
{
   CSV="csv", XLSX="xlsx", ...
};

class Converter
{
    public function convertTo(string $format)
    {
    //Убираем проверку
//        if($format != 'csv' || $format != 'xlsx')
//            throw new \Exception ("...");
    };
};
```
3.2 Также, если какой-то объект не удовлетворяет условию, то выбрасывается исключение

```php
public function getContract()
{
   $contract = Contract::where...->first();
   if(is_null($contract)
        throw new Exception($some_message);
    //Производим дальнейшие манипуляции
};
```

Тут можно вынести $conract в качестве параметра, тем самым, мы даем понять клиенту класса, что данный метод не работает с null.
```php
public function getContract(Contract $contract)
{
    //Проивзодим дальнейшие манипуляции
};
```
-------------------------------------------------------
Вывод:
В вышеприведенных примерах код был улучшен с помощью следующих действий:
1. Обертка примитивных типов в классы обертки -- тем самым мы снижаем вероятность того, что пользователь введет неверный формат данных, которые могут привести к неожиданному результату.
2. Добавление конструктора с параметрами -- тем самым, мы убираем сеттеры, наш объект становится, хоть и в слабой степени, иммутабельным -- мы не можем изменить его внутренее состояние, не вызвав команду АТД. Также мы устанавливаем валидацию на параметры в едином месте, тем самым убираем лишние строки кода ,которые могут быть размазаны по методу.
3. Убрали точки генерации исключения -- тем самым, мы убираем вариант, когда клиент класса, может вызвать такую комбинацию методов, при которой программа экстренно завершится, а клиент класса может об этом и не догадываться.

Благодаря таким методам, мы снижаем количество вариантов развития событий определенного участка кода, тем самым мы покроем тестами бОльший вариант событий.
