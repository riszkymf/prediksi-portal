<template>
  <div class="col-md-10 mt-5 py-3">
    <h3>Evaluasi Data</h3>
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
        data-bs-target="#testDataResult"
        aria-expanded="false"
        aria-controls="testDataResult"
      >
        Data Latih
      </button>
      <button
        class="btn btn-outline-secondary"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#trainDataResult"
        aria-expanded="false"
        aria-controls="trainDataResult"
      >
        Data Uji
      </button>
    </div>
  </div>
  <div
    class="col-md-10 g-0 mt-5"
    :class="{ hide: state !== 'loaded' }"
    id="trainDataResult"
  >
    <div class="table-responsive">
      <span class="title">
        <h5>Data Uji</h5>
      </span>
      <span class="title">
        <h6>Hasil Evaluasi Data Uji</h6>
      </span>
      <TableReport :report="getEvaluation(trainResult.test.evaluation)" />
    </div>
  </div>
  <div class="w-100"></div>
  <div
    class="col-md-10 g-0 mt-5"
    :class="{ hide: state !== 'loaded' }"
    id="testDataResult"
  >
    <div class="table-responsive">
      <span class="title">
        <h5>Data Latih</h5>
      </span>
      <span class="title">
        <h6>Hasil Evaluasi Data Latih</h6>
      </span>
      <TableReport :report="getEvaluation(trainResult.train?.evaluation)" />
    </div>
  </div>

  <div class="col-md-10 g-0 mt-5" :class="{ hide: state !== 'loaded' }">
    <span class="title">
      <h5>Data Gabungan</h5>
    </span>
    <div class="table-responsive">
      <span class="title">
        <h6>Hasil Evaluasi Data Gabungan</h6>
      </span>
      <table style="width: 40%" class="table table-bordered table-striped">
        <tbody>
          <tr>
            <td>True Positive</td>
            <td>{{ trainResult.evaluation.confusion_matrix.true_positive }}</td>
          </tr>
          <tr>
            <td>False Positive</td>
            <td>{{ trainResult.evaluation.confusion_matrix.false_positive }}</td>
          </tr>
          <tr>
            <td>True Negative</td>
            <td>{{ trainResult.evaluation.confusion_matrix.true_negative }}</td>
          </tr>
          <tr>
            <td>False Negative</td>
            <td>{{ trainResult.evaluation.confusion_matrix.false_negative }}</td>
          </tr>
        </tbody>
      </table>
      <span class="title">
        <h6>Hasil Confusion Matrix</h6>
      </span>
      <TableReport :report="getEvaluation(trainResult.evaluation.report)" />
    </div>
  </div>
</template>

<style lang="scss">
.hide {
  display: none !important;
}
</style>

<script lang="ts">
import AlertDiv from "@/components/AlertDiv.vue";
import TableReport from "@/components/TableReport.vue";
import { datasetStore } from "@/stores/datasets";
import type { ReportMetric, TrainResult, EvaluationResult } from "@/stores/datasets";

export default {
  components: {
    AlertDiv,
    TableReport,
  },
  data() {
    const datasetState = datasetStore();
    const evaluation: EvaluationResult = {
      confusion_matrix: {
        true_positive: 0,
        true_negative: 0,
        false_negative: 0,
        false_positive: 0,
      },
      report: {} as ReportMetric,
    };
    let trainResult = {
      test: {},
      train: {},
      evaluation: evaluation,
    } as TrainResult;
    return {
      parsed: false,
      datasetState: datasetState,
      trainResult: trainResult,
      alert: {
        message: "",
        type: "success",
      },
      state: "preparing",
    };
  },
  methods: {
    fetchData() {
      this.datasetState.getResult().then((result) => {
        if (result !== undefined) {
          this.trainResult = result;
          this.state = "loaded";
        }
      });
    },
    getEvaluation(report: ReportMetric | undefined) {
      let result: ReportMetric = {
        yes: {},
        no: {},
        weighted_avg: {},
        macro_avg: {},
        accuracy: 0,
      };
      if (report === undefined) {
        return result;
      }
      return report;
    },
  },
  watch: {
    state() {
      this.trainResult = this.datasetState.trainResult as TrainResult;
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>
