<template>
  <div class="col-md-10 mt-5 py-3">
    <h3>Tambah Data</h3>
  </div>
  <div class="w-100"></div>
  <div class="col-md-10">
    <AlertDiv :message="alert.message" :type="alert.type" />
  </div>
  <div class="w-100"></div>
  <div class="col-md-6" id="uploadForm">
    <div class="mb-3">
      <div class="input-group">
        <input
          accept=".csv"
          @change="
            {
              getFile($event);
            }
          "
          class="form-control"
          type="file"
          id="formFile"
        />
        <button
          @click="uploadFile"
          class="btn btn-sm btn-secondary"
          type="submit"
          :disabled="file.name == ''"
        >
          Unggah File
        </button>
      </div>
      <small id="passwordHelpBlock" class="form-text text-muted">
        File harus dalam format csv
      </small>
    </div>
  </div>
  <div class="col-md-11" :class="{ hide: !parsed }">
    <div class="table-responsive">
      <span class="title">
        <h5>
          {{ filename }}
        </h5>
      </span>
      <EasyDataTable :headers="table.headers" :items="table.content" />
    </div>
  </div>
  <div class="col-md-10" :class="{ hide: !existingFilenames }">
    <div class="table-responsive">
      <span class="title">
        <h5>Data yang sudah diunggah</h5>
      </span>
      <EasyDataTable :headers="filenameTable.headers" :items="filenameTable.content" />
    </div>
  </div>
</template>

<style lang="scss">
.hide {
  display: none !important;
}
</style>

<script lang="ts">
import Papa from "papaparse";
import type { Header, Item } from "vue3-easy-data-table";
import axios from "axios";
import AlertDiv from "@/components/AlertDiv.vue";
import { datasetStore } from "@/stores/datasets";

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
    const filenameTableContent: Item[] = [];

    const tableContent: Item[] = [];
    const filenameTableHeaders: Header[] = [
      { text: "No", value: "No" },
      { text: "Dataset", value: "filename" },
    ];
    const fileUpload: File = new File([""], "");

    return {
      file: fileUpload,
      filename: "",
      parsed: false,
      table: {
        headers: tableHeaders,
        content: tableContent,
      },
      filenameTable: {
        headers: filenameTableHeaders,
        content: filenameTableContent,
      },
      alert: {
        message: "",
        type: "alert-success",
      },
    };
  },
  methods: {
    readDatasets() {},
    getFile($event: Event) {
      const target = $event.target as HTMLInputElement;
      if (target && target.files) {
        let fileupload = target.files[0];
        this.file = fileupload;
        this.filename = target.files[0].name;
        this.parseFile();
      }
    },
    createTable(results: Papa.ParseResult<object>) {
      this.parsed = true;
      const headers = results.meta.fields;
      if (headers) {
        this.table.headers = headers.map((el: string) => {
          return {
            text: el,
            value: el,
          };
        });
      }
      this.table.content = results.data;
    },
    parseFile() {
      Papa.parse(this.file, {
        header: true,
        skipEmptyLines: false,
        complete: this.createTable,
      });
    },
    getFilename() {
      this.datasetState.getCurrentDataSet().then(() => {
        const filenames = this.datasetState.dataSetsLists;
        console.log(filenames);
        let counter = 1;
        filenames.forEach((el) => {
          this.filenameTable.content.push({
            No: counter,
            filename: el,
          });
          counter = counter + 1;
        });
      });
    },
    uploadFile() {
      const API_HOST = import.meta.env.VUE_APP_API_HOST || "http://0.0.0.0:5334/api";
      let formData = new FormData();
      formData.append("file", this.file);
      axios
        .post(API_HOST + "/dataset", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(() => {
          this.alert.type = "success";
          this.alert.message = "Berhasil mengunggah dataset";
          this.getFilename();
        })
        .catch((reason: string) => {
          this.alert.type = "error";
          this.alert.message = "Gagal mengunggah dataset " + reason;
        });
    },
    existingFilenames() {
      return this.datasetState.currentDataSet !== "";
    },
  },
  mounted: function () {
    this.datasetState.getCurrentDataSet();
    this.getFilename();
  },
};
</script>
