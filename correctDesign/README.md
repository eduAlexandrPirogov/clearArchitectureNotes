# Конструируем корректный дизайн

Убрать проверку "на дурака" можно различными способами. Прежде чем подойти к ним, нужно понять, почему нам вообще приходится использовать
защиту "от дурака".

Зачастую, данные приходят в качестве аргументов. Данные имеют тип, который отражает множество всех возможных значений этих данных.
Например, если функция имеет в качестве параметра целочисленное число, то в качестве аргумента может прийти любое значение множества целочисленных.
Если функция имеет в качестве параметра строку, но нам может придти бесконечное множество строк.

Чтобы улучшить надежность кода, лучше **не пытаться охватить все возможные случаи** работы с данным типом данных, а **ограничить/сузить область множества типа данных**.

Например, у нас имеется функция, которая принимает на вход строку-команду, и в зависимости, от данной команды, выполняем определенное действие.
Тут можно либо:
1. создать if-ы, чтобы проверить на корректность, тем самым мы просматриваем все возможные варианты работы функции;
2. определить множество **допустимых** значений (например, в качестве словаря).

Теперь рассмотрим методы,как можно достичь подобных "сокращений". 
Допустим, наша функция принимает в качестве параметр А типа Т. Тогда, мы можем сконструировать собственный тип данных Т`, который будет являться
подмножеством множества типа Т. 
Например, у нас имеется тип данных целочисленное, а мы хотим валидировать возраст. Можно создать тип данных "Возраст", который будет являться
подмножеством множества целочисленные. (Пример очень примитивный).

Или, например, если на вход подается строка, то проще создать тип данных, который будет содержать в себе только некоторые значения из тип данных "строка".

Как создавать подобные "подмножества":
1. Создать классы
2. Создать перечисления
3. Создать словари

Рассмотрим примеры:

Создание подмножеств посредством словаря:
1)
Было:
```cpp
//Подобие факторки для создания конкректного типа Arguments на основе данной строки. 
std::unique_ptr<Arguments> ArgumentsFactory::createArgumentInstance(const std::string& command, const std::vector<std::string>& args)
{
    current_create_status = true;
    //ADT dictionary would be great here
    if(command == "get")
    {
        return std::make_unique<GetCommandArguments>(args);
    } 
    if(command == "put")
    {
        return std::make_unique<PutCommandArguments>(args);
    }
    current_create_status = false;
    return std::make_unique<InvalidCommandArguments>();
};
```

Стало:
```cpp
//Создаем только доступные перечисления
enum CommandsEnum
{
  GET, PUT, INVALID
}

//В классе имеется внутреннее поле словарь, типа ArgumentsNewInstances <CommandsEnum, std::function<std::unique_ptr<Arguments>(std::vector<std::string>&)>>

std::unordered_map<CommandsEnum, std::function<std::unique_ptr<Arguments>(std::vector<std::string>&)>> argumentsNewInstances;

//Новообновленный метод
std::unique_ptr<Arguments> ArgumentsFactory::createArgumentInstance(CommandsEnum command, const std::vector<std::string>& args)
{
    return argumentsNewInstances[command];
};
```
Тем самым мы удалили if-else в методе createArgumentInstance, сократили возможные варианты для корректного вызова метода createArgumentInstance.
Теперь, мы явно даем понять, какие значение -- корректные, а какие -- нет.

Создание подмножеств посредством перечислений:
2)

Было:
```cpp
//Метод, который с помощью libcurl исполняет запрос. Нижеприведенный метод принимает в качестве параметра строку.
void setUrl(const char* url)
{
  curl_easy_setopt(curl, CURLOPT_URL, url); 
}

```

Стало:
```cpp
/**
 * Enum to escape writing URL as const char*
*/
enum DROPBOX_API_URLS
{
    DOWNLOAD_FILE, UPLOAD_FILE, RETRIEVE_BEARER, FILE_METADATA
};

