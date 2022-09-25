


Логический дизайн следующий: программа, имеющая некоторый набор статистических данных, позволяет эти данные визуализировать в виде графиков.
Графики могут быть разного типа: 
1. Столбчатый
2. Точечный
3. Линейный
То есть, у пользователя имеется кнопка выбора графика, который может менять. Графики можно комбинировать, то есть на одной оси координат могут присутствовать разные
виды графиков.
Имеется следующий код отрисовки графиков:

```cpp
void GraphBuilderDCPanel::Paint(Graph* graph)
{
    int exists = 0;
    std::vector<Graph*>::iterator it = graphs.begin();
    for (; it != graphs.end(); ++it)
    {
        if (graph->compare(*it))
        {
            *it = graph;
            exists = 1;
            break;
        }
    }
        
    wxClientDC dc(this);
    dc.Clear();
    if(exists==0)
        graphs.push_back(graph);
    for (auto& graph : graphs)
    {
        if (graph->getType() == "Линии")
        {
            DrawGraphLine(graph);
        }
        else if (graph->getType() == "Столбцы")
        {
            DrawGraphColumn(graph);
        }
        else {
            DrawGraphDotted(graph);
        }
    }
}

void GraphBuilderDCPanel::DrawGraphLine(Graph* graph)
{
   wxClientDC dc(this);
    wxGraphicsContext* gc = wxGraphicsContext::Create(dc);
    if (gc && graphs.size() <= 0)return;
    
    wxFont titleFont = wxFont(wxNORMAL_FONT->GetPointSize() * 2.0,
    wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD);
    gc->SetFont(titleFont, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);
    
    gc->SetFont(*wxNORMAL_FONT, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);
    auto value = graph->xValues();
    double tw, th;
    gc->GetTextExtent(this->title, &tw, &th);
    const double titleTopBottomMinimumMargin = this->FromDIP(10);

    wxRect2DDouble fullArea{ 0, 0, static_cast<double>(GetSize().GetWidth()), static_cast<double>(GetSize().GetHeight()) };

    const double marginX = fullArea.GetSize().GetWidth() / 8.0;
    const double marginTop = std::max(fullArea.GetSize().GetHeight() / 8.0, titleTopBottomMinimumMargin * 2.0 + th);
    const double marginBottom = fullArea.GetSize().GetHeight() / 8.0;
    double labelsToChartAreaMargin = this->FromDIP(10);

    wxRect2DDouble chartArea = fullArea;
    chartArea.Inset(marginX, marginTop, marginX, marginBottom);

    gc->DrawText(this->title, (fullArea.GetSize().GetWidth() - tw) / 2.0, (marginTop - th) / 2.0);

    wxAffineMatrix2D normalizedToChartArea{};
    normalizedToChartArea.Translate(chartArea.GetLeft(), chartArea.GetTop());
    normalizedToChartArea.Scale(chartArea.m_width, chartArea.m_height);

    double lowValue = min();
    double highValue = max();

    int segmentCount;
    double rangeLow;
    double rangeHigh;
    std::tie(segmentCount, rangeLow, rangeHigh) = calculateChartSegmentCountAndRange(lowValue, highValue);

    double yValueSpan = rangeHigh - rangeLow;
    lowValue = rangeLow;
    highValue = rangeHigh;

    double yLinesCount = segmentCount + 1;

    wxAffineMatrix2D normalizedToValue{};
        normalizedToValue.Translate(0, highValue);
        normalizedToValue.Scale(1, -1);
        normalizedToValue.Scale(static_cast<double>(value.size() - 1), yValueSpan);

        gc->SetPen(wxPen(wxColor(128, 128, 128)));

        for (int i = 0; i < yLinesCount; i++)
        {
            double normalizedLineY = static_cast<double>(i) / (yLinesCount - 1);

            auto lineStartPoint = normalizedToChartArea.TransformPoint({ 0, normalizedLineY });
            auto lineEndPoint = normalizedToChartArea.TransformPoint({ 1, normalizedLineY });

            wxPoint2DDouble linePoints[] = { lineStartPoint, lineEndPoint };
            gc->StrokeLines(2, linePoints);

            double valueAtLineY = normalizedToValue.TransformPoint({ 0, normalizedLineY }).m_y;

            auto text = wxString::Format("%.2f", valueAtLineY);
            text = wxControl::Ellipsize(text, dc, wxELLIPSIZE_MIDDLE, chartArea.GetLeft() - labelsToChartAreaMargin);

            double tw, th;
            gc->GetTextExtent(text, &tw, &th);
            gc->DrawText(text, chartArea.GetLeft() - labelsToChartAreaMargin - tw, lineStartPoint.m_y - th / 2.0);
        }

        wxPoint2DDouble leftHLinePoints[] = {
            normalizedToChartArea.TransformPoint({0, 0}),
            normalizedToChartArea.TransformPoint({0, 1}) };

        wxPoint2DDouble rightHLinePoints[] = {
            normalizedToChartArea.TransformPoint({1, 0}),
            normalizedToChartArea.TransformPoint({1, 1}) };

        gc->StrokeLines(2, leftHLinePoints);
        gc->StrokeLines(2, rightHLinePoints);

        wxPoint2DDouble* pointArray = new wxPoint2DDouble[value.size()];
        wxPoint2DDouble* pointArrayY = new wxPoint2DDouble[value.size()];

        wxAffineMatrix2D valueToNormalized = normalizedToValue;
        valueToNormalized.Invert();
        wxAffineMatrix2D valueToChartArea = normalizedToChartArea;
        valueToChartArea.Concat(valueToNormalized);

        for (int i = 0; i < value.size(); i++)
        {
            pointArray[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), value[i] });
            pointArrayY[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), value[i] });

            dc.DrawCircle(wxPoint(pointArray[i].m_x, pointArray[i].m_y), 5);

            dc.SetBrush(*(new wxBrush(graph->getColour())));
            dc.DrawText(std::to_string(value[i]), wxPoint(pointArray[i].m_x - 30, pointArray[i].m_y - 20));
        }

        gc->SetPen(wxPen(graph->getColour(), 3));
        gc->StrokeLines(value.size(), pointArray);


        delete[] pointArray;
        delete gc;
}

void GraphBuilderDCPanel::DrawGraphDotted(Graph* graph)
{
     //Дублирующийся код, полная версия приведена выше
}

void GraphBuilderDCPanel::DrawGraphColumn(Graph* graph)
{
   //Дублирующийся код, полная версия приведена выше
}
```
Рассмотрим по-блочно данный кусок кода и разберем недостатки:
1. Данный код проверяет, существует ли график в контейнере. Если да, то... и тут проблема, что не ясно, что обозначает exists = 1. Удаляем ли мы график, или пропускаем далее. Или exists может равняться другим значениям, из-за чего появляется множество дизайнов.
```cpp
 int exists = 0;
    std::vector<Graph*>::iterator it = graphs.begin();
    for (; it != graphs.end(); ++it)
    {
        if (graph->compare(*it))
        {
            *it = graph;
            exists = 1;
            break;
        }
    }
```
2. В следующем коде имеется проблема else, который отвечает за дефолтную отрисвоку. Вопрос в том, а какая может быть дефолтная отрисовка? Тип графика может быть любым, из-за чего непонятно какому дизайну он следует (в одной сфере, могут использоваться линейные графики по дефолту, в другой -- точечные и так далее).
```cpp
  for (auto& graph : graphs)
    {
        if (graph->getType() == "Линии")
        {
            DrawGraphLine(graph);
        }
        else if (graph->getType() == "Столбцы")
        {
            DrawGraphColumn(graph);
        }
        else {
            DrawGraphDotted(graph);
        }
    }
```

