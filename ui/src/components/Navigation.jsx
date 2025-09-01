import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
    return (
        <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
            <Link to="/" style={{ marginRight: '1rem' }}>Home</Link>
            <Link to="/about">About</Link>
        </nav>
    );
};

export default Navigation;
