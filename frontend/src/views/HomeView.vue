<template>
  <div class="col-lg-10 jumbotron jumbotron-fluid">
    <div class="container">
      <h1>
        {{ content }}
      </h1>
    </div>
  </div>
</template>

<style lang="scss">
div.jumbotron {
  padding: calc(1.5rem + 1.5vw) 0px;
  p {
    padding-top: 5px;
    margin-bottom: 0rem;
  }
}
</style>

<script lang="ts">
export default {
  data() {
    const content = "Prediksi Kanker Paru Paru";
    return {
      content: content,
    };
  },
};
</script>
