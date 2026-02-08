import React from 'react';
import { Trash2, FileText, User, Clock } from 'lucide-react';

function History({ history, selectedId, onSelect, onDelete }) {
    return (
        <div className="flex-1 overflow-y-auto p-3">
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Recent Datasets
            </h3>
            {history.length === 0 ? (
                <p className="text-xs text-gray-500 italic">No datasets uploaded yet</p>
            ) : (
                <ul className="space-y-2">
                    {history.map((batch) => (
                        <li 
                            key={batch.id} 
                            className={`p-2.5 rounded-lg transition-all border flex items-center justify-between gap-2 ${
                                selectedId === batch.id
                                ? 'bg-blue-50 border-blue-200 shadow-sm' 
                                : 'bg-white border-gray-200 hover:bg-gray-50'
                            }`}
                        >
                            {/* Left side - Filename and metadata */}
                            <div 
                                className="flex-1 min-w-0 cursor-pointer"
                                onClick={() => onSelect(batch.id)}
                            >
                                <div className="font-medium text-xs truncate flex items-center gap-2">
                                    <FileText className="w-3.5 h-3.5 text-blue-500 shrink-0" />
                                    <span className="truncate text-slate-700">
                                        {batch.filename}
                                    </span>
                                </div>
                                <div className="text-xs text-gray-400 mt-1 ml-5 space-y-0.5">
                                    <div className="flex items-center gap-1">
                                        <Clock className="w-3 h-3" />
                                        {new Date(batch.uploaded_at).toLocaleDateString()} {new Date(batch.uploaded_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </div>
                                    {batch.uploaded_by && (
                                        <div className="flex items-center gap-1">
                                            <User className="w-3 h-3" />
                                            {batch.uploaded_by.username}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Right side - Delete button */}
                            <button
                                onClick={(e) => { 
                                    e.stopPropagation(); 
                                    onDelete && onDelete(batch.id);
                                }}
                                title="Delete dataset"
                                className="shrink-0 p-1.5 bg-red-50 hover:bg-red-100 text-red-600 rounded transition-colors"
                            >
                                <Trash2 className="w-4 h-4" />
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default History;