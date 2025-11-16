import { useContext, useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { AuthContext } from "../contexts/AuthContext"
import { Input, Button } from "@/ui";

const Login = () => {
    const { login, target } = useContext(AuthContext);
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [err, setErr] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        login(username, password)
            .then(() => {
                setErr('');
                navigate(target || '/',{replace:true});
            })
            .catch(err => {
                setErr(err.response?.data?.message || 'Login failed');
            });
    }

    return (
        <div className="flex flex-col items-center justify-center">
            <h1 className="text-2xl font-bold mb-4">Login</h1>

            {err &&<div className="p-4 bg-red-300 rounded mb-4 w-full text-center">
                <p className="text-red-500">{err}</p>
            </div>}
            
            <form className="flex flex-col gap-4"
                onSubmit={handleLogin}
            >
                <div>
                    <label htmlFor="username">Username:</label>
                    <Input type="text" id="username" name="username"
                        className=""
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <Input type="password" id="password" name="password"
                        className=""
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <Button type="submit" size="lg">Login</Button>
            </form>
        </div>
    )
}

const Signup = () => {
    const { signup } = useContext(AuthContext);
    const [fullname, setFullname] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSignup = (e) => {
        e.preventDefault();
        signup(fullname, username, password);
    }

    return (
        <div className="flex flex-col items-center justify-center">
            <h1 className="text-2xl font-bold mb-4">Signup</h1>

            <form className="flex flex-col gap-4" onSubmit={handleSignup}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <Input type="text" id="username" name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="email">Email:</label>
                    <Input type="email" id="email" name="email" 
                        value={fullname}
                        onChange={(e) => setFullname(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <Input type="password" id="password" name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <Button type="submit" size="lg">Signup</Button>
            </form>
        </div>
    )
}

export const Logout = () => {
    const { logout } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        logout();
        navigate('/', { replace: true });
    }, []);

    return null;
}

const Auth = () => {
    const [isSignup, setIsSignup] = useState(false);

    return (
        <div className="flex flex-col justify-center items-center min-h-screen gap-8">
            {isSignup ? <Signup /> : <Login />}
            <button
                className="mt-4 text-blue-500 underline"
                onClick={() => setIsSignup(!isSignup)}
            >
                {isSignup ? "Already have an account? Login" : "Don't have an account? Signup"}
            </button>
        </div>
    );
}

export default Auth;