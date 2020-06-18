import axios from "axios";
import SimilarityResponse from "@/logic/network/SimilarityResponse";
import GoTerm from "@/logic/entities/GoTerm";

export default class APICommunicator {
    public static readonly BASE_URL: string = "http://localhost:5000";

    public static async computeSimilarities(go1: string[], go2: string): Promise<SimilarityResponse> {
        const result = await axios.post(`${APICommunicator.BASE_URL}/analyse`, {
            sample1: go1,
            sample2: go2
        });
        return result.data;
    }

    public static async getGoTerms(terms: string[]): Promise<GoTerm[]> {
        const result = await axios.post(`${APICommunicator.BASE_URL}/goterms`, {
            goterms: terms
        });

        return result.data.goterms;
    }
}
