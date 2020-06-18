<template>
    <v-container fluid>
        <div class="text-h3">Result</div>
        <div class="text-h4 my-4">Similarities</div>
        <div class="d-flex justify-space-between">
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
        <div class="text-h4 my-4">Sample summary</div>
        <v-row>
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
