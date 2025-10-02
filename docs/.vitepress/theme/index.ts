import DefaultTheme from "vitepress/theme";
import Layout from "./Layout.vue";
import HistogramViewer from "./components/HistogramViewer.vue";
import JsonHistogram from "./components/JsonHistogram.vue";
import AcceptanceViewer from "./components/AcceptanceViewer.vue";
import AcceptancePlot from "./components/AcceptancePlot.vue";

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('HistogramViewer', HistogramViewer);
    app.component('JsonHistogram', JsonHistogram);
    app.component('AcceptanceViewer', AcceptanceViewer);
    app.component('AcceptancePlot', AcceptancePlot);
  }
};