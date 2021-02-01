<template>
    <v-container fluid>
        <div>
            <h1>Help - Command Line Interface</h1>
            The MegaGO command line interface is a Python-package that can be easily installed using PiP. MegaGO
            requires at least Python 3.6 to work. All required dependencies will automatically be installed when using
            PiP, but you can also install the package from source by cloning our
            <a href="https://github.com/MEGA-GO/MegaGO">GitHub repository</a>.
            <h2 class="mt-6">Installation</h2>
            <ul>
                <li>
                    First, make sure that a valid Python 3.6 installation is available on your system. If you're using
                    macOS you can use HomeBrew to install Python by running <span class="monospace">brew install
                    python3</span>. On Windows, you can find Python 3 in the Microsoft Store, which offers a one-click
                    installation process.
                </li>
                <li>
                    Execute <span class="monospace">pip --version</span>. If an error is shown or the output indicates
                    that this is a PiP-version that belongs to Python version 2, use <span class="monospace">pip3</span>
                    in the following commands.
                </li>
                <li>
                    Now, run <span class="monospace">pip install megago</span> to install the application.
                </li>
            </ul>
            <h2 class="mt-6">Usage</h2>
            To start using the CLI, you have to provide it two sets of GO-terms that should be compared with each other.
            The default usage is the following:
            <div class="monospace code-block">
                <span class="font-weight-black">
                    $ megago [-h] [--version] [--log LOG_FILE] [--verbose] [--plot PLOT_FILE] [SAMPLE_1] [SAMPLE_2] ... [SAMPLE_N]
                </span>
            </div>
            You can directly pass two sets of GO-terms, separated by semicolons, to start the analysis. Or you can
            provide two CSV-files, each containing a list of GO-terms, one term per line. The application checks if the
            arguments you provided end in a valid file-extension or not, and determines from this information if you
            passed in a set of GO-terms directly or not.

            <h4 class="mt-4">Example - directly providing GO-terms</h4>
            <div class="monospace code-block">
                <div class="font-weight-black">
                    $ megago &quot;GO:0006412;GO:0005975;GO:0042026&quot; &quot;GO:0006457;GO:0006351&quot;
                </div>
                <div>
                    DOMAIN,SIMILARITY<br>
                    biological_process,0.5758376741973126<br>
                    cellular_component,0<br>
                    molecular_function,0
                </div>
            </div>

            <h4 class="mt-4">Example - using CSV-files</h4>
            <div class="monospace code-block">
                <div class="font-weight-black">
                    $ megago <a href="/samples/sample7.txt" download="sample7.txt">sample7.txt</a> <a href="/samples/sample8.txt" download="sample8.txt">sample8.txt</a>
                </div>
                <div>
                    DOMAIN,SIMILARITY<br>
                    biological_process,0.7489033566836133<br>
                    cellular_component,0.8207787417812381<br>
                    molecular_function,0.877707549440742
                </div>
            </div>

            <h3 class="mt-4">Command line options</h3>
            <h4>--version</h4>
            Print the currently installed version of the MegaGO CLI.
            <div class="monospace code-block">
                <div class="font-weight-black">
                    $ megago --version
                </div>
                <div>
                    megago 0.2.2
                </div>
            </div>
            <h4 class="mt-4">--log LOG_FILE</h4>
            Indicate the file to which all log-related information should be written. If an existing file is given, it
            will be overwritten. Requires a file argument!
            <div class="monospace code-block">
                <div class="font-weight-black">
                    $ megago --log logfile.txt GO:0099131 GO:0000000
                </div>
                <div>
                    DOMAIN,SIMILARITY<br>
                    biological_process,nan<br>
                    cellular_component,0<br>
                    molecular_function,0
                </div>
                <div class="font-weight-black">
                    $ cat logfile.txt
                </div>
                <div>
                    2020-10-19T11:01:02+0200 WARNING - GO:0000000 was not found in the Gene Ontology parsed by this
                    script
                </div>
            </div>
            <h4 class="mt-4">--verbose / -v</h4>
            Print all available information messages during the analysis. By default, not all status messages are
            shown. By enabling this option, all messages are always printed.
            <h4 class="mt-4">--plot PLOT_FILE</h4>
            Generate a swarm plot of the GO similarities that were computed by this script. Requires a file argument!
            The filetype is automatically determined based on the extension used (e.g. .png, .svg, ...)
            <h4 class="mt-4">--heatmap</h4>
            Generate an interactive heatmap that visualises the pairwise similarities between all given samples. Note
            that clustering has been automatically applied to these heatmaps. A "heatmap.html" will be produced in the
            current working directory when this option has been set.
            <h4 class="mt-4">--help / -h</h4>
            Print all options for this command.
        </div>
    </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class Help extends Vue {

}
</script>

<style scoped>
    .monospace {
        font-family: 'Roboto Mono', monospace;
        background-color: #ddd;
    }

    .code-block {
        border: 1px solid gray;
        padding: 4px;
    }
</style>
