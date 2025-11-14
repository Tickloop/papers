import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Auth, { Logout } from './pages/Auth';
import PrivateRoute from './pages/PrivateRoute';
import Discover from './pages/Discover';
import DiscoverLayout from './pages/DiscoverLayout';
import Likes from './pages/Likes';
import Home from './pages/Home';
import { AuthProvider } from './contexts/AuthContext';

function App() {
    return (
        <AuthProvider>
        <Router>
            <div className="app min-w-screen min-h-screen flex flex-col">
                <main className="flex-grow">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/auth" element={<Auth />} />
                        <Route path="/logout" element={<Logout />} />

                        <Route element={<PrivateRoute />}>
                            <Route path="/discover" element={<DiscoverLayout />}>
                                <Route index element={<Discover />} />
                                <Route path="likes" element={<Likes />} />
                            </ Route>
                        </Route>
                    </Routes>
                </main>
            </div>
        </Router>
        </AuthProvider>
    );
}

export default App;
