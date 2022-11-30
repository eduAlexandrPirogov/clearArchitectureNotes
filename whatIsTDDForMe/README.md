# Что TDD есть для меня

Я использую TDD уже больше больше, чем полгода, и могу сделать некоторую рефлексию по имеющемуся опыту. Мой TDD, со временем, перешел от максималисткого
до такого "гибридного", и объясню почему далее.

Прежде, опишу плюсы TDD, который начинал использовать, как только изучил данную технику, и старался следовать ей "максимально" строго:
1. Изменилось мышление о создании классов (не системы!!!); в купе с  АТД спроектированные классы получилась гибкими -- их можно было использовать несколько раз
2. Со временем, возвращаться к проекту становилось проще -- если нужно добавить фичу или изменить что-то, то делалось с тестами это легче (Но речь прежде всего о локальной проблеме)
3. Если имелись споры в команде, то достаточно было обратиться к тесту, показать сеньору/ПМ'у, спросить "верно ли тест отрабатывает для заданного домена значений?",из-за чего спроы решались довольно быстро.
4. Локальный дизайн (второй уровень) выходил более качественным, нежели до TDD.

Используя TDD, принес свои плоды, но также, я сталкивался со следующими проблемами:
1. Большое количество методов в классах. Если мы создаем один относительно большой метод, то нам сложнее его тестировать, для него придется писать несколько тестов, что нарушает SRP (один тест тестирует одну вещь).
2. Также проблема с доступом к методами -- маленькие методы зачастую закрыты. Делать их публичными -- нелучшая идея, поскольку нарушает интерфейс класса (типа данных).
3. Тесты ограниченны программистом -- если имеется метод А, который принимает множество значений K {k1,...kn,...}, то, в лучшем случае, если я смогу определить 50% тестирования различных ситуаций из множества K. Тут хорош  фаззинг, нежели TDD.
4. Несмотря, на то, что тесты делают локальный(!!!) код лучше, из этого не следует, что весь дизайн станет лучше, из-за чего я однажды оступился на работе.
5. Не все виды ситуаций (как мне кажется) можно сделать с TDD.

По мере применения TDD, я ушел от "самого правильного" TDD к своему гибриду, следуя в основном TCR (но 100% чистому, тоже немного под себя изменил): 
к TDD приступаю как можно позже, пока не буду уверен в хорошем проектировании класса/модуля/проекта на бумаге. Да и воспринимаю использование TDD не как "путеводитель по созданию системы",
а как "метки на деревьях, путешествуя по лесу", чтобы в случае чего можно было вернуться в определенную точку.
TDD -- инструмент, который нужно применять только в подходящей ситуации. 

Какие по итогу имею достоинства применения данной техники/инструмента:
1. Некая верификацию корректности кода
2. Некая верификация хорошо спроектированного класса.
3. Формальное отражение корректности локального кода (но не системы опять же). Если меня спросят, почему сделал так или иначе, то просто показываю тесты.