<script setup>
import DefaultTheme from "vitepress/theme";
import { onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vitepress";
import mediumZoom from "medium-zoom";

const { Layout } = DefaultTheme;
const router = useRouter();

let zoom = null;
let observer = null;

const attachZoomable = () => {
  if (!zoom) return;
  const nodes = document.querySelectorAll("[data-zoomable]");
  if (nodes.length) zoom.attach(nodes);
};

onMounted(() => {
  zoom = mediumZoom({ background: "transparent" });
  attachZoomable();

  observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (!(node instanceof Element)) continue;
        if (node.matches?.("[data-zoomable]")) zoom.attach(node);
        const nested = node.querySelectorAll?.("[data-zoomable]");
        if (nested && nested.length) zoom.attach(nested);
      }
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
});

onBeforeUnmount(() => {
  observer?.disconnect();
  zoom?.detach();
});

router.onAfterRouteChanged = attachZoomable;
router.onAfterRouteChange = attachZoomable;
</script>

<template>
  <Layout />
</template>

<style>
.medium-zoom-overlay {
  backdrop-filter: blur(5rem);
}

.medium-zoom-overlay,
.medium-zoom-image--opened {
  z-index: 999;
}
</style>