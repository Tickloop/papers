import React from 'react';
import { getLikedPapers, deleteLikedPaper } from '@/api/papers';
import { Button } from '@/ui';
import { IoOpenOutline, IoTrashBin, IoArchiveOutline } from "react-icons/io5";
import clsx from 'clsx';

const LikedPaper = ({ paper, key, onArchive, onDelete }) =>  {
    const [ isTruncated, setIsTruncated ] = React.useState(true);

    return (
        <li key={key} className="text-sm p-4 border-b border-gray-300">
            <div className="font-bold text-md">{paper.title}</div>
            <div className="text-gray-500 my-1">{paper.author}</div>
            <div className="flex flex-col">
            <span 
                className={clsx({ "line-clamp-4": isTruncated })}
            >
                {paper.abstract}</span>
                <span 
                onClick={() => setIsTruncated(!isTruncated)}
                    className="text-blue-500 cursor-pointer">
                        ...read {isTruncated ? 'more' : 'less'}
                    </span>
            </div>
            
            <div className="flex flex-row gap-2 mt-2 justify-end">
                <Button  
                    variant="icon"
                    >
                    <a href={paper.url || ''} target='_blank' rel="noopener noreferrer">
                        <IoOpenOutline />
                    </a>
                </Button>
                <Button 
                    className="text-green-500" 
                    variant="icon"
                    onClick={() => onArchive(paper.id)}
                    >
                        <IoArchiveOutline />
                </Button>
                <Button 
                    className="text-red-500" 
                    variant="icon"
                    onClick={() => onDelete(paper.id)}
                    >
                        <IoTrashBin />
                </Button>
            </div>
        </li>
    )
}

const Likes = () => {
    const [likedPapers, setLikedPapers] = React.useState([]);
    
    const removePaperFromLikes = (paperId) => {
        setLikedPapers(prevPapers => prevPapers.filter(paper => paper.id !== paperId));
    }

    const handleArchivePaper = (paperId) => {
        removePaperFromLikes(paperId);

        // Implement archive functionality here
        console.log(`Archive paper with ID: ${paperId}`);
    }

    const handleDeletePaper = (paperId) => {
        removePaperFromLikes(paperId);
        deleteLikedPaper(paperId);
        console.log(`Delete paper with ID: ${paperId}`);
    }

    React.useEffect(() => {
        getLikedPapers().then(data => setLikedPapers(data));
    }, []);

    return (
        <div className="mt-4">
            {likedPapers.length === 0 ?
                <p className="text-center">No liked papers 😞</p>
                :
                <ul className="flex flex-col">
                    {likedPapers.map((paper, index) => (
                        <LikedPaper 
                            key={index}
                            paper={paper}
                            onArchive={() => handleArchivePaper(paper.id)}
                            onDelete={() => handleDeletePaper(paper.id)}
                        />
                    ))}
                </ul>
            }
        </div>
    );
};

export default Likes;
