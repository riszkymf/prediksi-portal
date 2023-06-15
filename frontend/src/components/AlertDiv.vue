<template>
  <div
    class="alert"
    :class="[showMessage ? 'show' : 'hide', getClass(type)]"
    role="alert"
  >
    {{ message }}
  </div>
</template>

<script lang="ts">
export default {
  props: {
    message: String,
    type: String,
  },
  data() {
    return {
      active: false,
    };
  },
  methods: {
    deactivateAlert() {
      this.active = false;
    },
    getClass(alertType: string | undefined): string {
      let alertClass = "alert-default";
      switch (alertType) {
        case "success":
          alertClass = "alert-success";
          break;
        case "info":
          alertClass = "alert-info";
          break;
        case "error":
          alertClass = "alert-danger";
          break;
        case "warning":
          alertClass = "alert-warning";
          break;
      }
      this.active = true;
      return alertClass;
    },
  },
  computed: {
    showMessage() {
      return Boolean(this.message && this.active);
    },
  },
};
</script>
