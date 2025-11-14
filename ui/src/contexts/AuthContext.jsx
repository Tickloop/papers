import { loginUser, signupUser } from "../api/auth";
import { createContext, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [target, setTarget] = useState(null);

    const isAuthenticated = () => {
        const token = localStorage.getItem('authToken');
        return token !== null;
    };

    const login = (username, password) => {
        return loginUser(username, password)
            .then(data => {
                localStorage.setItem('authToken', data.token);
            })
            .catch(err => {
                throw err;
            });
    }

    const signup = (fullname, username, password) => {
        return signupUser(fullname, username, password)
            .then(data => {
                localStorage.setItem('authToken', data.token);
            });
    }

    const logout = () => {
        localStorage.removeItem('authToken');
    }


    return (
        <AuthContext.Provider value={{ isAuthenticated, login, signup, logout, target, setTarget }}>
            {children}
        </AuthContext.Provider>
    );
}