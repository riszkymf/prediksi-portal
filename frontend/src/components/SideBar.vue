<template>
  <nav
    class="navbar d-inline-flex flex-row justify-content-left"
    :class="{ hide: !sidebarToggle.isSidebarActive }"
    id="navbarMenu"
  >
    <span class="fs-5 sidebar-title">
      <h5>Sistem Prediksi Kanker Paru-paru</h5>
    </span>
    <ul class="menuList navbar-nav">
      <a
        v-for="menuItem in menuLists.items"
        class="nav-item"
        :key="menuItem.menuItemId"
        :class="{ active: menuItem.isActive }"
        :href="menuItem.target"
        @click="switchContent(menuItem.menuItemId, menuItem.target)"
      >
        <li><i :class="[menuItem.icon]"></i>{{ menuItem.displayName }}</li>
      </a>
    </ul>
  </nav>
</template>

<style lang="scss">
@import "../assets/css/sidebar.scss";
</style>

<script lang="ts">
import { TOGGLER_SIDEBAR } from "@/stores/display";
import { menuItems } from "@/stores/menuItems";
import { TOGGLER_CONTENT } from "@/stores/display";
export default {
  data() {
    const sidebarToggle = TOGGLER_SIDEBAR();
    const menuLists = menuItems();
    return {
      sidebarToggle,
      menuLists,
    };
  },
  methods: {
    switchContent(idContent: number, idPage: string) {
      const contentToggle = TOGGLER_CONTENT();
      this.menuLists.activate(idContent);
      contentToggle.getPage(idPage);
    },
  },
};
</script>
