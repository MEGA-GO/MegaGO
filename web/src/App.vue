<template>
    <v-app>
        <v-app-bar app color="primary" dark>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>
            <v-toolbar-title>Mega GO</v-toolbar-title>
        </v-app-bar>
        <v-main class="mx-xs-2 mx-sm-4 mx-md-16">
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-main>
    </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class App extends Vue {
}
</script>
