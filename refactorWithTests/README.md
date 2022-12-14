# Проектные ошибки

1) Схема приложеня для загрузки и скачивания файла с dropbox с помощью API:
Было:
1. Поступала команда в виде const* char[], int argc (границы нельзя изменить).
2. Данная строка валидировалась внутри класса CommandParser.
3. CommandParser имел команды-запросы, string getCommand(), std::vector<std::string> getArgs(), чтобы получить результат распаршенной команды. 
4. Был класс ArgumentValidator, валидирующий аргументы для команды get/put.
5. Если аргументы проходили валидацию и пользователь указывал верную команду, создавался класс Command, который принимал в качестве параметров аргументы.

Что было сделано:
1. Создан класс ParserCLI, который парсил командную строку и хранил команду и аргументы команды.
```cpp
class ParserCLI
{
   public:
    //Границы для работы с парсером
    ParserCLI(char* argv[], int argc);
    bool parse();
    const std::string retrieveCommand();
    const std::vector<std::string> retrieveArgs();
}
```

2. Пропарсив командную строку, команда и аргументы отправлялись в класс ArgumentsFactory, для валидации корректности аргументов. Обозначаем границы через интерфейс класса (метод createArgumentsInstance)
```cpp
class FactoryArguments
{
    public:
    //...
    
   //Аргументы создаются только через команды и набор аргументов. Остальные конструктора удалены
    std::unique_ptr<Arguments> createArgumentsInstance(const std::string& command, const std::vector<std::string&> args);
};
```

3. Полученный инстанс класса Arguments используется при создании класса Commands:
```cpp
//Границы работы метода -- мы всегда получаем список команды в виде КОМАНДА АРГУМЕНТ_КОМАНДЫ_1 АРГУМЕНТ_КОМАНДЫ_2...
std::unique_ptr<Command> CommandsBuilder::build(const std::string& command, const std::vector<std::string>& args)
{
    //Аргументы создаются только через команды и набор аргументов. Остальные конструктора удалены
    std::unique_ptr<CommandParserWithoutConfig> commandParser = std::make_unique<CommandParserWithoutConfig>(command, argc);
    commandParser->parse();
    
    std::unique_ptr<Arguments> args = std::move(commandParser->getParsedArguments());
    
    auto findResult = commandsTable->find(command);
    std::unique_ptr<Command> cmd = findResult != commandsTable->end() ? std::move(commandsTable->operator[](command)(args)) 
        : std::move(commandsTable->operator[]("invalid")(args)) ;
    return cmd;
};
```
4. Для валидации аргументов, создан отдельный класс Rules, который имеет абстрактный метод validate(). В зависимости от ситуации, можно добавить свою валидацию.
Класс выглядит следующим образом:

```cpp
enum PATHRULESTATUSES
{
    SOURCE_FILE_EXISTS,
    SOURCE_FILE_NOTEXISTS,
    SOURCE_DIRECTORY_EXISTS,
    SOURCE_DIRECTORY_NOTEXISTS,
    INCORRECT_ARGUMENTS_COUNT,
    INVALID_PATH,
    INVALID_ARGUMENTS
};

/**
 * Class to Validate types of Arguments
*/
class Rule
{
    public:
        virtual const PATHRULESTATUSES validate() = 0;
};

class PathRule : public Rule
{
    std::string localPath;
    PATHRULESTATUSES currentParseStatus;
    std::unordered_map<PATHRULESTATUSES, const char*> argumentsMessage;
    public:
        PathRule() = delete;
        /**
         * Pre-conditions: given name of existing file
         * Post-conditions: instance of PathRule created
        */
        //Пути указываются в виде строки
        PathRule(const std::string& localPath);

        /**
         * Pre-conditions: 
         * Post-conditions: validates given arguments
        */
        const PATHRULESTATUSES validate();

        const char* errorMessage();
};

class GetCommandArguments : public Arguments
{   
        PATHRULESTATUSES parseStatus;
        std::unique_ptr<PathRule> pathRule;
    public:
        GetCommandArguments() = delete;
        //Удаляем остальные конструкты
        
        //Обозначаем явные границы для начала работы с классом
        GetCommandArguments(const std::vector<std::string>& givenArgs);

        bool validate();
        inline PATHRULESTATUSES status() 
        {
            return parseStatus;
        }

        virtual const char* errorMessage();
};
```

5. Перед исполнением команды, если аргументы не проходят валидацию, программа завершается и выдает ошибку:

```cpp
void PutCommand::execute(RequestHandler* handler)
{
    validateArgs();
    handler->handleRequest(this);
};

void PutCommand::validateArgs()
{
    bool argsIsValid = args->validate();
    if(!argsIsValid)
    {
        std::string ArgError = "\n\n\n+-------------ERROR!-------------+\n";
        ArgError += "|"; ArgError+= args->errorMessage(); ArgError += "      |\n";
        ArgError +=  "+--------------------------------+\n";
        
        throw std::runtime_error(ArgError);
    }
    
};
```

