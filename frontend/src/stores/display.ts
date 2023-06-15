import { defineStore } from "pinia";

export const TOGGLER_SIDEBAR = defineStore("toggleSidebar", {
  state: () => ({
    isSidebarActive: true,
  }),
  actions: {
    toggleSidebar() {
      this.isSidebarActive = !this.isSidebarActive;
    },
  },
});

export const TOGGLER_CONTENT = defineStore("toggleContent", {
  state: () => ({
    activePage: "home",
  }),
  actions: {
    getPage(contentId: string) {
      this.activePage = contentId.replace("#", "");
    },
  },
});
