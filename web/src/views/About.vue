<template>
    <v-container fluid>
        <div>
            <div class="text-h3">About us</div>
            <p class="text-body-1">
                Mega GO is a project that aims at comparing two sets of GO terms and started initially at the EuBIC
                conference in Nyborg, Denmark (2020). The Mega GO project aims to provide users with a measure that
                indicates how similar two sets of GO terms are to each other.
            </p>
            <div class="text-h4">Our team</div>
            <v-container fluid>
                <v-row>
                    <v-col :md="4" :sm="12">
                        <team-card name="Henning Schiebenhoefer" affiliation="Robert Koch Institut, Germany"></team-card>
                    </v-col>
                    <v-col :md="4" :sm="12">
                        <team-card
                            name="Tim Van Den Bossche"
                            affiliation="Ghent University, Belgium"
                            :profile-picture="require('./../assets/tim_profile.jpg')">
                        </team-card>
                    </v-col>
                    <v-col :md="4" :sm="12">
                        <team-card
                            name="Pieter Verschaffelt"
                            affiliation="Ghent University, Belgium"
                            :profile-picture="require('./../assets/pieter_profile.jpg')">
                        </team-card>
                    </v-col>
                    <v-col :md="4" :sm="12">
                        <team-card
                            name="Bart Mesuere"
                            affiliation="Ghent University, Belgium"
                            :profile-picture="require('./../assets/bart_profile.jpeg')">
                        </team-card>
                    </v-col>
                    <v-col :md="4" :sm="12">
                        <team-card name="Wassim Gabriel" affiliation="Technische Universität München, Germany"></team-card>
                    </v-col>
                    <v-col :md="4" :sm="12">
                        <team-card name="Michał Burdukiewicz" affiliation="Warsaw University of Technology, Poland"></team-card>
                    </v-col>
                    <v-col :md="4" :sm="12">
                        <team-card name="Alessio Soggiu" affiliation="University of Milan, Italy"></team-card>
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </v-container>

</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import TeamCard from "@/components/TeamCard.vue";
@Component({
    components: { TeamCard }
})
export default class About extends Vue {

}
</script>

<style scoped>

</style>
