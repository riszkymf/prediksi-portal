import { defineStore } from 'pinia';

export const menuItems = defineStore("menuItems", {
  state: () => ({
    items: [
      {
        menuItemId: 0,
        name: "home",
        displayName: "Home",
        target: "#home",
        targetIsLink: false,
        isActive: true,
        icon: "bi bi-app",
      },
      {
        menuItemId: 1,
        name: "tambahData",
        displayName: "Tambah Data",
        target: "#tambahData",
        targetIsLink: false,
        isActive: false,
        icon: "bi bi-database-fill-add"
      },
      {
        menuItemId: 2,
        name: "prosesData",
        displayName: "Proses data",
        target: "#prosesData",
        targetIsLink: false,
        isActive: false,
        icon: "bi bi-wrench"
      },
      {
        menuItemId: 3,
        name: "pengujianData",
        displayName: "Pengujian Data",
        target: "#pengujianData",
        targetIsLink: false,
        isActive: false,
        icon: "bi bi-hourglass-bottom"
      },
      {
        menuItemId: 4,
        name: "evaluasiData",
        displayName: "Evaluasi Data",
        target: "#evaluasiData",
        targetIsLink: false,
        isActive: false,
        icon: "bi bi-graph-up"
      },
    ],
  }),
  actions: {
    activate(menuItemId: number) {
      this.items = this.items.map((el) => {
        el.isActive = el.menuItemId === menuItemId;
        return el;
      });
    },
  },
  getters: {
    getItems: (state) => state.items,
  },
});
