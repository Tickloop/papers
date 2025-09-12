import axios from 'axios';

const localhost = 'http://localhost:8080';
// const localhost = 'http://192.168.1.192:8080';

const baseClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || localhost,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Handle Errors globally
baseClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // 401 - Unauthorized
        if (error.response?.status === 401) {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
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

// Request interceptor
// baseClient.interceptors.request.use(
//     (config) => {
//         const token = localStorage.getItem('authToken');
//         if (token) {
//             config.headers.Authorization = `Bearer ${token}`;
//         }
//         return config;
//     },
//     (error) => {
//         return Promise.reject(error);
//     }
// );

// // Response interceptor
// baseClient.interceptors.response.use(
//     (response) => {
//         return response;
//     },
//     (error) => {
//         if (error.response?.status === 401) {
//             localStorage.removeItem('authToken');
//             window.location.href = '/login';
//         }
//         return Promise.reject(error);
//     }
// );

export default baseClient;