<template>
    <v-container fluid>
        <div v-if="$store.getters.invalidTerms.length > 0">
            <v-alert type="warning">
                Attention: the following GO terms you provided are invalid or unknown to our systems. These terms are
                not being used during the similarity analysis: {{ $store.getters.invalidTerms.join(", ") }}
            </v-alert>
        </div>
        <div class="text-h3">Result</div>
        This page contains the similarity computed between the two samples you submitted during the previous step of the
        analysis process.
        <div class="text-h4 mt-4">Similarities</div>
        Since GO terms that originate from different GO domains cannot be directly compared, we provide you with 3
        different similarity values: one for each GO domain.
        <div class="d-flex justify-space-between mt-4">
            <v-card style="width: 300px; height: 300px;" class="mr-8">
                <div class="d-flex flex-column" style="height: 100%;">
                    <v-card-title>Biological process</v-card-title>
                    <v-card-text class="d-flex justify-center align-center flex-grow-1 flex-column">
                        <img src="./../assets/biological_process.svg" alt="biological process icon" style="height: 150px;"/>
                        <v-avatar :color="colorScale($store.getters.similarities.biologicalProcess)" size="60" class="mt-4">
                            <span class="white--text headline">
                                {{ Math.round($store.getters.similarities.biologicalProcess * 100) }}%
                            </span>
                        </v-avatar>
                    </v-card-text>
                </div>
            </v-card>

            <v-card style="width: 300px; height: 300px;" class="mr-8">
                <div class="d-flex flex-column" style="height: 100%;">
                    <v-card-title>Cellular component</v-card-title>
                    <v-card-text class="d-flex justify-center align-center flex-grow-1 flex-column">
                        <img src="./../assets/cellular_component.svg" alt="cellular component icon" style="height: 150px;"/>
                        <v-avatar :color="colorScale($store.getters.similarities.cellularComponent)" size="60" class="mt-4">
                            <span class="white--text headline">
                                {{ Math.round($store.getters.similarities.cellularComponent * 100) }}%
                            </span>
                        </v-avatar>
                    </v-card-text>
                </div>
            </v-card>

            <v-card style="width: 300px; height: 300px;">
                <v-responsive :aspect-ratio="1">
                    <div class="d-flex flex-column" style="height: 100%;">
                        <v-card-title>Molecular function</v-card-title>
                        <v-card-text class="d-flex justify-center align-center flex-grow-1 flex-column">
                            <img src="./../assets/molecular_function.svg" alt="molecular function icon" style="height: 150px;"/>
                            <v-avatar :color="colorScale($store.getters.similarities.molecularFunction)" size="60" class="mt-4">
                                <span class="white--text headline">
                                    {{ Math.round($store.getters.similarities.molecularFunction * 100) }}%
                                </span>
                            </v-avatar>
                        </v-card-text>
                    </div>
                </v-responsive>
            </v-card>
        </div>
        <div class="text-h4 mt-4">Sample summary</div>
        You can find a summary of all GO terms that are present in both files below. You can filter or sort these tables
        by domain, identifier or name.
        <v-row class="mt-4">
            <v-col :cols="6">
                <v-card>
                    <v-card-title>
                        Sample 1
                    </v-card-title>
                    <v-card-text>
                        <go-list-component :terms="$store.getters.goList1"></go-list-component>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col :cols="6">
                <v-card>
                    <v-card-title>
                        Sample 2
                    </v-card-title>
                    <v-card-text>
                        <go-list-component :terms="$store.getters.goList2"></go-list-component>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import GoListComponent from "./../components/GoListComponent.vue";
import { scaleLinear } from "d3-scale";

@Component({
    components: { GoListComponent }
})
export default class Result extends Vue {
    // @ts-ignore
    private colorScale = scaleLinear().domain([0, 1]).range(["#F44336", "#8BC34A"]);
}
</script>

<style scoped>

</style>
