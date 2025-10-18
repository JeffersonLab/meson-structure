import DefaultTheme from "vitepress/theme";
import Layout from "./Layout.vue";
import HistogramViewer from "./components/HistogramViewer.vue";
import JsonHistogram from "./components/JsonHistogram.vue";
import BeamEnergyCompareViewer from "./components/BeamEnergyCompareViewer.vue";
import BeamEnergyComparePlot from "./components/BeamEnergyComparePlot.vue";

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('HistogramViewer', HistogramViewer);
    app.component('JsonHistogram', JsonHistogram);
    app.component('BeamEnergyCompareViewer', BeamEnergyCompareViewer);
    app.component('BeamEnergyComparePlot', BeamEnergyComparePlot);
  }
};