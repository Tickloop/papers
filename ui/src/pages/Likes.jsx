import React from 'react';
import { getLikedPapers } from '@/api/papers';

const Likes = () => {
    const [likedPapers, setLikedPapers] = React.useState([]);

    React.useEffect(() => {
        getLikedPapers(0, 10).then(data => setLikedPapers(data));
    }, []);

    return (
        <div className="mt-4">
            <ul>
                {likedPapers.map(paper => (
                    <li key={paper.id} className="text-xs p-2 border-1 shadow-xs my-2 rounded-lg">
                        <div className="font-bold">{paper.title}</div>
                        <div className="text-gray-500 my-1">{paper.author}</div>
                        <div className="line-clamp-4">{paper.abstract}</div>
                        <button className="mt-2 text-xs text-blue-500">
                            <a href={paper.url || ''}>View Paper</a>
                        </button>
                    </li>

                ))}
            </ul>
        </div>
    );
};

export default Likes;
