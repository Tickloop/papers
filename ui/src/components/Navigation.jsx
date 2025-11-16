import { useState } from 'react';
import { Link } from 'react-router-dom';
import { IoMenu, IoClose } from "react-icons/io5";
import { MdExitToApp } from "react-icons/md";
import { TbFilterSearch } from "react-icons/tb";
import clsx from 'clsx';
import { Button } from '@/ui';

const Sidebar = ({ isOpen, onClose }) => {
    return (
        <div className={clsx(
            "fixed top-0 left-0 w-full h-full bg-white dark:bg-black opacity-95 z-50",
            "transform transition-transform duration-300 ease-in-out",
            { 'translate-x-0': isOpen, '-translate-x-full': !isOpen }
        )} 
            onClick={onClose}>
            <div className="w-screen h-screen p-2" onClick={(e) => e.stopPropagation()}>
                <div className="flex flex-row justify-between items-center mb-4">
                    <button onClick={onClose}>
                        <IoClose size={24} />
                    </button>
                    <h2 className="text-2xl px-4">
                        <span className="mr-1 italic">lavavite</span>
                        <span className="relative top-[-4px]">🏎️</span>
                        <span className="relative">💨</span>
                    </h2>
                </div>
                <nav className="flex flex-col gap-4">
                    <Link to="/archive" className="text-lg" onClick={onClose}>Archive</Link>
                    <Link to="/profile" className="text-lg" onClick={onClose}>Profile</Link>
                </nav>
                <div className="absolute bottom-4 left-0 w-full flex justify-center">
                    <Link to="/logout" className="flex flex-row items-center gap-2 text-red-500" onClick={onClose}>
                        <MdExitToApp size={20} />
                        <span>Logout</span>
                    </Link>
                </div>
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
            <div>
                <TbFilterSearch size={24} />
            </div>
        </nav>
        </>
    );
};

export default Navigation;
