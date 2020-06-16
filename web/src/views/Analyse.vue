<template>
    <v-container fluid>
        <v-row>
            <v-col :cols="6">
                <div class="text-h4 mb-2">Sample 1</div>
                <go-input-component></go-input-component>
            </v-col>
            <v-col :cols="6">
                <div class="text-h4 mb-2">Sample 2</div>
                <go-input-component></go-input-component>
            </v-col>
        </v-row>
        <v-row>
            <div class="d-flex justify-center" style="width: 100%;">
                <v-btn color="primary">
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

@Component({
    components: { GoInputComponent }
})
export default class Analyse extends Vue {

}
</script>

<style scoped>

</style>
