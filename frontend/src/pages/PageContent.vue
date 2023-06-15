<template>
  <div class="content" id="pageContent" :class="{ expand: isSidebarOpen() }">
    <div class="row justify-content-evenly">
      <component :is="getPageContent()"></component>
    </div>
  </div>
</template>

<style lang="scss">
@import "../assets/css/contentPage.scss";
</style>

<script lang="ts">
import HomeView from "@/views/HomeView.vue";
import TambahData from "@/views/TambahDataView.vue";
import ProsesDataView from "@/views/ProsesDataView.vue";
import EvaluasiView from "@/views/EvaluasiView.vue";
import UjiDataView from "@/views/UjiDataView.vue";
import { TOGGLER_CONTENT } from "@/stores/display";
import { TOGGLER_SIDEBAR } from "@/stores/display";
import { menuItems } from "@/stores/menuItems";

type ComponentMap = {
  [key: string]: any;
};
const renderedTemplate: ComponentMap = {
  home: HomeView,
  tambahData: TambahData,
  prosesData: ProsesDataView,
  pengujianData: UjiDataView,
  evaluasiData: EvaluasiView,
};

export default {
  methods: {
    getPageContent() {
      const togglerContent = TOGGLER_CONTENT();
      const currentPage = togglerContent.activePage;
      let template = renderedTemplate[currentPage];
      return template;
    },
    isSidebarOpen() {
      const isSidebarActive = TOGGLER_SIDEBAR().isSidebarActive;
      return !isSidebarActive;
    },
  },
  created() {
    let urlParams = window.location.hash;
    const togglerContent = TOGGLER_CONTENT();
    const menuLists = menuItems();
    let menuId = 0;
    menuLists.items.forEach((el) => {
      if (el.target == urlParams) {
        menuId = el.menuItemId;
      }
    });
    menuLists.activate(menuId);
    togglerContent.getPage(urlParams);
  },
};
</script>
