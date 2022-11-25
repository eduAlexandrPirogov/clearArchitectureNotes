# Коструируем корректный дизайн

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
public function defineType(string $type)
{
   if(trim($type) == 'план)
      return Months::TYPE_PLAN;
   if(trim($type) == 'факт')
      return Months::TYPE_FACT
   ...
   
   return MonthType::Nothing
   //throw new exception...
}

public function readMonth(array $data)
{
    foreach(...)
    {
    ....
       if($type == $this->defineType($data[0][$column])
          throw new Exception...
    }
}
```

Стало:
```php
$MonthTypes = [
   'план' => Months::TYPE_PLAN,
   'факт' => Months::TYPE_FACT,
   ...
]

//удаляем функцию defineType

public function readMonth(array $data)
{
    foreach(...)
    {
    ....
       if(!array_key_exists($data[0][$column], $MonthTypes)
          throw new Exception...
    }
}
```
Избавились от 6 if-ов просто сузив до минимума домен для функции  defineType, но потом, как выяснилось, от этой функции в целом омж

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
   public const $delimeters = [
       Delimeters::COMMA => ',',
       Delimeters::COLON => ';',
       Delimeters::SEMICOLON => ':'
   ];
   
    public const $escapeCharacters = [
       EscapeCharacters::BACKSLAH => ',',
       ...
   ];
  //...
   
   public function saveDataCsv(Delimeters $delimeter, $escape_character, $enclosure)
   {
      //Настройка файла и запись
   };
  
}
```
 
