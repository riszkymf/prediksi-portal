import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';
import { datasetStore } from './stores/datasets';

const app = createApp(App)

app.use(createPinia())


const datasetState = datasetStore()

app.use(router)
app.component('EasyDataTable', Vue3EasyDataTable);


app.mount('#app')
