<template>
  <div class="col-md-10 mt-5 py-3">
    <h3>Pengujian Data</h3>
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
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#trainDataResult"
        aria-expanded="false"
        aria-controls="trainDataResult"
      >
        Hasil Data Latih
      </button>
      <button
        class="btn btn-outline-secondary"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#testDataResult"
        aria-expanded="false"
        aria-controls="testDataResult"
      >
        Hasil Data Uji
      </button>
    </div>
  </div>
  <div
    class="col-md-10 mt-5"
    :class="{ hide: !tableExist('train') }"
    id="trainDataResult"
  >
    <div class="table-responsive">
      <span class="title">
        <h5>Data Uji</h5>
      </span>
      <span class="title">
        <h5>Hasil Data Uji</h5>
      </span>
      <EasyDataTable
        :headers="train.table.headers"
        :items="train.table.content"
        :table-class-name="'mb-5'"
        show-index
      />
      <span class="title mt-2">
        <h5>Hasil Prediksi Data Uji</h5>
      </span>
      <div :v-if="state == 'loaded'" class="card" style="width: 30rem">
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            Yang terkena kanker paru-paru berjumlah: {{ train.predictionResult.yes }}
          </li>
          <li class="list-group-item">
            Yang tidak terkena kanker paru-paru berjumlah: {{ train.predictionResult.no }}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="w-100"></div>
  <div class="col-md-10 mt-5" :class="{ hide: !tableExist('test') }" id="testDataResult">
    <div class="table-responsive">
      <span class="title">
        <h5>Data Latih</h5>
      </span>
      <span class="title">
        <h5>Hasil Data Latih</h5>
      </span>
      <EasyDataTable
        :headers="test.table.headers"
        :items="test.table.content"
        :table-class-name="'mb-5'"
        show-index
      />
      <span class="title mt-2">
        <h5>Hasil Prediksi Data Latih</h5>
      </span>
      <div :v-if="state == 'loaded'" class="card" style="width: 30rem">
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            Yang terkena kanker paru-paru berjumlah: {{ test.predictionResult.yes }}
          </li>
          <li class="list-group-item">
            Yang tidak terkena kanker paru-paru berjumlah: {{ test.predictionResult.no }}
          </li>
        </ul>
      </div>
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
import AlertDiv from "@/components/AlertDiv.vue";
import { datasetStore } from "@/stores/datasets";
import type { PredictionCount, TrainResult } from "@/stores/datasets";

const parseDataSetToTable = (datasets: Array<object>) => {
  const rowAwal = datasets[0];
  const table: TableConfig = {
    headers: [],
    content: [],
  };
  table.headers = Object.keys(rowAwal).map((el) => {
    return {
      text: el,
      value: el,
    };
  });
  table.content = datasets;
  return table;
};

type TableConfig = {
  headers: Header[];
  content: Item[];
};

export default {
  components: {
    AlertDiv,
  },
  data() {
    const datasetState = datasetStore();
    const testTable: TableConfig = { headers: [], content: [] };
    const testPred: PredictionCount = { yes: 0, no: 0 };
    const trainTable: TableConfig = { headers: [], content: [] };
    const trainPred: PredictionCount = { yes: 0, no: 0 };

    const testData = {
      table: testTable,
      predictionResult: testPred,
    };
    const trainData = {
      table: trainTable,
      predictionResult: trainPred,
    };
    return {
      parsed: false,
      datasetState: datasetState,
      test: testData,
      train: trainData,
      alert: {
        message: "",
        type: "success",
      },
      state: "preparing",
    };
  },
  methods: {
    tableExist(tableName: string): Boolean {
      if (tableName == "train") {
        return this.train.table.content.length > 0;
      }
      if (tableName == "test") {
        return this.test.table.content.length > 0;
      }
      return false;
    },
    setupData(result: TrainResult) {
      this.test.table = parseDataSetToTable(result.test.prediction_result);
      this.test.predictionResult = result.test.prediction_count;
      this.train.table = parseDataSetToTable(result.train.prediction_result);
      this.train.predictionResult = result.train.prediction_count;
      this.state = "loaded";
    },
    fetchData() {
      this.datasetState.getResult().then((result) => {
        if (result != undefined) {
          this.setupData(result);
        }
      });
    },
  },
  mounted() {
    if (!this.datasetState.resultExists()) {
      this.fetchData();
    }
    if (this.datasetState.resultExists()) {
      this.setupData(this.datasetState.trainResult as TrainResult);
    }
  },
};
</script>
