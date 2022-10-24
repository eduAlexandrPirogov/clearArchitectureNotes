# Mixins

Ссылки на источники:
1. Mixin-based Programming in C++: https://yanniss.github.io/practical-fmtd.pdf
2. Stack overflow: https://stackoverflow.com/questions/18773367/what-are-mixins-as-a-concept

Пример кода расположен в самом низу

Несмотря на то, что одна из ролей примесей -- некое подобие множественного наследования, а в С++ множественное 
наследование имеется, имеются интересные моменты, которые стоит рассмотреть.

# Вступление

Выделим два определения примесей:

1. Вики: Примеси -- класс, который содержит методы, которые будут использовать другие классы, не будучи их родительским классом. Позволяет провести "инъекцию" кода в какой-либо класс.Класс миксина действует как родительский класс, содержащий желаемую функциональность. Затем подкласс может наследовать или просто повторно использовать эту функциональность, но не как средство специализации. Как правило, примесь экспортирует желаемую функциональность в дочерний класс, не создавая жесткой единой связи «является». В этом заключается важное различие между концепциями примесей и наследования в том, что дочерний класс все еще может наследовать все функции родительского класса, но семантика о том, что дочерний элемент «является разновидностью» родителя, не обязательно должна применяться.

Статья Mixin-based Programming: Примеси -- это техника, чтобы указать расширение, не определяя заранее, что именно оно может расширять.

То есть примеси, это способ расширение класса родителя, причем класс родитель может быть потенциально любым.

# Вывод по Примесям

Примеси очень схожи с Паттерном "ПосетителЬ" по назначению -- расширение кода класса не изменяя сам класс.
При этом, миксины кажутся более гибкими, нежели "Посетитель".
Рассмотрим ситуацию. Имеется некоторая структура данных, пусть будет Список и Неориентированный Граф. И допустим мы хотим получить 1) некоторые агрегированные данные вышеупомянутых структур данных 2) получить некоторые свойства вышеупомянутых данных и мы не хотим изменять существующие интерфейфы двух классов.
Важный нюанс! Предполагаем, что у вышеупомянутых структур данных имеется итератор с единым для обоих интерфейсов!
Используя "Посетитель", нам пришлось бы на каждую операцию создавать соответствующий посетитель и реализовывать методы для каждого класса. Также нам придетс "плодить" параллельную иерарию классов.
Примеси же решают эту проблему более элегантно: Мы создаем класс Примесь с параметром шаблоном родителя, от которого наследуемся. В Примесях реализуем нужные нам методы, далее наследуемся от Примесей дочерним классом. Плюс такого подхода в том, что 1) мы не плодим параллельную иерархию классов и 2) примеси можно использовать потенциально ко многим суперклассам. 
Но у этого подхода имеются минусы, по крайней мере в С++:
1) Отсутвите type-checking-a
2) Неудобочитаемый синтаксис вложенных template<A<B<C...>>>>. 
3) Стоит держать в голове особенности работы с виртуальными методами
4) По мере расширения функционала класса, плодятся "слои примесей" (о чем говорят авторы статьи).
5) Нераспространенная техника в С++ (по крайней мере, пока обозревал форумы).

# Пример кода

Рассмотрим, как выглядят примеси в C++

```cpp
template<typename T>
class Iterable
{
    public:
    virtual T Next() = 0;
    virtual bool HasNext() = 0;
};

//Some class
template<typename T, size_t bufferSize>
class Array
{
    std::array<T, bufferSize> array;

class Iterator : public Iterable<T>
    {
        size_t indx;
        Array parent;
        public:
        Iterator(Array& arr)
        {
            indx = 0;
            parent = arr;
        }
        T Next()
        {
            int oldIdnex = indx;
            indx++;
            return parent.array[oldIdnex];
        }

        bool HasNext()
        {
            return indx < bufferSize;
        };
    };
public:
    Array() = default;

    void insert(size_t index, T item)
    {
        array[index] = item;
    }

    Iterator* iterator()
    {
        return new Iterator{*this};
    }

};

//another class
template<typename K, typename V>
class Map
{
    std::map<K, V> map;
    class Iterator : public Iterable<V>
    {
        size_t indx;
        Map parent;
        public:
        Iterator(Map& arr)
        {
            indx = 1;
            parent = arr;
        }
        V Next()
        {
            int oldIdnex = indx;
            indx++;
            return parent.map[oldIdnex];
        }

        bool HasNext()
        {
            return indx < parent.map.size();
        };
    };
    public:
    Map() = default;

    void insert(K key, V value)
    {
        map.insert(std::make_pair<K,V>(std::move(key), std::move(value)));
    };

    size_t size()
    {
        return map.size();
    }

    virtual void toString()
    {
        for(const auto& item :map)
            std::cout << item.first << ' ' << item.second << '\n';
    }

    Iterator* iterator()
    {
        return new Iterator{*this};
    }
    
};

//Creating mixing
template<typename BASE>
class SummMixin : public BASE //inherit from parametrized parent
{
public:
    SummMixin() = default;

    virtual size_t sum()
    {
        auto iter = BASE::iterator();
        size_t sum = 0;
        while(iter->HasNext())
            sum += iter->Next();
        return sum;
    }
};

typedef SummMixin<Map<int,int>> MapSum; //typedef для удобства
typedef SummMixin<Map<int,int>> ArraySum;

class ArrayExt : public ArraySum{
public:
    ArrayExt() = default;
}; //creating instances

class MapExt : public MapSum{
public:
    MapExt() = default;
};


int main()
{

    ArrayExt newArray;
    newArray.insert(0,10); //derived method
    newArray.insert(1,20); //derived method
    std::cout << "Sum of array " << newArray.sum() << '\n'; // extended method

    MapExt newMap;
    newMap.insert(1,1);
    newMap.insert(2,2);
    std::cout << "Sum of map " << newMap.sum() << '\n';

}
```
