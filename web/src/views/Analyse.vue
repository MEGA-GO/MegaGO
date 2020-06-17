<template>
    <v-container fluid>
        <v-row>
            <v-col :cols="6">
                <div class="text-h4 mb-2">Sample 1</div>
                <go-input-component v-model="goList1"></go-input-component>
            </v-col>
            <v-col :cols="6">
                <div class="text-h4 mb-2">Sample 2</div>
                <go-input-component v-model="goList2"></go-input-component>
            </v-col>
        </v-row>
        <v-row>
            <div class="d-flex justify-center" style="width: 100%;">
                <v-btn color="primary" @click="startAnalysis" :disabled="loading">
                    <v-icon dark class="mr-2">mdi-play-circle</v-icon>
                    Analyse!
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
        this.loading = true;
        await this.$store.dispatch("analyse");
        this.loading = false;
    }
}
</script>

<style scoped>

</style>
