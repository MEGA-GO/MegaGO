<template>
    <div>
        <v-textarea solo name="input-7-4" label="Please a provide a list of valid GO identifiers" hide-details :rows="10">
        </v-textarea>
        <span>Or <a @click="uploadFile">upload a file</a> directly</span>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class GoInputComponent extends Vue {
    private uploadFile() {
        console.log();
    }
}
</script>

<style scoped>

</style>
