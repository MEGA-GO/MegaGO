<template>
    <v-container fluid>
        <v-alert type="error" v-if="errorVisible">
            Could not complete your request. Please try again later...
        </v-alert>

        <div class="text-h3">Analyze</div>
        <p class="text-body-1">
            Please provide two lists of GO-terms for which the domain-based similarity should be computed. These lists
            can either be pasted directly in the textarea's below, or you can upload a valid file containing one term
            per line. Both txt-based and csv-based files are accepted.
        </p>
        <p>
            See the following files for some valid example inputs:
            <a href="/samples/sample7.txt" download="sample7.txt">sample7.txt</a>,
            <a href="/samples/sample8.txt" download="sample8.txt">sample8.txt</a>.
        </p>
        <v-row>
            <v-col :cols="6">
                <div class="mb-2">
                    <span class="text-h4">Sample 1</span>
                    <a class="float-right" style="position: relative; top: 16px;" @click="loadSample7Data()">
                        Use sample data
                    </a>
                </div>
                <go-input-component :disabled="loading" v-model="goList1"></go-input-component>
            </v-col>
            <v-col :cols="6">
                <div class="mb-2">
                    <span class="text-h4">Sample 2</span>
                    <a class="float-right" style="position: relative; top: 16px;" @click="loadSample8Data()">
                        Use sample data
                    </a>
                </div>
                <go-input-component :disabled="loading" v-model="goList2"></go-input-component>
            </v-col>
        </v-row>
        <v-row>
            <div class="d-flex justify-center" style="width: 100%;">
                <v-progress-linear v-if="loading" :value="$store.getters.progress * 100" height="25">
                    <template v-slot="{ value }">
                        <strong>{{ Math.ceil(value) }}%</strong>
                    </template>
                </v-progress-linear>
                <v-btn large v-else color="primary" @click="startAnalysis" :disabled="loading">
                    <v-icon large dark class="mr-2">mdi-play-circle</v-icon>
                    Analyze!
                </v-btn>
            </div>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import GoInputComponent from "@/components/GoInputComponent.vue";
import { Watch } from "vue-property-decorator";
import sample7 from "raw-loader!@/assets/sample7.txt";
import sample8 from "raw-loader!@/assets/sample8.txt";

@Component({
    components: { GoInputComponent }
})
export default class Analyse extends Vue {
    private goList1 = "";
    private goList2 = "";

    private loading = false;

    private errorVisible = false;

    private created() {
        this.goList1 = this.$store.getters.goList1.join("\n");
        this.goList2 = this.$store.getters.goList2.join("\n");
    }

    @Watch("goList1")
    private onGoList1Changed(newValue: string, oldValue: string) {
        if (oldValue !== newValue) {
            this.$store.dispatch("updateGoList1", newValue.trimEnd().split("\n"));
        }
    }

    @Watch("goList2")
    private onGoList2Changed(newValue: string, oldValue: string) {
        if (oldValue !== newValue) {
            this.$store.dispatch("updateGoList2", newValue.trimEnd().split("\n"));
        }
    }

    private async startAnalysis() {
        this.errorVisible = false;
        try {
            this.loading = true;
            await this.$store.dispatch("analyse");
            this.loading = false;
            await this.$router.push("/result");
        } catch (err) {
            console.error(err);
            this.loading = false;
            this.errorVisible = true;
        }
    }

    private async loadSample7Data() {
        this.goList1 = sample7;
    }

    private async loadSample8Data() {
        this.goList2 = sample8;
    }
}
</script>

<style>
    .v-banner__wrapper {
        padding: 0;
    }
</style>
