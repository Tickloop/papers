import { useContext, useEffect } from 'react';
import { useNavigate, Outlet } from "react-router-dom"
import { AuthContext } from '../contexts/AuthContext';

const Auth = () => {
    const { isAuthenticated, setTarget } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            setTarget(window.location.pathname);
            navigate('/auth', {replace:true});
        }        
    }, [])

    if (!isAuthenticated()) {
        return null;
    }
    return <Outlet />;
}

export default Auth;