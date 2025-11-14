import { useState } from 'react';
import { Link } from 'react-router-dom';
import { IoMenu, IoClose } from "react-icons/io5";
import { MdExitToApp } from "react-icons/md";
import clsx from 'clsx';

const Sidebar = ({ isOpen, onClose }) => {
    

    return (
        <div className={clsx(
            "fixed top-0 left-0 w-full h-full bg-black opacity-90 z-50",
            "transform transition-transform duration-300 ease-in-out",
            { 'translate-x-0': isOpen, '-translate-x-full': !isOpen }
        )} 
            onClick={onClose}>
            <div className="w-screen h-screen p-4" onClick={(e) => e.stopPropagation()}>
                <div className="flex flex-row justify-between items-center mb-4">
                    <button onClick={onClose}>
                        <IoClose size={24} />
                    </button>
                    <h2 className="text-2xl">Sidebar Menu</h2>
                </div>
                <ul>
                    <li className="p-4 flex flex-row justify-between items-center border-b">
                        <Link to="/logout" onClick={onClose} className="text-lg">Logout</Link>
                        <MdExitToApp size={24} />
                    </li>
                </ul>
            </div>
        </div>
    );
};

const Navigation = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <>
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <nav className="flex flex-row justify-between items-center gap-4 p-2">
            <div>
                <IoMenu size={24} onClick={() => setSidebarOpen(!sidebarOpen)}/>
            </div>
            <div className="p-2 flex flex-row justify-around flex-1">
                <Link to="/discover">Discover</Link>
                <Link to="/discover/likes">Liked</Link>
            </div>
        </nav>
        </>
    );
};

export default Navigation;
