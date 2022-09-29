# Антипаттерн "Самодокументирующийся код"

Ссылка на README.md по данному отчету: https://github.com/eduAlexandrPirogov/clearArchitectureNotes/blob/main/commentaries/README.md


-------
## Пример 1
Рассмотрим следующий класс:

```php
class Relation
{

    public const INSERT_STATUS_NIL = -1;
    public const INSERT_STATUS_OK = 0;
    public const INSERT_STATUS_ERR = 1;
    public const INSERT_STATUS_DUPLICATE = 2;

    public const SEARCH_STATUS_NIL = -1;
    public const SEARCH_STATUS_OK = 0;
    public const SEARCH_STATUS_NOTFOUND = 1;

    private string $title;

    private array $rows; //class rows
    private array $primary_key;
    private array $unique_key;
    private array $schema;

    private int $insert_status;
    private int $search_status;

    public function __construct(string $title, array $schema)
    {
          //...

    }



    public function search(int $index, string $needle) : int
    {
         //...
    }

    public function search_pk(array $fk_columns): int
    {
         //...
    }


    public function union(Relation $anotherRelation) : Relation
    {
        //...
    }

    public function erase(int $byValue, int $at)
    {
        //...
    }

    public function size(): int
    {
        return count($this->rows);
    }

    public function insert(Row $row) : void
    {
          //...
    }

    private function contains(Row $anotherRow) : boolean
    {
          //...
    }

    public function search_row_by_index(int $index, array $primary_key): Row
    {
          //...
    }

    public function array_for_export(bool $with_id) : array
    {
         //...
    }

    public function row(int $id)
    {
        return $this->rows[$id-1];
    }

    public function title(): string
    {
        return $this->title;
    }

    private function check_row_schema(Row $row)
    {
          //...
    }

    public function iterator(): RelationIterator
    {
        return $this->createIterator();
    }
    
    private function createIterator(): RelationIterator
    {
       //...
    };
	
	
    public function get_insert_status(): int
    {
        return $this->insert_status;
    }
    
    public function get_search_status(): int
    {
        return $this->search_status;
    }

    public function get_primary_key(): array
    {
        return $this->primary_key;
    }

    public function set_primary_key(array $primary_key)
    {
        $this->primary_key = $primary_key;
    }

    public function set_unique_key(array $unique_key)
    {
        $this->unique_key = $unique_key;
    }
    }

}
```

Что делает данный класс в проекте? Данный класс -- реализации структуры данных "реляционная таблица", подобно реляционной таблице в реляционных СУБД, хранит лишь объекты "Row" (класс, который содержит колонки определенного типа). Данный класс предоставляет возможность производить стандартные операции поиска: по значению в колонки в классе "Row", по набору значений, определить, является ли строка подстройкой; установка первичного ключа, для однозначной идентификации объекта и т.д.
Данный класс активно используется в проекте, так как позволяет легко создавать массивы "отформатированных" данных в виде реляционных таблиц.

Попробуем взглянуть на данный код без комментариев со стороны "самодокументирующийся код":

```php
    public function insert(Row $row)
    {
        if (count($this->schema) != $row->size() ||
            $this->contains($row) == true
            ) {
            $this->insert_status = Relation::INSERT_STATUS_DUPLICATE;
        } else {
            //$this->check_row_schema($row);
            $this->rows[] = $row;
            $this->insert_status = Relation::INSERT_STATUS_OK;
        }
    }

    private function contains(Row $anotherRow)
    {
        $tmpAnotherSubRow = $anotherRow->sub_row($this->unique_key);
        foreach ($this->rows as $row) {
            /* @var $row Row */
            $tmpSubRow = $row->sub_row($this->unique_key);
            if ($row->equals($anotherRow) || (count($this->unique_key) > 0 && $tmpSubRow->equals($tmpAnotherSubRow))) {
                return true;
            }
        }
        return false;
    }
```

Смотря на метод `insert` видно, что в случае, если строка уже содержится, то она не будет добавлена в АСД "Relation". Но по каким критериям проверяется, что строка уже содержится в АСД "Relation"? По хэш-коду или по содержиому строки? Иначе говоря, **какому критерию должен удовлетворять объект класса "Row", чтобы соответствовать другому объекту класса "Row"**? 

