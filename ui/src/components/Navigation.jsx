import { Link } from 'react-router-dom';

const Navigation = () => {
    return (
        <nav className="px-1 flex flex-row justify-around">
            <Link to="/">Discover</Link>
            <Link to="/likes">Liked</Link>
        </nav>
    );
};

export default Navigation;
