import Vue from "vue";
import Vuex, { GetterTree, MutationTree, ActionTree, ActionContext, Store } from "vuex";
import APICommunicator from "@/logic/network/APICommunicator";
import SimilarityResponse from "@/logic/network/SimilarityResponse";

Vue.use(Vuex);

export type Similarities = {
    biologicalProcess: number;
    cellularComponent: number;
    molecularFunction: number;
};

export interface GoState {
    goList1: string[];
    goList2: string[];
    // A list with 3 items that respectively represent the similarity for biological process, cellular component
    // and molecular function.
    similarities: Similarities;
    // A list containing all GO terms that were submitted by the user, but that are not known to the application. These
    // terms are thus not taken into account during the analysis.
    invalidTerms: string[];
    // Part of the analysis that has been done at this point.
    progress: number;
}

const state: GoState = {
    goList1: [],
    goList2: [],
    similarities: {
        biologicalProcess: NaN,
        cellularComponent: NaN,
        molecularFunction: NaN
    },
    invalidTerms: [],
    progress: 0
};

const getters: GetterTree<GoState, any> = {
    goList1(state: GoState): string[] {
        return state.goList1;
    },

    goList2(state: GoState): string[] {
        return state.goList2;
    },

    similarities(state: GoState): Similarities {
        return state.similarities;
    },

    invalidTerms(state: GoState): string[] {
        return state.invalidTerms;
    },

    progress(state: GoState): number {
        return state.progress;
    }
};

const mutations: MutationTree<GoState> = {
    UPDATE_GO_LIST1(state: GoState, terms: string[]) {
        state.goList1.splice(0, state.goList1.length);
        state.goList1.push(...terms);
    },

    UPDATE_GO_LIST2(state: GoState, terms: string[]) {
        state.goList2.splice(0, state.goList2.length);
        state.goList2.push(...terms);
    },

    UPDATE_SIMILARITIES(state: GoState, values: number[]) {
        state.similarities.biologicalProcess = values[0];
        state.similarities.cellularComponent = values[1];
        state.similarities.molecularFunction = values[2];
    },

    UPDATE_INVALID_TERMS(state: GoState, terms: string[]) {
        state.invalidTerms.splice(0, state.invalidTerms.length);
        state.invalidTerms.push(...terms);
    },

    UPDATE_PROGRESS(state: GoState, value: number) {
        state.progress = value;
    }
};

const actions: ActionTree<GoState, any> = {
    updateGoList1(store: ActionContext<GoState, any>, terms: string[]) {
        // terms = terms.filter((v, i) => terms.indexOf(v) === i);
        store.commit("UPDATE_GO_LIST1", terms);
    },

    updateGoList2(store: ActionContext<GoState, any>, terms: string[]) {
        // terms = terms.filter((v, i) => terms.indexOf(v) === i);
        store.commit("UPDATE_GO_LIST2", terms);
    },

    /**
     * Compute the similarities between the two sets of GO terms that are currently set.
     */
    async analyse(store: ActionContext<GoState, any>) {
        const id: string = await APICommunicator.computeSimilarities(
            store.getters.goList1,
            store.getters.goList2
        );

        await new Promise<void>(resolve => {
            // Keep requesting a progress update, until the current progress is 1. After that we can safely request the
            // computed results and continue...
            const interval = setInterval(async() => {
                const progress = await APICommunicator.getProgress(id);
                store.commit("UPDATE_PROGRESS", progress);
                if (progress === 1) {
                    const data: SimilarityResponse = await APICommunicator.getResults(id);
                    store.commit("UPDATE_SIMILARITIES", [
                        data.similarity.biological_process,
                        data.similarity.cellular_component,
                        data.similarity.molecular_function
                    ]);
                    store.commit("UPDATE_INVALID_TERMS", data.invalid);

                    clearInterval(interval);
                    resolve();
                }
            }, 2000);
        });
    },

    updateInvalidTerms(store: ActionContext<GoState, any>, terms: string[]) {
        store.commit("UPDATE_INVALID_TERMS", terms);
    }
};

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
});
