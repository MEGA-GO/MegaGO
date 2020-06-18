<template>
    <v-virtual-scroll height="300" :items="items" :item-height="50">
        <template v-slot="{ item }">
            <v-list-item>
                <v-list-item-avatar>
                    <v-avatar color="primary" size="56" class="white--text">
                        GO
                    </v-avatar>
                </v-list-item-avatar>

                <v-list-item-content>
                    <v-list-item-title>{{ item.code }}</v-list-item-title>
                </v-list-item-content>

                <v-list-item-action>
                    <v-btn depressed small :href="`http://amigo.geneontology.org/amigo/term/${item.code}`" target="_blank">
                        View term
                        <v-icon color="orange darken-4" right>
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

@Component
export default class GoListComponent extends Vue {
    @Prop({ required: true })
    private terms!: string[];

    private items: { code: string }[] = [];

    private mounted() {
        this.onTermsChanged();
    }

    @Watch("terms")
    private onTermsChanged() {
        this.items.splice(0, this.items.length);
        this.items.push(...this.terms.map((id) => {
            return {
                code: id
            };
        }));
    }
}
</script>

<style scoped>

</style>
