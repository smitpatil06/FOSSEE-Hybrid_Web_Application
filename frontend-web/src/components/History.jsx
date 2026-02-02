import React from 'react';

function History({ history, selectedId, onSelect, onDelete }) {
    return (
        <div className="flex-1 overflow-y-auto p-4">
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Recent Datasets
            </h3>
            {history.length === 0 ? (
                <p className="text-sm text-gray-500 italic">No datasets uploaded yet</p>
            ) : (
                <ul className="space-y-2">
                    {history.map((batch) => (
                        <li 
                            key={batch.id} 
                            className={`p-3 rounded-lg transition-all border flex items-start justify-between ${
                                selectedId === batch.id
                                ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-sm' 
                                : 'bg-white border-transparent hover:bg-gray-50 hover:border-gray-200'
                            }`}
                        >
                            <div className="flex-1 cursor-pointer" onClick={() => onSelect(batch.id)}>
                                <div className="font-medium text-sm truncate flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-green-400"></span>
                                    {batch.filename}
                                </div>
                                <div className="text-xs text-gray-400 pl-4 mt-1">
                                    {new Date(batch.uploaded_at).toLocaleString()}
                                </div>
                                {batch.uploaded_by && (
                                    <div className="text-xs text-gray-500 pl-4 mt-1">
                                        By: {batch.uploaded_by.username}
                                    </div>
                                )}
                            </div>

                            <div className="ml-3 flex-shrink-0 self-start">
                                <button
                                    onClick={(e) => { e.stopPropagation(); onDelete && onDelete(batch.id); }}
                                    title="Delete dataset"
                                    className="inline-flex items-center px-2 py-1 bg-red-50 hover:bg-red-100 text-red-600 rounded text-xs font-medium border border-red-100"
                                >
                                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    Delete
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default History;
