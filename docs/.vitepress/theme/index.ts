import DefaultTheme from "vitepress/theme";
import Layout from "./Layout.vue";
import HistogramViewer from "./components/HistogramViewer.vue";
import JsonHistogram from "./components/JsonHistogram.vue";
import PlotCompareViewer from "./components/PlotCompareViewer.vue";
import VerticalComparePlot from "./components/VerticalComparePlot.vue";

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('HistogramViewer', HistogramViewer);
    app.component('JsonHistogram', JsonHistogram);
    app.component('PlotCompareViewer', PlotCompareViewer);
    app.component('VerticalComparePlot', VerticalComparePlot);
  }
};
