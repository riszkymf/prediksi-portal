<template>
  <table class="table table-bordered table-striped">
    <thead>
      <tr>
        <th scope="col"></th>
        <th scope="col">Yes</th>
        <th scope="col">No</th>
        <th scope="col">Macro Average</th>
        <th scope="col">Weighted Average</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="key in metric">
        <td>{{ key }}</td>
        <td>{{ getValue(report?.yes, key) }}</td>
        <td>{{ getValue(report?.no, key) }}</td>
        <td>{{ getValue(report?.macro_avg, key) }}</td>
        <td>{{ getValue(report?.weighted_avg, key) }}</td>
      </tr>
      <tr>
        <td colspan="4">Akurasi</td>
        <td>
          {{ report?.accuracy }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
<style lang="scss">
thead {
  th {
    font-size: 1vw;
  }
}
</style>

<script lang="ts">
import type { ReportMetric } from "@/stores/datasets";
import type { PropType } from "vue";

export default {
  props: {
    report: Object as PropType<ReportMetric>,
    akurasi: Number,
  },
  data() {
    let metric: string[] = [];

    return {
      active: false,
      metric: metric,
    };
  },
  methods: {
    getValue(o: { [key: string]: number } | undefined, key: string) {
      if (o === undefined) {
        return "";
      }
      let value = o[key];
      if (value % 1 != 0) {
        return value.toFixed(4);
      }
      return value;
    },
  },
  watch: {
    report() {
      if (this.report !== undefined) {
        this.metric = Object.keys(this.report.no);
      }
    },
  },
};
</script>