Можно изучить метод `contains`, но дальше встретим строку **$anotherRow->sub_row($this->unique_key);**. Казалось бы очевидно, что метод sub_row возвращает строку, созданную из некоторых элементов объекта класса "Row". Но чтобы удостовериться в этом, приходиться смотреть метод **sub_row** (удостовериться, а не выбрасивает ли метод исключение, или имеются ли у него какие-либо нестандартные ситуации. 
Несмотря на то, что методы вроде отражают семантический смысл кода, но данный код можно подходить под различные задачи (по сути это АСД Set, но немного кастомизированное) и не соответствует единому дизайну. 

Опишем изначально перед классом, зачем он нужен, что он делает (но сделаем это в рамках разрабатываемой системы, **как этот кусок кода вписывается в общую систему в целом**):


```php

Данный вариант комментария не финальный, финальные будут обсуждены ниже.
/*
* Данный класс отражает АСД "Реляционная таблица"и хранит только уникальные объекты класса Row. Определение равенства объектов класса Row отражено в классе Row.
* Методы данного класса позволяют найти объекты Row по значению (содержимое сторки), набору значений, добавить или удалить строку. 
*/

class Relation
{
   //...
}
```

То есть мы говорим, что данный класс -- контейнер для объектов класса Row, он имеет методы для вставки и удаления, а также поиску значений. При этом, это будет определение в рамках разрабатываемой системы.

Теперь опишем методы insert и contains. Чтобы описать, что именно код делает, но так, чтобы пользователи класса "не догадывались", что делает код, достаточно 
описать пред и пост-условия:
```php
   
    //Pre-cond: Row's schema equals Relation's schema
    //Post-condition: Row was inserted into the Relation
    public function insert(Row $row)
    {
        if (count($this->schema) != $row->size() ||
            $this->contains($row) == true
            ) {
            $this->insert_status = Relation::INSERT_STATUS_DUPLICATE;
        } else {
            //$this->check_row_schema($row);
            $this->rows[] = $row;
            $this->insert_status = Relation::INSERT_STATUS_OK;
        }
    }

    //Pre-cond: Given a Row
    //Post-cond: Determine if relation contains given row (rows equality described in class Row).
    private function contains(Row $anotherRow) : boolean
    {
        $tmpAnotherSubRow = $anotherRow->sub_row($this->unique_key);
        foreach ($this->rows as $row) {
            /* @var $row Row */
            $tmpSubRow = $row->sub_row($this->unique_key);
            if ($row->equals($anotherRow) || (count($this->unique_key) > 0 && $tmpSubRow->equals($tmpAnotherSubRow))) {
                return true;
            }
        }
        return false;
    }
```

Тут может возникнуть вопрос вопрос: Почему мы описываем класс в рамках разрабатыаемой системы на довольно высоком уровне, а методы класса -- на более низком, то есть мы с помощью пред и пост условий **конкретизируем** (спускаемся на уровень ниже), что делает та или иная функция? Почему бы нам не описать все это перед классом?

Тут стоит понимать важный момент. Разрабатывая определенную систему, на уровне ТЗ у нас имеется некоторая абстрктная модель. На основе ТЗ формируем спецификации -- некоторая модель, но уже уровнем ниже, нежели модель абстрктная модель ТЗ. После спецификаций -- архитектура, далее графическая схема, далее код и т.д. У нас постоянно будут определяться новые модели, то есть модель модели, но уровнем ниже. Каждая единица разработки (будь то функция, класс) представляет модель модели (этих слоев может быть множество, пока не дойдет до абстрактной модели ТЗ). И стоит, как мне кажется, описывать единицу разработки в рамках высшестояшей по уровню модели (методы в рамках класса, класс в рамках модуля, модуль в рамках архитектруы и т.п.). 

Рассмотрим еще два примера:

--------
## Пример 2

Следующий пример представляет классы, которые предназначены для формирования дерева для последующего парсинга SQL запросов.
Имеется следующие классы в иерархии:

```cpp
class Tree
{
   public:
       const int TRAVEL_STATUS_NIL = -1;
       const int TRAVEL_STATUS_OK = 0;
       const int TRAVEL_STATUS_ERR = 1;
   
       virtual void travel(Node* current, std::map<std::string, std::string>& plan) = 0;
       Node* getRoot();
       int get_travel_status();
   protected:
            
       int travel_status;

       Node* root = nullptr;
       Node* current = nullptr;
 
       std::vector<std::string> splittedWords;
       void setLeft(Node* parent, Node* left);
       void setRight(Node* parent, Node* right);
       virtual void createTree(std::string& selectQuery) = 0;
   private:
};

class SelectTree : public Tree
{
   public:
       SelectTree(std::string& selectQuery);
       void travel(Node* current, std::map<std::string, std::string>& plan);

   protected:
       void createTree(std::string& selectQuery);
       void takeKeyWord();
       void takeArgs();
   private:
       void fillVector(std::string& expression);
};
```

Какие могут возникнуть вопросы, если мы будем смотреть со стороны самодокументирующегося кода?
1. Метод travel подразумевается в ширину или в глубину?
2. Метод createTree принимает в качестве аргумента любую строку, или же какую-ту строго определенную?

Попробуем добавить комментарии к коду, в рамках **вышестоящей модели**. 

```cpp

/**
* Абстрактный класс Tree представляет структуры данных, которая отражает SQL запрос в виде синтаксического дерева.
* Метод createTree должен быть определен в наследующихся от данного класса классах.
*/

class Tree
{
   //...
};

/**
* Класс SelectTree представляет структуры данных, которая отражает SQL  Select запрос в виде синтаксического дерева.
*/
class SelectTree : public Tree
{
   //...
};
```

Мы опимсали наши классы в рамках вышестоящей модели на этот раз лишь одной строкой, в отличие от первого примера. В выводе будут рассмотрены все варианты комментирования классов.

С функциями будет все намного проще:

```cpp
//Pre-cond: given existing Node and correct plan of query
//Post-cond: Tree DFS travel and current travel status was updated
void travel(Node* current, std::map<std::string, std::string>& plan);
```

Опять же, мы даем комментарии к функциям в рамках класса. Но могут быть ситуации, когда используются модули функций (математические, например), тогда их следует описывать в рамках архитектуры (или иного вышестоящего уровня модели).

--------
## Пример 3

Следующий класс отражает структуру данных в виде JSON.

```cpp

/**
* Преобразовывает строку в виде JSON для более удобной работы с JSON-raw данными.
**/

class Json
{
public:
	Json();
	Json(std::string& raw_json);
	Json(std::string& key, std::string& value);

	//Pre-cond:
	//Post-cond: set (or create if not exists) key with given value
	void setValue(std::string& key, std::string& value);
	
	//Pre-cond: key is exists
	//Post-cond: key with value was deleted from JSON
	void deleteByKey(std::string& key);
	
	//Pre-cond: given array of existed keys
	//Post-cond: keys with values were deleted
	void filter(std::vector<std::string>& keys_to_filter);
	
	void setSchema();

	//Pre-cond: key is exists
	//Post-cond: return value by key;
	std::string& get_by_key(std::string& key);
	
	//Pre-cond:
	//Post-cond:: return array of existing keys
	std::vector<std::string> getSchema();
	
	//Pre-cond:
	//Post-cond: return raw json string
	std::string to_str();

};
```

---------------------
Вывод 

На основе вышеприведенных примеров, можно высказать очевидную вещь, что комментарии позволяют внести ясность в код, но вопрос в том, какие это комментарии.
Как было сказано выше, что представление системы в виде классов -- это очередная модель модели модели, и нужно стремиться писать комментарие в рамках общей системы (в рамках более высокого уровня модели). Почему это желательно? 
1. Не имеет смысла комментировать что делает код на низком уровне, поскольку сам код это уже делает (самый низкий уровень)
2. Не стоит описывать, что делает код (уровень функций), поскольку имя функции должно говорить об этом, но стоит описывать спецификации функции (пред и пост условия). Таким образом мы, во-первых, даем понять, почему эта функция следует дизайну; во-вторых, мы не раскрываем, как работает функция;
3. Не стоит комментировать класс в рамках "что делает?". Во-первых, описание класса может следовать разным дизайнам (как в случае первого примера: Relation может отражать различный дизайн так как это просто контейнер, но описание в рамках системы дает понять, как этот класс используется в системе). Во-вторых, описывая класс в рамках "что делает" может не дать понять, а зачем этот класс нужен.
Комментирование в рамках общей системы дает более цельную картину системы со стороны кода в сторону дизайна. А пред и пост условия методов говорят о том, что класс делает.

Но тут имеется вопрос "а как описать класс в рамках общей системы, не говоря, что он делает?".Получается, мы должны дать понять, что делает класс для системы, не говоря что он делает?
И вот тут стоит обратить на важный момент: мы говорим не "что" делает класс, а "зачем" он нужен системе. В чем разница? Например, АСД словарь и список, если описывать их со стороны "что делают", то быстро придет к выводу, что добавляют/удаляют/ищут/изменяют хранящиеся данные. Но если мы будет задавать вопрос "зачем?", то поймем мотивацию использования того или иного класса в конкретной ситуации.

По итогу, для вышеприведенных классов, будут лучше следующие комментарии (методы были убраны в качестве уменьшения количества строк):

Пример 1
```php

/*
* Отражает данные в виде АСД "Реляционная таблица".
* Позволяет хранить объекты класса "Row" и взаимодействовать с ними (поиск, изменение, добавление, удаление). -- зачем нужен класс
*/
class Relation
{

};
```

Пример 2
```cpp
/*
* Отражает данные в виде АСД "Синтаксическое дерево"
* Преобразует SQL запрос в синтаксическое дерево -- зачем нужен класс
*/
class Tree
{

};

/*
* Отражает данные в виде АСД "Синтаксическое дерево"
* Преобразует SQL SELECT запрос в синтаксическое дерево. -- зачем нужен класс
*/
class SelectTree : public Tree
{

};
```

Пример 3
```cpp
/**
* Преобразовывает строковые json raw данные в виде JSON для более удобной работы. -- зачем нужен класс
**/
class Json
{

};
