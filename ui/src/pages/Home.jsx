import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div className="flex flex-col justify-center items-center min-h-screen">
            <h1 className="text-3xl font-bold">Welcome to the Home Page</h1>
            <p className="mt-4 text-lg">Explore papers and manage your likes!</p>
            <div className="mt-6 flex flex-row gap-4">
                <Link to="/discover" className="px-4 py-2 outline-blue-500 border border-blue-500  hover:outline-2 hover:outline-blue-300 rounded transition">
                    Discover Papers
                </Link>
            </div>
        </div>
    )
}

export default Home;