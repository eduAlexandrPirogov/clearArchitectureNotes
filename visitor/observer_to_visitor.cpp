#include <memory>
#include <string>
#include <list>
#include <iostream>
#include <algorithm>
#include <numeric>


class WeatherWidget
{
    public:
        virtual void accept(class WidgetVisitor& visitor, float metric) = 0;
};

class ForecastWidget : public WeatherWidget
{
    public:
        void accept(WidgetVisitor& visitor, float metric);
        void forecast(float metric);
        void forecastWet(float metric);
};

class StatisticWidget : public WeatherWidget
{
    std::list<float> temperatures;
    std::list<float> wets;
    public:
        void accept(WidgetVisitor& visitor, float metric);
        void calculate(float metric);
        void calculateWet(float metric);
};

class DisplayWidget : public WeatherWidget
{
    public:
        void accept(WidgetVisitor& visitor, float metric);
        void show(float metric);
        void displayWet(float metric);
};


class WidgetVisitor
{
    public:
    virtual void visit(ForecastWidget& widget, float metric)=0;
    virtual void visit(DisplayWidget& widget, float metric)=0;
    virtual void visit(StatisticWidget& widget, float metric)=0;
};

class WeatherVisitor : public WidgetVisitor
{
    public:
    void visit(ForecastWidget& widget, float metric);
    void visit(DisplayWidget& widget, float metric);
    void visit(StatisticWidget& widget, float metric);
};

class WetWeatherVisitor : public WidgetVisitor
{
public:
    void visit(ForecastWidget& widget, float metric);
    void visit(DisplayWidget& widget, float metric);
    void visit(StatisticWidget& widget, float metric);
};

class Observable
{
public:
    virtual void notify(WidgetVisitor& visitor, float metric) = 0;
};

class WeatherWidgetsObs : public Observable
{
    std::list<std::shared_ptr<WeatherWidget>> widgets;
    public:
        void notify(WidgetVisitor& visitor, float metric)
        {
            for(auto& widget : widgets)
                widget->accept(visitor, metric);
        }

        void addWidget(std::shared_ptr<WeatherWidget>&& widget)
        {
            widgets.emplace_back(std::move(widget));
        }
};

void WeatherVisitor::visit(ForecastWidget& widget, float metric)
{
    widget.forecast(metric);
}

void WeatherVisitor::visit(DisplayWidget& widget, float metric)
{
    widget.show(metric);
}

void WeatherVisitor::visit(StatisticWidget& widget, float metric)
{
    widget.calculate(metric);
}

void WetWeatherVisitor::visit(StatisticWidget& widget, float metric)
{
    widget.calculateWet(metric);
}

void WetWeatherVisitor::visit(ForecastWidget& widget, float metric)
{
    widget.forecastWet(metric);
}

void WetWeatherVisitor::visit(DisplayWidget& widget, float metric)
{
    widget.displayWet(metric);
}

void ForecastWidget::accept(WidgetVisitor& visitor, float metric)
{
    visitor.visit(*this, metric);

}
void ForecastWidget::forecast(float metric)
{
    std::cout << "Forecast for tomorow: " << metric + 1.5 << '\n';
}

void StatisticWidget::accept(WidgetVisitor& visitor, float metric)
{
    visitor.visit(*this, metric);
};


void DisplayWidget::displayWet(float metric)
{
    std::cout << "Just displaying wet: " << metric << '\n';
};


void ForecastWidget::forecastWet(float metric)
{
    std::cout << "Forecast for tomorow wet: " << metric - 1.5 << '\n';
}; 

void StatisticWidget::calculate(float metric)
{
    temperatures.push_back(metric);
    float sum = std::accumulate(temperatures.begin(), temperatures.end(), 0);
    size_t count = temperatures.size();
    std::cout << "Avg temperature for the last " <<  count << " days is " << sum/count*1.0 << '\n';
};


void StatisticWidget::calculateWet(float metric)
{
    wets.push_back(metric);
    float sum = std::accumulate(wets.begin(), wets.end(), 0);
    size_t count = wets.size();
    std::cout << "Avg Wet for the last " <<  count << " days is " << sum/count*1.0 << '\n';
};


void DisplayWidget::accept(WidgetVisitor& visitor, float metric)
{
    visitor.visit(*this, metric);
}

void DisplayWidget::show(float metric)
{
    std::cout << "Just displaying temperature: " << metric << '\n';
};


int main()
{
    std::shared_ptr<WeatherWidgetsObs> obs = std::make_shared<WeatherWidgetsObs>();
    std::shared_ptr<WeatherWidget> displayWidget = std::make_shared<DisplayWidget>();
    std::shared_ptr<WeatherWidget> forecastWidget = std::make_shared<ForecastWidget>();
    std::shared_ptr<WeatherWidget> statisticWidget = std::make_shared<StatisticWidget>();


    obs->addWidget(std::move(displayWidget));
    obs->addWidget(std::move(forecastWidget));
    obs->addWidget(std::move(statisticWidget));

    std::shared_ptr<WeatherVisitor> weatherVisitor = std::make_shared<WeatherVisitor>();

    obs->notify(*(weatherVisitor.get()), 14.0f);
    obs->notify(*(weatherVisitor.get()), 13.2f);
    obs->notify(*(weatherVisitor.get()), 16.3f);

    std::cout << "\n------------------------------------------\n";

    std::shared_ptr<WetWeatherVisitor> metricVisitor = std::make_shared<WetWeatherVisitor>();

    obs->notify(*(metricVisitor.get()), 6.0f);
    obs->notify(*(metricVisitor.get()), 9.2f);
    obs->notify(*(metricVisitor.get()), 10.3f);
    return 0;
}
