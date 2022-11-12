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



2. Избавляемся от дефолтных конструкторов
В большинстве случаев, которые я встретил, если в классе имеются setter'ы, то их можно убирать и смело добавлять в конструктор. Таким образом, мы 
не нарушаем инкапсуляцию.

2.1

2.2
