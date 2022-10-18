#Observer to Visitor

Имеется следующий код:

```cpp
class ObservableWeather 
{
    public:
        virtual void update() = 0;
        virtual void setMetrics(float newTemperature, float newWet) = 0;
};


class WeatherForeacstSimple : public ObservableWeather
{
    float temperature, wet;
public:
    void update()
    {
        temperature += 5;
        wet -= 1;
        std::cout << "Current Weather: temperature " << temperature 
        << " wet: " << wet << "\n";
    }

    void setMetrics(float newTemperature, float newWet)
    {
        temperature = newTemperature;
        wet = newWet;
    }
};

class WeatherForeacstComplex : public ObservableWeather
{
    float temperature, wet;
public:
    void update()
    {
        temperature += 5.0/64.0 + 3.3 - 5;
        wet -= 3;
        std::cout << "Current Weather: temperature " << temperature 
        << " wet: " << wet << "\n";
    }

    void setMetrics(float newTemperature, float newWet)
    {
        temperature = newTemperature;
        wet = newWet;
    }
};


class WeatherObserver
{
    public:
        virtual void add(std::shared_ptr<ObservableWeather>&& weather) = 0;
        virtual void notify() = 0; 
};

class SyzranWatherObserver : public WeatherObserver
{
    std::list<std::shared_ptr<ObservableWeather>> metrics;
    public:
        inline void add(std::shared_ptr<ObservableWeather>&& weather)
        {
            metrics.emplace_back(std::move(weather));
        }

        inline void notify()
        {
            for (auto &&metric : metrics)
                metric->update();
            
        }

        inline void sendMetrics(float temperature, float wet)
        {
            for (auto &&metric : metrics)
                metric->setMetrics(temperature, wet);
            
        }
};
```

Ситуация, когда нужно нужно модифицировать класс, но не хотим обновлять конейтнер

```cpp

```
