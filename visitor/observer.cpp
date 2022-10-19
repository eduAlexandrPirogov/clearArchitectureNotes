#include <memory>
#include <string>
#include <list>
#include <iostream>
#include <algorithm>
#include <numeric>

class WeatherWidget
{
    public:
        virtual void update(float temperature) = 0;
};

class ForecastWidget : public WeatherWidget
{
    public:
        virtual void update(float temperature);
};

class StatisticWidget : public WeatherWidget
{
    std::list<float> temperatures;
    public:
        virtual void update(float temperature); 
};

class DisplayWidget : public WeatherWidget
{
    public:
        virtual void update(float temperature); 
};

class Observable
{
public:
    virtual void notify(float temperature) = 0;

};

class WidgetVisitor
{
    public:
    virtual void visit(ForecastWidget& widget);
    virtual void visit(DisplayWidget& widget);
    virtual void visit(StatisticWidget& widget);
};

class WeatherWidgetsObs : public Observable
{
    std::list<std::shared_ptr<WeatherWidget>> widgets;
    public:
        void notify(float temperature)
        {
            for(auto& widget : widgets)
            {
                widget->update(temperature);
            }
        }

        void addWidget(std::shared_ptr<WeatherWidget>&& widget)
        {
            widgets.emplace_back(std::move(widget));
        }
};

void ForecastWidget::update(float temperature)
{
    std::cout << "Forecast for tomorow: " << temperature + 1.5 << '\n';

}

void StatisticWidget::update(float temperature)
{
    temperatures.push_back(temperature);
    float sum = std::accumulate(temperatures.begin(), temperatures.end(), 0);
    size_t count = temperatures.size();
    std::cout << "Avg temperatre for the last " <<  count << " days is " << sum/count*1.0 << '\n';
}

void DisplayWidget::update(float temperature)
{
    std::cout << "Just displaying temperature: " << temperature << '\n';
}


int main()
{
    std::shared_ptr<WeatherWidgetsObs> obs = std::make_shared<WeatherWidgetsObs>();
    std::shared_ptr<WeatherWidget> displayWidget = std::make_shared<DisplayWidget>();
    std::shared_ptr<WeatherWidget> forecastWidget = std::make_shared<ForecastWidget>();
    std::shared_ptr<WeatherWidget> statisticWidget = std::make_shared<StatisticWidget>();


    obs->addWidget(std::move(displayWidget));
    obs->addWidget(std::move(forecastWidget));
    obs->addWidget(std::move(statisticWidget));

    obs->notify(14.0f);
    obs->notify(13.2f);
    obs->notify(16.3f);
    return 0;
}
