<template>
    <div>
        <v-textarea
            solo
            :disabled="disabled"
            name="go-list"
            label="Please a provide a list of valid GO identifiers"
            hide-details
            :rows="10"
            v-model="contents"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            data-gramm_editor="false"
            :loading="loading">
        </v-textarea>
        <div>
            <span style="float: left;">Or <a @click="selectFile" :class="disabled ? 'disabled' : ''">upload a file</a> directly</span>
            <span style="float: right;">{{ this.contents ? this.contents.split("\n").length : 0 }} GO terms in sample</span>
        </div>
        <input type="file" ref="fileUploader" accept="text/plain, .csv" style="display:none">
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

@Component
export default class GoInputComponent extends Vue {
    @Prop({ required: false, default: "" })
    private value!: string;

    @Prop({ required: false, default: false })
    private disabled!: boolean;

    private fileElement!: HTMLInputElement | null;
    private contents = "";
    private loading = false;

    mounted() {
        this.fileElement = this.$refs.fileUploader as HTMLInputElement | null;

        this.fileElement?.addEventListener("change", () => {
            const files = this.fileElement?.files;

            if (files && files.length > 0) {
                this.processFile(files[0]);
            }
        });
    }

    @Watch("value")
    private onValueChanged() {
        this.contents = this.value;
    }

    @Watch("contents")
    private onContentsChanged() {
        this.$emit("input", this.contents);
    }

    private selectFile() {
        if (this.fileElement && !this.disabled) {
            this.fileElement.click();
        }
    }

    private processFile(file: File) {
        this.loading = true;
        const reader = new FileReader();
        reader.onload = (data) => {
            let contents = data?.target?.result;
            if (contents && contents instanceof ArrayBuffer) {
                const decoder = new TextDecoder();
                contents = decoder.decode(contents);
            }

            if (contents) {
                this.contents = atob(contents.split(",")[1]).trimEnd();
            }

            this.loading = false;
        };
        reader.readAsDataURL(file);
    }
}
</script>

<style scoped>
    .disabled {
        color: gray;
        cursor: default;
    }
</style>
