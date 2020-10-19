<template>
    <v-container fluid>
        <div>
            <h1>Help - Web application</h1>
            In this document, we explain the different steps that are required to successfully compare two sets of
            GO-terms using this web application. This is not hard, and consists of the following steps.

            <h2>Homepage</h2>
            Click the big red "start analysis" button. This button will bring you the analysis page.
            <v-img src="@/assets/help_1.png"></v-img>

            <h2>Analyze</h2>
            On the analysis page, you are required to provide two different sets of GO-terms. You can paste these
            GO-terms (one per line) directly in the provided text areas, or you can upload a file. If you choose to
            upload a file that contains one GO-term per line, the terms will automatically be inserted and the set
            of GO-terms can be modified if required.
            <v-img src="@/assets/help_2.png"></v-img>

            <h2>Loading state</h2>
            Once the analysis is started, a progress bar is shown that indicates which part of the analysis has already
            been done. The page will automatically display all analysis results once the computations are done.
            <v-img src="@/assets/help_3.png"></v-img>

            <h2>Results</h2>
            <p>
                The results page is probably the most important page of the whole application. All GO-terms are split into
                3 sets (per sample provided) before the analysis starts: one set per GO domain. The sets of the respective
                domains are then compared to each other, which results in a similarity score. All three similarity scores
                are shown on this page, together with an overview of the GO-terms that were provided in both samples.
            </p>

            <p>
                If one or more GO-terms are unknown to our application, you should see a banner that informs you of which
                terms were not taken into account during the analysis.
            </p>
            <v-img src="@/assets/help_4.png"></v-img>

        </div>
    </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class WebHelp extends Vue {

}
</script>

<style scoped>

</style>
