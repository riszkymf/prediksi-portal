import { defineStore } from "pinia";
import axios from "axios";

export type TrainResult = {
    train: DatasetResult,
    test: DatasetResult,
    evaluation: EvaluationResult
}

export type PredictionCount = {
    yes: number,
    no: number,
}

export type DatasetResult = {
    accuracy: number,
    prediction_result: object[],
    prediction_count: PredictionCount
    evaluation: ReportMetric
}

export type ReportMetric = {
    yes: {
        [key:string]: number
    },
    no: {
        [key:string]: number
    },
    macro_avg: {
        [key:string]: number
    },
    weighted_avg: {
        [key:string]: number
    }
    accuracy: number
}

export type EvaluationResult = {
    confusion_matrix: {
        true_positive: number,
        true_negative: number,
        false_positive: number,
        false_negative: number,
    },
    report: ReportMetric
}



export const datasetStore = defineStore('dataset',{
    state: ()=>{
        let trainResult: TrainResult|{} = {}
        let dataSetsLists: string[] = []
        return {
            currentDataSet : '',
            dataSetsLists: dataSetsLists,
            trainResult: trainResult,
            resultTrue: false
        }
    },
    actions:{
        setCurrentDataset(datasetTitle:string){
            this.currentDataSet = datasetTitle
        },
        resultExists(){
            try {
                return 'train' in this.trainResult 
                && 'test'  in this.trainResult
                && 'evaluation' in this.trainResult    
            } catch (error) {
                return false
            }

        },
        async getCurrentDataSet(){
            const API_HOST = import.meta.env.VUE_APP_API_HOST || "http://0.0.0.0:5334/api";
            let datasetsFile:string[] = []
            const resp = await axios.get(API_HOST + "/dataset?target=dataset:filename")
            if (resp.status == 200) {
                if(resp.data.code == 200){
                    this.dataSetsLists = resp.data.data ?? []
                    this.currentDataSet = this.dataSetsLists[0] ?? ''
                    datasetsFile = this.dataSetsLists
                } else {
                    console.error(resp.data.message)
                    return []
                }
            } else {
                console.error(resp)
                return []
            }
            return datasetsFile
        },
        async getResult(){
            const API_HOST = import.meta.env.VUE_APP_API_HOST || "http://0.0.0.0:5334/api";
            const resp = await axios.get(API_HOST + "/process?target=dataset:result")
            if (resp.status == 200) {
                if (resp.data.code != 200) {
                  throw Error(resp.data.message)
                } 
                if(resp.data.data ?? false){
                    const trainResult: TrainResult = resp.data.data;
                    this.trainResult = trainResult
                    this.resultTrue = true
                    return trainResult
                }

              }
              else{
                throw Error("Failed to fetch data")
              }
        }
    }
})