import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navigation from './components/Navigation';
import Discover from './pages/Discover';
import Likes from './pages/Likes';

function App() {
    return (
        <Router>
            <div className="app w-[100vw] h-[100vh] flex flex-col p-2">
                <Navigation />
                <main className="flex-grow">
                    <Routes>
                        <Route path="/" element={<Discover />} />
                        <Route path="/likes" element={<Likes />} />
                    </Routes>
                </main>

            </div>
        </Router>
    );
}

export default App;