Таким образом:
1. Мы дефакторизовали реализацию на следующие "ответственности": пропарсить командную строку, создать аргументы, создать команду, провалидировать команду.
2. Класс ParserCLI -- парсит командную строку. Для работы с классом нужны char* argv[]. Далее никакой класс не работает с char* argv[], int argc.
4. Класс FactoryArguments создает объекты типа Agruments, НЕ взаимодействуя с терминальным вводом. Для работы с классом нужны string Command и vector<string> args.
5. Класс CommandBuilder -- создает класс Arguments и такж не взаимодействует с аргументами терминального ввода. Для работы с классом нужны string Command и vector<string> args (поскольку он передает их в ArgumentsFactory).
6. Класс Rules -- инкапсулирует валидацию аргументов. 
7. Класс Commands -- инкапсулирует воедино Arguments и соответствующие Rules.

Несмотря на то, что на вход подавались char* argv[], int argc, то мы, создав класс ParserCLI, сужаем границы дозволенной работы с программой, т.е. границы мы задаем явно через интерфейс классов.

Таким образом мы:
1. Избавили классы от работы с char* argv, возможности ошибок из-за неправильного индекса.
2. Каждый класс работает изолированно. Можно построить систему, фактически построив последовательную цепочку использования классов.

При корректном вызове программы, получается следующая схема:
1. На вход подается const char* argv[], int argc
2. Класс ParserCLI обрабатывает терминальный ввод.
3. Класс CommandBuilder запрашивает у класса ParserCLI команду и аргументы И передает классу ArgumentsFactory
4. Класс ArgumentsFactory создает объект типа Arguments. 
5. Далее создается класс Command с созданными Arguemnts и перед вызовом валидирует эти аргументы с помощью класса Rules.


------------------------------
2) Рефакторинг парсинга csv-файла и преобразование данных в csv в сиды для реляционной СУБД.
   

Последовательность действий такая:
1. Пропарсить файл (пропустим момент)
2. Закинуть данные в структуру данных "множество".
3. Провалидировать данные (чтобы дата была одного формата)
4. Установить связи между множествами (аналог foreignKey)
   
Изначально было сделано следующим образом:

```php
$relation = new Relation('table_name');
foreach($dataArray as $data)
{
   $row = new Row($data[0], $data[1]...);//Валидируем внутри данные с помощью методов validateDate($data), validateNumeric($data)...
   $relation->append($row);
}
```

И если понадобится сделать foreign key на другую таблицу, то:
   
```php
$relation = currentRelation();
$related = tableToRelate();
$rows = $relation->getRows();
foreach($rows as $row)
{
    //Ищем по совпадению данных
    $fkindex = $related->search($row);
    if($fkindex != -1)
        $row->pushFront($fkindex);
};
```
   
Рефакторинг.
Еще раз отметим алгорит:
   
Последовательность действий такая:
1. Закинуть данные в структуру данных "множество".
2. Провалидировать данные (чтобы дата была одного формата)
3. Установить связи между множествами (аналог foreignKey)
   
Первый шаг довольно простой, АСД принимает на вход строки, которая содержит значения.
Что было изменено:
   
1) Создана иерархия классов Column: DateColumn, IntColumn, StringColumn ..etc, которая на вход принимала данные и валидировала внутри себя

Например, DateColumn:
```php
class DateColumn extends Column
{

   public function __construct__($data)
   {
      //Внутри мы валидируем данные
      validate($data);
   }
   
   public function value()
   {
      return $this->value;
   }
}
```
   
2) Теперь строки содержат контейнер подобных Column.
3) Также класс Relation содержит схему, которую могут принимать строки. Теперь нельзя добавлять строки в отношение, которые имеют различную схему.
   
```php
class Relation
{
   public function __construct__($name, array $schema)
   {
      $schema = [DateColumn::class, IntColumn::class, ...]
   }
}
```
   
4) Также был добавлен классы ForeignKeyColumn и ForeignKeySearch, которые отвечали за поиск id, для ссылки на другую таблицу.
   
```php
class ForeignKeyColumn extends Column
{
      
}
   
class ForeignKeySearch
{
    public function __construct__(Relation $relatedTable, $rowToRelate)
    {
      //...
    }
   
     public function createForeignKey()
     {
        $this->search($this->relatedTable, $this->rowToRelate);
        if($this->search_status == self::SEARCH_STATUS_OK)
            return $this->currentFk;
        //..
     }
}
```
   
И теперь создание таблицы выглядит следующим образом:

```php
$relation = new Relation("table_name", [IntColumn::class, DateColumn::class];
foreach($csv_data as $data)
{
    $row = new Row([new IntColumn($data[0], new DateColumn($data[1]),..);
    $relation->append($row);
}
```

Получилось следующее:
1. Иерархия классов Column -- на вход подается значение, которое валидируется внутри класса. Таким образом нигде в системе, кроме как в модуле Columns не валидируются данные.
2. Для ForeignKey созданы два класса, которые инкапсулируют логику поиска ForeignKey. Таким образом, в системе нигде не происходит поиск строки, на которую стоит ссылаться, кроме как в ForeignKey и ForeignKeySearch классах.
3. Класс Row, как и класс Relation имеют схемы -- массив, состоящий из классов-Columns для валидации вставки строк одной схемы. Таким образом мы сузили круг, при которых программа может сработать корректно при некорректных данных.
4. Класс Row принимает на вход теперь конкретные данные. Явно указываем варианты, при которых класс будет работать.
   