3. Метод DrawGraphLine и ему подобные имеют множество проблем. В нем имеется множество проблем: 
   а. Наличие проверки на размер списка, чтобы не выполнять работу в никуда и не нагружать сервер
   б. Наличие константных литералов, которые могут подразумевать что-угодно под собой
   в. Наличие повторяющегося кода в других методах, которые нагружают сервер, а также сводят с толку.
   г. При потребности добавить тип графика или убрать, придется удалять методы из класса, которые могут вызываться в коде, и на которые могут быть завязаны объекты извне.
   
   
Перепишем код, чтобы он полностью соответствовал дизайну. 
Подумаем о дизайне логически (задаем вопросы "что делает"). У нас имеются сущность "графики", которые могут отличаться друг от друга, но имеют единый интерфейс. 
Графики располагаются на некой оси координат. На одной оси координат, могут отражаться разные типы графиков. В будущем, может возникнуть ситуация добавления/удаления графика.

Думая о программе так, у нас вырисовывается следующий, на первый взгляд, дизайн:
1. Создадим класс GraphToDraw, от которого будет наследовать разные типы графиков. Данные графики, как вариант, будут создаваться фабрикой.
2. Создадим класс GraphBuilder, который будет хранить графики для отрисовки. 

Теперь рассмотрим подробнее класс GraphToDraw:
1. Все математические вычисления можно вынести в отдельный модуль и создать в декларативной модели, то есть
   а. Dataflow переменные, которые не изменяются после инициализации
   б. Процедурная абстракция