/**
 * ATD that contains dropbox API URLS
*/
class DropboxUrlContainer
{
    std::unordered_map<DROPBOX_API_URLS, char*> dropboxUrls;
    public:
        DropboxUrlContainer()
        {
            dropboxUrls[DROPBOX_API_URLS::DOWNLOAD_FILE] = "https://content.dropboxapi.com/2/files/download";
            dropboxUrls[DROPBOX_API_URLS::UPLOAD_FILE] = "https://content.dropboxapi.com/2/files/upload";
            dropboxUrls[DROPBOX_API_URLS::RETRIEVE_BEARER] = "https://api.dropbox.com/oauth2/token";
            dropboxUrls[DROPBOX_API_URLS::FILE_METADATA] = "https://api.dropboxapi.com/2/files/get_metadata";
        };

        inline const char* find(DROPBOX_API_URLS key)
        {
            return dropboxUrls.find(key)->second;
        }
};

void setUrl(DROPBOX_API_URLS dropboxUrl)
{
  curl_easy_setopt(curl, CURLOPT_URL, dropboxUrl); 
}

auto dropboxUrl = dropboxUrls->find(DROPBOX_API_URLS::DOWNLOAD_FILE); //Any of AVAIBLE Url
setUrl(dropboxUrl);
```
Мы выделили контейнер для хранения URL-ок в отдельных АТД класс, обезопасили себя от некорректного вода URL, и URl-ки находятся в едином месте и не 
размазаны по проекту.
К тому же, если мы явно хотим устновить URL, то программисту-клиенту будет доступен метод, параметр которого -- множество DROPBOX URL-ок.

3)
Было:
```cpp
class GetCommand : public Command
{
    std::unique_ptr<GetArguments> args;
public:
    GetCommand() = delete;
    GetCommand(const GetCommand&) = delete;

    //Тут может передаваться любое значение
    GetCommand(const char* givenArgs);
    virtual void execute(RequestHandler* handler);
    virtual string strForPrint();
    virtual void validateArgs();
};

class PutCommand : public Command
{
    std::unique_ptr<PutArguments> args;
public:
    PutCommand() = delete;
    //Тут может передаваться любое значение
    PutCommand(const char* givenArgs);
    virtual void execute(RequestHandler* handler);
```

Стало:
```cpp
//Создаем класс-аргумент, где мы обрабатываем низкоуровневую логику.

/**
 * Class that handles arguments of Get Command to downlaod files from DropBox
*/
class GetCommandArguments : public Arguments
{   
        PATHRULESTATUSES parseStatus;
        std::unique_ptr<PathRule> pathRule;
    public:
        GetCommandArguments() = delete;
        GetCommandArguments(const std::vector<std::string>& givenArgs);
};

/**
 * Class that handles arguments of Put Command to upload files to Dropbox
*/
class PutCommandArguments : public Arguments
{   
        PATHRULESTATUSES parseStatus;
        std::unique_ptr<PathRule> pathRule;
    public:
        PutCommandArguments() = delete;
        PutCommandArguments(const std::vector<std::string>& givenArgs);
       //...
};

class GetCommand : public Command
{
    COMMANDS commandGet;
    std::unique_ptr<Arguments> args;
public:
    GetCommand() = delete;
    GetCommand(const GetCommand&) = delete;
    //Сужаем множество строк до подмножества
    GetCommand(std::unique_ptr<GetArguments>& givenArgs);
    GetCommand(COMMANDS command, std::unique_ptr<Arguments>& givenArgs);
};

class PutCommand : public Command
{
    COMMANDS commandPut;
    std::unique_ptr<Arguments> args;
public:
    PutCommand() = delete;
    
