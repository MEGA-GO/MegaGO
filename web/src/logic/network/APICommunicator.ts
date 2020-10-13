import axios from "axios";
import SimilarityResponse from "@/logic/network/SimilarityResponse";
import GoTerm from "@/logic/entities/GoTerm";

export default class APICommunicator {
    public static readonly BASE_URL: string = "/api";

    public static async computeSimilarities(go1: string[], go2: string): Promise<string> {
        const result = await axios.post(`${APICommunicator.BASE_URL}/analyze`, {
            sample1: go1,
            sample2: go2
        });
        return result.data.analysis_id;
    }

    public static async getProgress(id: string): Promise<number> {
        const result = await axios.post(`${APICommunicator.BASE_URL}/progress/${id}`);
        return parseFloat(result.data.progress);
    }

    public static async getResults(id: string): Promise<SimilarityResponse> {
        const result = await axios.post(`${APICommunicator.BASE_URL}/result/${id}`);
        return result.data;
    }

    public static async getGoTerms(terms: string[]): Promise<GoTerm[]> {
        const result = await axios.post(`${APICommunicator.BASE_URL}/goterms`, {
            goterms: terms
        });

        return result.data.goterms;
    }
}
