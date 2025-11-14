import Navigation from '@/components/Navigation';
import { Outlet } from 'react-router-dom';

const DiscoverLayout = () => {
    return (
        <>
            <Navigation />
            <Outlet />
        </>
    )
}

export default DiscoverLayout;