2. Вместо константных литералов использовать определенные константы.
3. Элементы Fonts вынести в отдельный файл

Попытка реализовать код, который соответствует только данному дизайну:

Вынес математические функции в отдельный файл с определенные dataflow переменными
Math.cpp
```cpp
#include <tuple>
#include <cmath>

constexpr int maxSegments = 6;
constexpr double rangeMults[] = { 0.2, 0.25, 0.5, 1.0, 2.0, 2.5, 5.0 };

std::tuple<int, double, double> calculateChartSegmentCountAndRange(double origLow, double origHigh)
{
    double magnitude = std::floor(std::log10(origHigh - origLow));

    for (auto r : rangeMults)
    {
        double stepSize = r * std::pow(10.0, magnitude);
        double low = std::floor(origLow / stepSize) * stepSize;
        double high = std::ceil(origHigh / stepSize) * stepSize;

        int segments = round((high - low) / stepSize);

        if (segments <= maxSegments)
            return std::make_tuple(segments, low, high);
    }

    // return some defaults in case rangeMults and maxSegments are mismatched
    return std::make_tuple(10, origLow, origHigh);
}

const float divideMarginXby = 8.0;
double MarginX(double width, double height)
{
    return width * height / divideMarginXby;
}

...
```

Создаем иерархию графиков:
```cpp
class GraphToDraw
{
protected:
    wxAffineMatrix2D valueToChartArea;
    ...
public:
	virtual void Draw() = 0;
    void Init()
    {
       /*
       * Устанавливаем значения для внутренних полей класса графика
        */
    }
};

class DottedGraphToDraw : public GraphToDraw
{
	virtual void Draw(wxClientDC* dc)
	{
        for (int i = 0; i < value.size(); i++)
        {
            pointArray[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), value[i] });
            pointArrayY[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), value[i] });

            dc.DrawCircle(wxPoint(pointArray[i].m_x, pointArray[i].m_y), 5);

            dc.SetBrush(*(new wxBrush(graph->getColour())));
            dc.DrawText(std::to_string(value[i]), wxPoint(pointArray[i].m_x - 30, pointArray[i].m_y - 20));
        }
	}
};

class ColumnGraphToDraw : public GraphToDraw
{
    virtual void Draw()
    {
        /*
        * Своя реализация
        */
    };
};

class LineGraphToDraw : public GraphToDraw
{
    virtual void Draw()
    {
        /*
        * Своя реализация
        */
    };
};
```

