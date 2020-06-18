<template>
    <div style="height: 300px;" v-if="loading">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    <v-virtual-scroll v-else height="300" :items="items" :item-height="50" :bench="50">
        <template v-slot="{ item }">
            <v-list-item>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-list-item-avatar>
                            <v-avatar v-on="on" v-bind="attrs" :color="namespaceColor[item.namespace]" size="56" class="white--text">
                                {{ namespaceAvatar[item.namespace] }}
                            </v-avatar>
                        </v-list-item-avatar>
                    </template>
                    <span>{{ humanReadableNamespace(item.namespace) }}</span>
                </v-tooltip>

                <v-list-item-content>
                    <v-list-item-title>{{ item.code }} - {{ item.name }}</v-list-item-title>
                </v-list-item-content>

                <v-list-item-action>
                    <v-btn
                        depressed
                        small
                        :href="`http://amigo.geneontology.org/amigo/term/${item.code}`"
                        target="_blank">
                        View term
                        <v-icon
                            color="orange darken-4"
                            right>
                            mdi-open-in-new
                        </v-icon>
                    </v-btn>
                </v-list-item-action>
            </v-list-item>
        </template>
    </v-virtual-scroll>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import APICommunicator from "@/logic/network/APICommunicator";

@Component
export default class GoListComponent extends Vue {
    @Prop({ required: true })
    private terms!: string[];

    private items: { code: string }[] = [];
    private loading = false;

    private namespaceAvatar = {
        // eslint-disable-next-line quote-props
        "biological_process": "BP",
        // eslint-disable-next-line quote-props
        "cellular_component": "CC",
        // eslint-disable-next-line quote-props
        "molecular_function": "MF"
    }

    private namespaceColor = {
        // eslint-disable-next-line quote-props
        "biological_process": "indigo",
        // eslint-disable-next-line quote-props
        "cellular_component": "red",
        // eslint-disable-next-line quote-props
        "molecular_function": "green"
    }

    private mounted() {
        this.onTermsChanged();
    }

    @Watch("terms")
    private async onTermsChanged() {
        this.loading = true;
        this.items.splice(0, this.items.length);
        this.items.push(...(await APICommunicator.getGoTerms(this.terms)));
        this.loading = false;
    }

    private humanReadableNamespace(ns: string): string {
        return ns.split("_").map(x => {
            if (x.length > 1) {
                return x[0].toUpperCase() + x.slice(1).toLowerCase();
            } else {
                return x.toUpperCase();
            }
        }).join(" ");
    }
}
</script>

<style scoped>

</style>
