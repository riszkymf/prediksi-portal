<template>
  <div class="col-md-10 mt-5 py-3">
    <h3>Proses Data</h3>
  </div>
  <div class="w-100"></div>
  <div class="col-md-10">
    <AlertDiv :message="alert.message" :type="alert.type" />
  </div>
  <div class="w-100"></div>
  <div class="col-md-10">
    <div class="input-group mb-3">
      <button
        class="btn btn-outline-secondary"
        @click="prosesData"
        type="button"
        id="prosesData"
      >
        Proses Data
      </button>
    </div>
  </div>
  <div class="col-md-10" :class="{ hide: !parsed }">
    <div class="table-responsive">
      <span class="title">
        <h5>
          {{ datasetState.currentDataSet }}
        </h5>
      </span>
      <EasyDataTable :headers="table.headers" :items="table.content" />
    </div>
  </div>
</template>

<style lang="scss">
.hide {
  display: none !important;
}
</style>

<script lang="ts">
import type { Header, Item } from "vue3-easy-data-table";
import axios from "axios";
import AlertDiv from "@/components/AlertDiv.vue";
import { datasetStore } from "@/stores/datasets";
import type { TrainResult } from "@/stores/datasets";

export default {
  components: {
    AlertDiv,
  },
  setup() {
    const datasetState = datasetStore();
    return {
      datasetState: datasetState,
    };
  },
  data() {
    const tableHeaders: Header[] = [];
    const tableContent: Item[] = [];

    return {
      parsed: false,
      table: {
        headers: tableHeaders,
        content: tableContent,
      },
      alert: {
        message: "",
        type: "success",
      },
    };
  },
  methods: {
    getNormalizedDataset() {
      const API_HOST = import.meta.env.VUE_APP_API_HOST || "http://0.0.0.0:5334/api";
      axios
        .get(API_HOST + "/process?target=dataset:normalize")
        .then((resp) => {
          if (resp.status == 200) {
            if (resp.data.code != 200) {
              this.alert.message = resp.data.message;
              this.alert.type = "error";
            } else {
              if (resp.data.data !== null) {
                this.parseDataSetToTable(resp.data.data);
              }
            }
          }
        })
        .catch((reason) => {
          this.alert.message = reason;
          this.alert.type = "error";
        });
    },
    parseDataSetToTable(datasets: Array<object>) {
      const headers: Header[] = [];
      const rowAwal = datasets[0];
      Object.keys(rowAwal).forEach((key) => {
        headers.push({
          text: key,
          value: key,
        });
      });
      this.table.headers = headers;
      this.table.content = datasets;
      this.parsed = true;
    },

    prosesData() {
      const API_HOST = import.meta.env.VUE_APP_API_HOST || "http://0.0.0.0:5334/api";
      const payload = {
        action: "preprocess",
      };
      axios
        .post(API_HOST + "/process", JSON.stringify(payload), {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((resp) => {
          if (resp.status == 200) {
            if (resp.data.code != 200) {
              this.alert.message = resp.data.message;
              this.alert.type = "error";
            } else {
              this.alert.type = "success";
              this.alert.message = "Berhasil memproses dataset";
              this.getNormalizedDataset();
            }
          }
        })
        .catch((reason) => {
          console.log("errr");
          this.alert.message = reason;
          this.alert.type = "error";
        });
    },
  },
  mounted: function () {
    this.getNormalizedDataset();
  },
};
</script>
