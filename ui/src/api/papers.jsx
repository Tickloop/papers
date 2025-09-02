import baseClient from "./baseclient";

const getPapers = async (limit = 25) => {
    return baseClient.get(`/v1/papers?limit=${limit}`)
        .then(res => res.data);
};

const sendPaperAction = async (id, action) => {
    return baseClient.post("/v1/papers", { id, action })
        .then(res => res.data);
};


const getLikesCount = async () => {
    return baseClient.get("/v1/papers/count/likes")
        .then(res => res.data)
};

const getTotalCount = async () => {
    return baseClient.get(baseURL + "/v1/papers/count/total")
        .then(res => res.json())
};

const getLikedPapers = async (offset = 0, limit = 10) => {
    return baseClient.get(`/v1/papers/likes?offset=${offset}&limit=${limit}`)
        .then(res => res.data);
};

export { getPapers, sendPaperAction, getLikesCount, getTotalCount, getLikedPapers };