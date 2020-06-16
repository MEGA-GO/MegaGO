<template>
    <v-app>
        <v-app-bar app color="primary" dark>
            <v-app-bar-nav-icon @click="navigationDrawer = !navigationDrawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Mega GO</v-toolbar-title>
        </v-app-bar>
        <v-navigation-drawer app v-model="navigationDrawer">
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title class="title">
                        Mega GO
                    </v-list-item-title>
                    <v-list-item-subtitle>
                        Compute similarity
                    </v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>

            <v-divider></v-divider>

            <v-list dense nav class="py-0 mt-4">
                <v-list-item v-for="item of links" :key="item.link" link :to="item.link">
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
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
    private navigationDrawer = false;

    private links = [
        {
            icon: "mdi-home",
            title: "Home",
            link: "/"
        },
        {
            icon: "mdi-domain",
            title: "About",
            link: "/about"
        },
        {
            icon: "mdi-help-circle-outline",
            title: "Help",
            link: "/help"
        }
    ]
}
</script>
