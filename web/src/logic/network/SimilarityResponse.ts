export default interface SimilarityResponse {
    invalid: string[],
    similarity: {
        biological_process: number,
        cellular_component: number,
        molecular_function: number
    }
}
