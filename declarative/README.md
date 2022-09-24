
```cpp
void GraphBuilderDCPanel::DrawGraphLine(Graph* graph)
{
    wxClientDC dc(this);
    wxGraphicsContext* gc = wxGraphicsContext::Create(dc);
    if (gc && graphs.size() > 0)
    {
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
    wxClientDC dc(this);
    //dc.Clear();
    wxGraphicsContext* gc = wxGraphicsContext::Create(dc);

    wxFont titleFont = wxFont(wxNORMAL_FONT->GetPointSize() * 2.0,
        wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD);

    gc->SetFont(titleFont, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);
        auto values = graph->xValues();

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
        normalizedToValue.Scale(static_cast<double>(values.size() - 1), yValueSpan);

        gc->SetPen(wxPen(wxColor(128, 128, 128)));
        gc->SetFont(*wxNORMAL_FONT, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);

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

        wxPoint2DDouble* pointArray = new wxPoint2DDouble[values.size()];
        wxPoint2DDouble* pointArrayY = new wxPoint2DDouble[values.size()];

        wxAffineMatrix2D valueToNormalized = normalizedToValue;
        valueToNormalized.Invert();
        wxAffineMatrix2D valueToChartArea = normalizedToChartArea;
        valueToChartArea.Concat(valueToNormalized);

        dc.SetBrush(*(new wxBrush(graph->getColour())));
        for (int i = 0; i < values.size(); i++)
        {
            pointArray[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), values[i] });
            pointArrayY[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), values[i] });
            
            dc.DrawCircle(wxPoint(pointArray[i].m_x, pointArray[i].m_y), 5);
            dc.DrawText(std::to_string(values[i]), wxPoint(pointArray[i].m_x-30, pointArray[i].m_y - 20));

        }

        gc->SetPen(wxPen(wxSystemSettings::GetAppearance().IsDark() ? *wxCYAN : *wxBLUE, 3));

        delete[] pointArray;
    delete gc;
}

void GraphBuilderDCPanel::DrawGraphDotted(Graph* graph)
{
    wxClientDC dc(this);
    //dc.Clear();
    wxGraphicsContext* gc = wxGraphicsContext::Create(dc);

    wxFont titleFont = wxFont(wxNORMAL_FONT->GetPointSize() * 2.0,
        wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD);

    gc->SetFont(titleFont, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);
    auto values = graph->xValues();

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
    normalizedToValue.Scale(static_cast<double>(values.size() - 1), yValueSpan);

    gc->SetPen(wxPen(wxColor(128, 128, 128)));
    gc->SetFont(*wxNORMAL_FONT, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);

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

    wxPoint2DDouble* pointArray = new wxPoint2DDouble[values.size()];
    wxPoint2DDouble* pointArrayY = new wxPoint2DDouble[values.size()];

    wxAffineMatrix2D valueToNormalized = normalizedToValue;
    valueToNormalized.Invert();
    wxAffineMatrix2D valueToChartArea = normalizedToChartArea;
    valueToChartArea.Concat(valueToNormalized);

    dc.SetBrush(*(new wxBrush(graph->getColour())));
    for (int i = 0; i < values.size(); i++)
    {
        pointArray[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), values[i] });
        pointArrayY[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), values[i] });

        dc.DrawCircle(wxPoint(pointArray[i].m_x, pointArray[i].m_y), 5);
        dc.DrawText(std::to_string(values[i]), wxPoint(pointArray[i].m_x - 30, pointArray[i].m_y - 20));

    }

    gc->SetPen(wxPen(wxSystemSettings::GetAppearance().IsDark() ? *wxCYAN : *wxBLUE, 3));

    delete[] pointArray;
    delete gc;
}

void GraphBuilderDCPanel::DrawGraphColumn(Graph* graph)
{
    wxClientDC dc(this);
   // dc.Clear();
    wxGraphicsContext* gc = wxGraphicsContext::Create(dc);
    wxFont titleFont = wxFont(wxNORMAL_FONT->GetPointSize() * 2.0,
        wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD);

    gc->SetFont(titleFont, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);
        auto values = graph->xValues();

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

        double lowValue = *std::min_element(values.begin(), values.end());
        double highValue = *std::max_element(values.begin(), values.end());

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
        normalizedToValue.Scale(static_cast<double>(values.size() - 1), yValueSpan);

        gc->SetPen(wxPen(wxColor(128, 128, 128)));
        gc->SetFont(*wxNORMAL_FONT, wxSystemSettings::GetAppearance().IsDark() ? *wxWHITE : *wxBLACK);

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

        wxPoint2DDouble* pointArray = new wxPoint2DDouble[values.size()];
        wxPoint2DDouble* pointArrayY = new wxPoint2DDouble[values.size()];

        wxAffineMatrix2D valueToNormalized = normalizedToValue;
        valueToNormalized.Invert();
        wxAffineMatrix2D valueToChartArea = normalizedToChartArea;
        valueToChartArea.Concat(valueToNormalized);

        for (int i = 0; i < values.size(); i++)
        {
            pointArray[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), values[i] });
            pointArrayY[i] = valueToChartArea.TransformPoint({ static_cast<double>(i), lowValue });

            dc.SetBrush(*(new wxBrush(graph->getColour())));
            dc.DrawCircle(wxPoint(pointArray[i].m_x, pointArray[i].m_y), 5);
            dc.SetBrush(*wxBLUE_BRUSH);
            dc.DrawLine(wxPoint(pointArray[i].m_x, pointArray[i].m_y), wxPoint(pointArrayY[i].m_x, pointArrayY[i].m_y));
            dc.DrawText(std::to_string(values[i]), wxPoint(pointArray[i].m_x - 30, pointArray[i].m_y - 20));

        }

        gc->SetPen(wxPen(wxSystemSettings::GetAppearance().IsDark() ? *wxCYAN : *wxBLUE, 3));

        delete[] pointArray;
}
```
