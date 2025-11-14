import baseClient from "./baseclient";

export const loginUser = async (username, password) => {
    return baseClient.post('/v1/auth/login', { username, password })
        .then(res => res.data);
}
    
export const signupUser = async (fullname, username, password) => {
    return baseClient.post('/v1/auth/signup', { fullname, username, password })
        .then(res => res.data);
}