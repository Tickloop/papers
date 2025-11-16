import axios from 'axios';

const localhost = 'http://localhost:8080';
// const localhost = 'http://192.168.1.192:8080';
// const localhost = 'http://100.92.64.105:8080';

const baseClient = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL || localhost}/api`,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});

// Handle Errors globally
baseClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // 401 - Unauthorized
        if (error.response?.status === 401) {
            console.error('Unauthorized access - perhaps redirect to login?', error);
            localStorage.clear();
            window.location.href = '/auth';
        }

        // 422 - Unprocessable entity
        if (error.response?.status === 422) {
            console.error('Validation error:', error);
        }

        // 500 - Server Error
        if (error.response?.status === 500) {
            console.error('Server error:', error);
        }

        return Promise.reject(error);
    }
);

export default baseClient;