    //Сужаем множество строк до подмножества
    PutCommand(std::unique_ptr<PutArguments>& givenArgs);
```
Несмотря на то, что за пределами вышеприведенного кода все равно осталось обработка const char* commandLine, мы запретили
в класс Command доставлять const char*, создавать его экземпляры без аргументов -- тем самым сузили возможные варианты создания класса.

Класс Arguments будет валидировать аргументы внутрит себя, и если данные аргументы не верны -- то выдается ошибка.

4)
Тут идет проверка низком уровне. На высоком уровне мы передаем функции строку, но внутри идет проверка...при каких значених будет корректно переданная строка, а при каких нет

Было:
```php
//Клиент-программист не знает, какую таблицу можно подставить, какую дату в каком формате, какое число будет валидным сервисом, а какое -- нет
public function getThreeMonthsFarFromInputDtae(string $table, string $from_date, int $service_id, array $monthsAgo)
{
    $rows = DB::table($table)->select(...)
                    ->where('service_id', '=', $service_id)
                    ->where('date', '>=', date('Y-m-01', strtotime("-$monthsAgo[0] month, strtotime(date('Y-m', strtotime($from_date))))))
                    ...
    $this->calculateForecast($rows);
}
```

```php
//Делаем wrapper над примитивным типом
class Date
{
    public function __construct__(string $date)
    {
        //валидируем и устаналиваем значение date корректного формата
    }
    
    //...
}

//Создаем словарь для таблиц, которые можно использовать

enum TablesForForecast
{
   case TABLE1;
   case ...
}


//Field for class
public const TABLES_FOR_FORECAST = [
       Delimeters::TABLE1 => 'table1',
       //...
   ];


public function getThreeMonthsFarFromInputDate(self::TABLES_FOR_FORECAST $table, Date $from_date, Service $service_id, array $monthsAgo)
{
    $rows = DB::table($table->toString())->select(...)
                    ->where('service_id', '=', $service_id->id())
                    ->where('date', '>=', date('Y-m-01', strtotime("-$monthsAgo[0] month, strtotime(date('Y-m', strtotime($from_date->toString()))))))
                    ...
    $this->calculateForecast($rows);
}
```
В данном случае были три проблемы-параметра метода getThreeMonthsFarFromInputDate:
1. string $table -- пользователь программист мог подставить любое строкровое значение
2. string $from_date -- тут не указан явно формат, что могло привести к проблемам
3. int $service_id -- отрицательные значения, значения, под которыми сервис не существует.

Что было сделано?
1. string $table -> перенесли в свойства класса, где расположен метод getThreeMonthsFarFromInputDate, задали только доступные имена таблиц для вызова метода.
2. string $from_date -> вынесли в отдельный класс, который внутри себя обрабатывает, валидирует и устанавливает нужный формат входящей строки, тем самым перенесли все проверки из метод в отдельный класс.
3. int $service_id -> сделали параметром модели, т.к. модель будет создана на основе данных в БД, тут мы убираем возможность ошибиться за счет имеющихся инструментов фреймворка.

5)
Было:
```php
class DataSaver
{

  //...
   
   //Какой $delimeter будет валидным а какой нет? Аналогично с другими параметрами
   public function saveDataCsv($delimeter, $escape_character, $enclosure)
   {
      //Настройка файла и запись
   };
  
}
```

Стало:
```php
enum Delimeters
{
   case COMMA;
   case COLON;
   case SEMICOLON;
   
}

enum EscapeCharacters
{
   case BACKSLAH;
   case ...
}

class DataSaver
{
   public const DELIMETERS = [
       Delimeters::COMMA => ',',
       Delimeters::COLON => ';',
       Delimeters::SEMICOLON => ':'
   ];
   
    public const ESCAPECHARACTERS = [
       EscapeCharacters::BACKSLAH => ',',
       ...
   ];
  //...
   
   public function saveDataCsv(self::DELIMETERS $delimeter, sefl::ESCAPECHARACTERS $escape_character, $enclosure)
   {
      //Настройка файла и запись
   };
  
}
```
 
В первом варианте, в  методе saveDataCsv мы могли поставить любой $delimeter, $escapre_character, тем самым пришлось бы валидировать данные внутри метода.
Вынеся параметры в перечисления, мы явно даем понять, какое множество значений допускается для метода saveDataCsv.
