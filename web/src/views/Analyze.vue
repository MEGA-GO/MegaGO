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
        <v-row>
            <v-col :cols="6">
                <div class="text-h4 mb-2">Sample 1</div>
                <go-input-component :disabled="loading" v-model="goList1"></go-input-component>
            </v-col>
            <v-col :cols="6">
                <div class="text-h4 mb-2">Sample 2</div>
                <go-input-component :disabled="loading" v-model="goList2"></go-input-component>
            </v-col>
        </v-row>
        <v-row>
            <div class="d-flex justify-center" style="width: 100%;">
                <v-btn large :loading="loading" color="primary" @click="startAnalysis" :disabled="loading">
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
            this.$store.dispatch("updateGoList1", newValue.split("\n"));
        }
    }

    @Watch("goList2")
    private onGoList2Changed(newValue: string, oldValue: string) {
        if (oldValue !== newValue) {
            this.$store.dispatch("updateGoList2", newValue.split("\n"));
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
}
</script>

<style>
    .v-banner__wrapper {
        padding: 0;
    }
</style>