Класс оси координат:
```cpp
class CoordinateAxes
{
public:
	void Draw()
	{
        int segmentCount;
        double rangeLow;
        double rangeHigh;
        std::tie(segmentCount, rangeLow, rangeHigh) = calculateChartSegmentCountAndRange(lowValue, highValue);

        double yValueSpan = rangeHigh - rangeLow;
        lowValue = rangeLow;
        highValue = rangeHigh;

        double yLinesCount = segmentCount + 1;

        wxAffineMatrix2D normalizedToValue{};
        normalizedToValue.Translate(0, highValue);
        normalizedToValue.Scale(1, -1);
        normalizedToValue.Scale(static_cast<double>(value.size() - 1), yValueSpan);

        gc->SetPen(wxPen(wxColor(128, 128, 128)));

        for (int i = 0; i < yLinesCount; i++)
        {
            double normalizedLineY = static_cast<double>(i) / (yLinesCount - 1);

            auto lineStartPoint = normalizedToChartArea.TransformPoint({ 0, normalizedLineY });
            auto lineEndPoint = normalizedToChartArea.TransformPoint({ 1, normalizedLineY });

            wxPoint2DDouble linePoints[] = { lineStartPoint, lineEndPoint };
            gc->StrokeLines(2, linePoints);

            double valueAtLineY = normalizedToValue.TransformPoint({ 0, normalizedLineY }).m_y;

            auto text = wxString::Format("%.2f", valueAtLineY);
            text = wxControl::Ellipsize(text, dc, wxELLIPSIZE_MIDDLE, chartArea.GetLeft() - labelsToChartAreaMargin);

            double tw, th;
            gc->GetTextExtent(text, &tw, &th);
            gc->DrawText(text, chartArea.GetLeft() - labelsToChartAreaMargin - tw, lineStartPoint.m_y - th / 2.0);
        }
	}
};
```

И метод Paint для отрисовки графиков пользователю:
```cpp
void GraphBuilderDCPanel::Paint(GraphToDraw* graph)
{
    checkForDuplicates(graph);
    wxClientDC dc(this);
    dc.Clear();
        
    coordAxes->Draw(dc);
    for (auto& graph : graphs)
        graph->Draw(dc);
}
```

Что получилось в итоге:
1. При переносе математических чистых функций в декларативный стиль позволило их легко тестировать.
2. Код, по возможности, стал соответствовать меньшему числу дизайнов. Математические функции строго отражают определенный дизайн (матрицы, точки в пространстве и т.д). Иерархия графиков и коордианата оси также отражают единый дизайн отрисовки (отрисовываются по определенным законам).

На переработку этого кода, чтобы он соответствовал дизайну ушло около 3 дней. Основная проблема заключалась в сильной зависимости от других классов, большого количества жестко закодированных значений, большое количество полей класса, костылей и прочего. Честно говоря, старый код мне так и не удалось преобразовать к рабочему виду, (например, при изменении модуля графиков, потребовалось менять модули, которые эти графики создают, затем модули, которые зависимы от модулей, которые создают графики и так далее, то есть у меня вышло все очень неавтономно). Плюс математические функции, которые потребовались для отрисовки были размазаны не только по классу, но и по плохо спроектированному модулю. 
По итогу, я ощутил "стоимость" поддержки существующей отвратительной архитектуры.