Границы классов:
На вход подается csv-файл, который преобразуется в массив со значениями. Мы создали для работы с данными граничными значенияси иерархию классов Column, который будет работать с соответствующим форматом данных. Для нового формата данных, будет создан новый класс Column, работающий с данными. При этом легко добавлять подобные классы и валидировать. Код валидации данных более не размазан по программной системе.

# Тесты

Теперь попробуем написать тесты, которые показывают, как классы  Columns влияют на работу системы. 
По отношению к системе, если входящие данные невозможно провалидировать, то выбрасывается исключение. В противном случае, работы программы продолжается.

```php
pest('Assert that dateColumn throws excpetion with incorrect data' ,functinon($invalidDate)
{
    $this->expectException(InvalidArgumentException::class);
   //example of invalid dates
   $dateColumn = new DateColumn('yyyy-mm-dd', $invalidDate);

})->with(['20211242', 'qwr-32-wq', '0000/00/00', '2035-20-20']); 

pest('Assert that numericColumn throws excpetion with incorrect data' ,functinon($invalidDate)
{
    $this->expectException(InvalidArgumentException::class);
   //example of invalid dates
   $dateColumn = new NumericColumn($invalidDate);

})->with(['20', '1', 'q', '203']); 
```

------------------------------

3) Я попытался сделать рефакторинг еще на паре рабочих проектах, на старых своих, но по итогу у меня ничего не вышло. 
Ниже я привел трудности, с которыми столкнулся ниже.

-------------------
Вывод.

Я не обладал опытом рефакторинга (обычно мой рефакторинг склонялся к переписыванию с нуля). В процессе попытки отрефакторить столкнулся со следующими проблемами:
1. У меня падали тесты и тесты приходилось переписывать, точнее следовать следующему алгоритму:
   1.1 У нас имеются старые тесты А для участка кода К.
   1.2 Пишем новые тесты Б для участка кода К, которую собираемся рефакторить. Тесты Б не проходят, тесты А -- проходят.
   1.3 Стараемся рефакторить так, чтобы тесты Б проходили, а тесты А -- нет.
   1.4 В процессе рефакторинга приходилось затрагивать другие классы, для которых также писались тесты.
   
   По итогу такой процесс занимал длительное время, если классы были сильно завязаны друг на друге (я пытался сделать на нескольких ранних проектах, но в итоге 
   сходилось все к переписыванию с нуля. Еще одна причина, по которой нужно стараться делать код модульным, самостоятельным. 
   
2. Рефакторинг -- это не "разовая" уборка раз в месяц, а скорее ежедневный ритуал по поддержке чистоты кода. Рефакторить проект, который давно никто не смотрел, который держится еле-еле -- себе дороже (убедился на себе). Особенно, если используются стороние библиотеки, которые с разными версиями могут работать некорректно, от этого больше бед, чем пользы. Переписать систему, которая работает давно и работает кое-как -- довольно проблемно. А когда на проекте нет тестов, то рефакторить,как мне кажется, бесполезно.

3. Рефакторинг -- "пересказ смысла, но более кратко и точно". И такой процесс (по крайнер мере у меня), занимает довольно долгое время. Нелегко оторвать мозг от "уже готового решения", особенно когда имеется уже готовая схема решения. Скорее тут стоит посмотреть со стороны "как представить данный участок кода", если использовать другие структуру данных и как они будут взаимодействовать между собой.

4. Рефакторинг -- это сигнал о том, что изначально система была плохо спроектирована. И тут возникает вопрос, зачем же нужен рефакторинг. С одной стороны, это может упростить систему на основе существующей -- мы видим, к чему нас привели спецификации, как данные взаимодействуют между собой, мы видим концепты системы, которые можем отразить напрямую в коде. Но тут скорее поможет не рефакторинг, а переписывания с нуля нового модуля и его подключение к системе. 

5. Рефакторить код, по которому нет документации, у которого нет тестов и нет комментариев -- себе дороже. Попытавшись отрефакторить проект, который принимал файл в FTP, агрегировал его, формировал данные для БД, а также формировал новые файл, в котором был только голый код, я потратил много нервов и сил, но ни к чему не пришел.
Тяжело, когда в проекте сильная связность между сущностями, и при попытке пересобрать логические единицы, переписываются более 10-15 классов, что опять же сводится к переписыванию модуля с нуля.

Ну и последнее, перед рефакторингом, лучше будет изучить стандартную литературу по рефакторингу. И желательно не приходить к нему вообще.

Возможно, мне просто нужно было больше подумать, но в среднем уходило по 3-4 часа на обдумывание, как сделать код более лучше. Но я больше задавался вопросом, "а что вообще тут происходит?" вместо "Как это сделано?".
