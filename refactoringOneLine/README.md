

Пример 1
Было
```php
public function search(Row $currentRow, array $subRow)
{
  $keys = ...
  ...
  //нижеприведенная строка и создает подстроку и сравнивает по значение с ключами; итератор и вычисляет значение и приводит к string
  if($currentRow->subRow($keys)->equals($subRowKeys) && $iterBegin->at(0)->getValue()->toString() == "some")
  {
    ...
  }
}
```

Стало
```php
public function search(Row $currentRow, array $subRowKeys)
{
  $keys = ...
  $subRowFromCurrentRow = $currentRow->subRow($keys); 
  $isSubrowsEquals = $subRowFromCurrentRow->equals($subRowKeys);
  
  $iterValue = $iterBegin->at(0)-getValue();
  $isNeededValue = $iterValue->toString() == "some");
  if($isSubrowsEquals && $isNeededValue)
  {
    ...
  }
}
```
В данном случае, мы явно может отследить ошибку по строке.

=====
Пример 2
Было
```php
//И получение элемента, и сравнение его.
$this->listViewResult = $entity->entityList()->get()->first()->compare($toCompare);
```

Стало
```php
//Убираем метод гет, добавляем срауз доступ к первому элементу, а-ля очередь
$firstEntity = $entity->entityList()->first();
$areEntitiesEqulas = $firstEntity->compare($toCompare);
```

=====

=====
Пример 3
Было
//вызов методов внутри параметров других методов
```php
$isKeyExists = key_exists('type', $this->helper->getColumns($this->helper->getGroupType));
```

Стало
//Вынос в отдельные переменные
```php
$columnToPick = $this->helper->getGroupType;
$arrayWithKeys = $this->helper->getColumns($columnsToPick);
$isKeyExists = key_exists('type', $arrayWithKeys);
```

=====

=====
Пример 4
Было
//вызов методов внутри параметров других методов
```php
$this->addTableTotalFinancialValues($this->helper->getCompaniesFinancials(), $this->helper->getCorrectedCompaniesFinancials());
```

Стало
//Вынос в отдельные переменные
```php
$correctedCompaniesFinancials = $this->helper->getCorrectedCompaniesFinancials();
$companyFinancials = $this->helper->getCompaniesFinancials(); 
$this->addTableTotalFinancialValues($companyFinancials, $correctedCompaniesFinancials);
```

=====

=====
Пример 5
Было
```php
//Вызов методов внутри методов
return $this->references_table->search_row_by_index($fk->getId(), $this->referenced_table->get_primary_key());
```

Стало
```php
//Вынос методо в переменные 
$fkId = $fk->getId();
$primaryKeyOfTable = $this->referenced_table->get_primary_key();

return $this->references_table->search_row_by_index($fkId, $primaryKeyOfTable);
```

=====

=====
Пример 6
Было
```php
//Испольозвание вычислений внутри функций с константами чревато ошибками 
if($parentRow->at($parentRow->size()-1)->getValue() > $row->at($row->size()-1)->getValue())
```

Стало
//Добавим "Итератор" и вынос в отдельные переменные
```php
$lastColumnOfParentRow = $parentRow->last();
$lastColumnOfGivenRow = $row->last();
if($lastColumnOfParentRow > $lastColumnOfGivenRow)
```

=====
Вывод: подобные изначальные приемы, когда писали в одну строку инструкции, возможно, применялись, чтобы не засорять методы $tmp-переменными.
Но такой код:
1. Труднее отлаживать -- компилятор/фреймворк может выдасть просто номер строки, в которой 3-4 метода придется отлаживать
2. Труднее читать
3. Нельзя поставить инструкцию assert()
4. Когда мы присваиваем результат переменной единжды, получается некое подобие "dataflow"-переменной. (при условии, что мы ее не меняем)

Вынос в отдельные переменные промежуточные результаты увеличивают количество строк, но делают код более читабельным, позволяют добавлять assert'ы, что особенно важно.
Ведь если одна строка делает вещь А, а следующая строка делает вещь Б и обе эти строки равно, то и выполнится строка С.
В одну строку получается так: строка делает вещь А, вещь Б, вещь С, и какая из них неверная -- не всегда будет понятно с первого раза.



Но однострочные функции применимы к алгоритмам, включающие в себя лямбда-функции, хотя можно и вынести лямбда-функцию в отдельную переменную.

