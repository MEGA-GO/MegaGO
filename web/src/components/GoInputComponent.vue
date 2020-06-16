<template>
    <div>
        <v-textarea solo name="input-7-4" label="Please a provide a list of valid GO identifiers" hide-details :rows="10">
        </v-textarea>
        <span>Or <a @click="selectFile">upload a file</a> directly</span>
        <input type="file" ref="fileUploader" accept="text/plain, .csv" style="display:none">
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class GoInputComponent extends Vue {
    private fileElement!: HTMLInputElement | null;

    mounted() {
        this.fileElement = this.$refs.fileUploader as HTMLInputElement | null;

        this.fileElement?.addEventListener("change", () => {
            const files = this.fileElement?.files;

            if (files && files.length > 0) {
                this.processFile(files[0]);
            }
        });
    }

    private selectFile() {
        if (this.fileElement) {
            this.fileElement.click();
        }
    }

    private processFile(file: File) {
        const reader = new FileReader();
        reader.onload = (data) => {
            let contents = data?.target?.result;
            if (contents && contents instanceof ArrayBuffer) {
                const decoder = new TextDecoder();
                contents = decoder.decode(contents);
            }

            if (contents) {
                const decoded = atob(contents.split(",")[1]);
                console.log(decoded);
            }
        };
        reader.readAsDataURL(file);
    }
}
</script>

<style scoped>

</style>
