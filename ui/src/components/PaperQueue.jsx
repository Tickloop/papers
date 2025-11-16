import React from 'react';
import clsx from 'clsx';
import { motion, useAnimation } from "framer-motion";
import {getPapers, sendPaperAction} from '@/api/papers';

const Paper = (
    { id, title, author, abstract }
) => {
    return (
        <div>
            <h2 className="text-sm font-bold">{title}</h2>
            <h3 className="text-xs font-thin italic my-1 whitespace-nowrap overflow-hidden text-ellipsis">{author}</h3>
            <p className="text-xs text-ellipsis overflow-hidden">{abstract}</p>
        </div>
    );
}

const Card = ({ children, id, onAccept, onReject, postUpdate }) => {
    // This one handles the motion and action
    // Child only diplays information
    const controls = useAnimation();
    const swipeSpeedThreshold = 100;
    const swipeOffsetThreshold = 150;

    const isValidSwipe = (offset, velocity) => {
        return Math.abs(offset) > swipeOffsetThreshold || Math.abs(velocity) > swipeSpeedThreshold;
    };

    const reset = () => {controls.start({ x: 0, y: 0, rotate: 0 })}


    const handleDragEnd = (event, info) => {
        const swipe = isValidSwipe(info.offset.x, info.velocity.x);

        if (!swipe) {
            reset();
            return;
        }

        // Optimistic UI update
        postUpdate(id);
        
        if (swipe && info.offset.x > swipeOffsetThreshold) {
            onAccept(id)
            .then(() => postUpdate(id))
            .catch(err => reset());
        }

        if (swipe && info.offset.x < -swipeOffsetThreshold) {
            onReject(id)
            .then(() => postUpdate(id))
            .catch(err => reset());
        }
    };

    return (
        <motion.div
            className={clsx(
                "col-start-1 col-end-2 row-start-1 row-end-2",
                "bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700",
                "rounded-xl p-4 shadow-sm"
            )}
            drag="x"
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.8}
            onDragEnd={handleDragEnd}
            animate={controls}
            initial={{ scale: 1, opacity: 1 }}
            whileTap={{ scale: 1.02 }}
        >
            {children}
        </motion.div>
    );
}

export const PaperQueue = () => {
    const [papers, setPapers] = React.useState([]);

    const refreshPapers = () => {
        if (papers.length <= 5) {
            getPapers().then(newPapers => {
                setPapers(prev => [...prev, ...newPapers]);
            });
        }
    }

    React.useEffect(() => {
        refreshPapers();
    }, []);

    const handleAccept = (id) => {
        return sendPaperAction(id, "accept");
    };

    const handleReject = (id) => {
        return sendPaperAction(id, "reject");
    };

    const popPaper = (id) => {
        setPapers(prev => prev.filter(p => p.id !== id));
    }

    return (
        <div className="p-4 grid h-[100%] grid-cols-1 grid-rows-1 overflow-x-hidden">
            {[...papers].reverse().map((paper, index) => (
                <Card
                    key={index}
                    id={paper.id}
                    onAccept={handleAccept}
                    onReject={handleReject}
                    postUpdate={popPaper}
                >
                    <Paper {...paper}></Paper>
                </Card>
            ))}
        </div>
    );
};