---------------------------2------------
Следующий пример более удачный:

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

    private array $rows;
    private array $primary_key;
    private array $unique_key;
    private array $schema;

    private int $insert_status;
    private int $search_status;


    //Пред-условия: Передано название отношения
    //Пост-условия:
    public function __construct(string $title, array $schema)
    {
        $this->rows = array();
        $this->primary_key = array();
        $this->unique_key = array();

        $this->title = $title;
        $this->schema = $schema;

        $this->search_status = Relation::INSERT_STATUS_NIL;
        $this->insert_status = Relation::INSERT_STATUS_NIL;

    }

    public function iterator(): RelationIterator
    {
        return $this->createIterator();
    }

    //Пред-условия: Передан объект типа $row
    //Пост-условия:

    public function search(int $index, string $needle)
    {
        foreach ($this->rows as $row) {
            if ($row->contains_by_index($index, $needle)) {
                $this->search_status = Relation::SEARCH_STATUS_OK;
                return $row->Id();
            }
        }
        $this->search_status = Relation::SEARCH_STATUS_NOTFOUND;
        return -1;
    }

    //Пред-условия:
    //Пост-условия:

    public function search_pk(array $fk_columns): int
    {
        $fk_row = new Row(-1);
        foreach ($fk_columns as $fk_column)
            $fk_row->append($fk_column);

        foreach ($this->rows as $row) {
            $tmpRow = ($row->sub_row($this->primary_key));

            if ($tmpRow->equals($fk_row))
                return $row->Id();
        }

        $this->search_status = Relation::SEARCH_STATUS_NOTFOUND;
        return -1;
    }

    //Пред-условия:
    //Пост-условия:

    public function get_insert_status(): int
    {
        return $this->insert_status;
    }

    //Пред-условия:
    //Пост-условия: возвращает код insert метода

    public function get_search_status(): int
    {
        return $this->search_status;
    }



    //Пред-условия:
    //Пост-условия:

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

    public function union(Relation $anotherRelation)
    {
        $result_relation = new Relation($this->title, $this->schema);
        foreach ($this->rows as $row) {
            $row->set_id($result_relation->size() + 1);
            $result_relation->insert($row);
        }


        foreach ($anotherRelation->rows as $row) {
            $row->set_id($result_relation->size() + 1);
            $result_relation->insert($row);
        }

        return $result_relation;
    }

    public function erase(int $byValue, int $at)
    {
        foreach ($this->rows as $id => $row)
        {
            if($row->at($at)->getValue() == $byValue)
                unset($this->rows[$id]);
        }

    }

    public function size(): int
    {
        return count($this->rows);
    }

    /**
     * @throws InvalidRowSchemaCountException
     */
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

    public function search_row_by_index(int $index, array $primary_key): Row
    {
        foreach ($this->rows as $row) {
            if ($row->Id() == $index) {
                if($primary_key == [])
                    return $row;
                $resultRow = new Row($row->Id());
                return $row->sub_row($primary_key);
            }
        }
        return new Row(-1);
    }

    public function array_for_export(bool $with_id)
    {
        $export_array = array();
        foreach ($this->rows as $row) {
            $export_array[] = $row->to_array($with_id);
        }
        return $export_array;
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
        if (count($this->schema) != $row->size())
            throw new InvalidRowSchemaCountException("Количество значений в строке не совпадает со схемой отношения!");

        if (!$row->fist_the_schema($this->schema))
            throw new InvalidRowSchemaException("Схема строки не совпадает со схемой отношения!");
    }

    private function createIterator(): RelationIterator
    {
        return new class($this->rows) implements RelationIterator
        {
            private $data;
            private int $currentIndex;

            public function __construct(&$dataToIterate)
            {
                $this->data = $dataToIterate;
                if(count($this->data) == 0)
                    $this->currentIndex = $this->end();
                $this->currentIndex = 0;
            }

            public function begin()
            {
                // TODO: Implement begin() method.
                if(count($this->data) == 0)
                    return $this->end();
                $this->currentIndex = 0;
                return $this->data[$this->currentIndex];
            }

            public function next()
            {
                if(count($this->data) == $this->currentIndex+1)
                    return $this->end();
                return $this->data[++$this->currentIndex];
            }

            public function end()
            {
                return -1;
            }
        };
    }

}

```
