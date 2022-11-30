#

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
    ParserCLI(char* argv[], int argc);
    bool parse();
    const std::string retrieveCommand();
    const std::vector<std::string> retrieveArgs();
}
```

2. Пропарсив командную строку, команда и аргументы отправлялись в класс ArgumentsFactory, для валидации корректности аргументов: 
```cpp
class FactoryArguments
{
    public:
    //...
    
    // Подаются распаршенные команда и аргументы
    std::unique_ptr<Arguments> createArgumentsInstance(const std::string& command, const std::vector<std::string&> args);
};
```

3. Полученный инстанс класса Arguments используется при создании класса Commands:
```cpp
std::unique_ptr<Command> CommandsBuilder::build(const std::string& command, const std::vector<std::string>& args)
{
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
        PathRule(const std::string& localPath);

        /**
         * Pre-conditions: 
         * Post-conditions: validates given arguments
        */
        const PATHRULESTATUSES validate();

        const char* errorMessage();
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
2. Класс ParserCLI -- парсит командную строку
3. Класс FactoryArguments создает объекты типа Agruments, НЕ взаимодействуя с терминальным вводом
4. Класс CommandBuilder -- создает класс Arguments и такж не взаимодействует с аргументами терминального ввода 
5. Класс Rules -- инкапсулирует валидацию аргументов.
6. Класс Commands -- инкапсулирует воедино Arguments и соответствующие Rules.

При корректном вызове программы, получается следующая схема:
1. На вход подается const char* argv[], int argc
2. Класс ParserCLI обрабатывает терминальный ввод.
3. Класс CommandBuilder запрашивает у класса ParserCLI команду и аргументы И передает классу ArgumentsFactory
4. Класс ArgumentsFactory создает объект типа Arguments. 
5. Далее создается класс Command с созданными Arguemnts и перед вызовом валидирует эти аргументы с помощью класса Rules.


------------------------------
2) Переделать взаимодействие с 




------------------------------
3) Переделать 
