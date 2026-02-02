import React, { useState, useEffect } from 'react';
import api, { data as dataAPI, auth } from '../api';
import Charts from '../components/Charts';
import History from '../components/History';

function Upload({ user, onLogout }) {
    const [history, setHistory] = useState([]);
    const [selectedData, setSelectedData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const res = await dataAPI.getHistory();
            setHistory(res);
            if (res.length > 0) {
                handleLoadBatch(res[0].id);
            }
        } catch (err) {
            console.error('Error fetching history:', err);
        }
    };

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        setLoading(true);
        try {
            await dataAPI.uploadFile(file);
            alert("Dataset uploaded successfully!");
            fetchHistory();
        } catch (error) {
            alert(error.response?.data?.error || "Upload Failed. Please check CSV format.");
        }
        setLoading(false);
    };

    const handleLoadBatch = async (id) => {
        setLoading(true);
        try {
            const res = await dataAPI.getSummary(id);
            setSelectedData(res);
        } catch (error) {
            console.error('Error loading batch:', error);
            alert('Failed to load dataset');
        }
        setLoading(false);
    };

    const handleLogout = async () => {
        await auth.logout();
        onLogout();
    };

    const handleDeleteBatch = async (id) => {
        if (!window.confirm('Delete this dataset? This action cannot be undone.')) return;
        setLoading(true);
        try {
            await api.delete(`/summary/${id}/`);
            // If deleted item was selected, clear selection
            if (selectedData?.id === id) setSelectedData(null);
            await fetchHistory();
            alert('Dataset deleted successfully');
        } catch (error) {
            console.error('Delete error:', error);
            alert(error.response?.data?.detail || 'Failed to delete dataset');
        }
        setLoading(false);
    };

    const handleDownloadReport = async () => {
        if (!selectedData) return;
        try {
            await dataAPI.downloadReport(selectedData.id, selectedData.filename);
        } catch (error) {
            console.error('Download error:', error);
            alert(error.message || 'Failed to download PDF report');
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50 font-sans text-slate-800">
            {/* Navbar */}
            <nav className="bg-slate-900 text-white shadow-lg z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-3">
                            <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center font-bold text-xs">C</div>
                            <div>
                                <span className="font-bold text-xl tracking-tight">ChemViz</span>
                                <span className="ml-2 text-xs bg-blue-700 px-2 py-0.5 rounded text-blue-100">FOSSEE</span>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="text-sm">
                                Welcome, <span className="font-semibold">{user?.username}</span>
                            </span>
                            <button
                                onClick={handleLogout}
                                className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-sm font-medium transition-colors"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            <div className="flex flex-1 overflow-hidden">
                {/* Sidebar */}
                <div className="w-72 bg-white border-r border-gray-200 flex flex-col shadow-sm">
                    <div className="p-6 border-b border-gray-100 bg-gray-50">
                        <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">
                            Data Management
                        </h2>
                        <label className="flex flex-col w-full h-32 border-2 border-dashed border-blue-300 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors">
                            <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                <svg className="w-8 h-8 text-blue-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                                </svg>
                                <p className="mb-1 text-sm text-gray-500 font-semibold">Click to upload CSV</p>
                                <p className="text-xs text-gray-400">Chemical Params only</p>
                            </div>
                            <input type="file" onChange={handleUpload} accept=".csv" className="hidden" />
                        </label>
                    </div>

                    <History 
                        history={history} 
                        selectedId={selectedData?.id}
                        onSelect={handleLoadBatch}
                        onDelete={handleDeleteBatch}
                    />
                </div>

                {/* Main Dashboard */}
                <main className="flex-1 overflow-y-auto bg-gray-50 p-8">
                    {loading && (
                        <div className="text-center py-10 text-blue-600 font-medium animate-pulse">
                            Processing Analytical Data...
                        </div>
                    )}

                    {selectedData && !loading ? (
                        <div className="max-w-6xl mx-auto space-y-6 animate-fade-in-up">
                            {/* Header */}
                            <header className="flex justify-between items-end pb-6 border-b border-gray-200">
                                <div>
                                    <h1 className="text-3xl font-bold text-slate-800">{selectedData.filename}</h1>
                                    <p className="text-slate-500 mt-1">Chemical Equipment Parameter Analysis</p>
                                </div>
                                <button 
                                    onClick={handleDownloadReport}
                                    className="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-md shadow-sm transition-colors"
                                >
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    Download PDF Report
                                </button>
                            </header>

                            {/* KPI Grid */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <StatCard label="Total Equipment Units" value={selectedData.summary.total_count} sub="units detected" />
                                <StatCard label="Average Flowrate" value={selectedData.summary.avg_flow?.toFixed(2)} sub="m³/hr" />
                                <StatCard label="Average Pressure" value={selectedData.summary.avg_press?.toFixed(2)} sub="bar (g)" />
                            </div>

                            {/* Visualization */}
                            <Charts data={selectedData} />

                            {/* Data Table */}
                            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                                <div className="px-6 py-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                                    <h3 className="font-bold text-gray-700">Raw Parameter Logs</h3>
                                    <span className="text-xs text-gray-400 italic">Showing all records</span>
                                </div>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-sm text-left text-gray-600">
                                        <thead className="text-xs text-gray-500 uppercase bg-gray-100">
                                            <tr>
                                                <th className="px-6 py-3">Equipment Name</th>
                                                <th className="px-6 py-3">Type</th>
                                                <th className="px-6 py-3 text-right">Flowrate</th>
                                                <th className="px-6 py-3 text-right">Pressure</th>
                                                <th className="px-6 py-3 text-right">Temperature</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {selectedData.data.map((row, idx) => (
                                                <tr key={idx} className="hover:bg-blue-50/50 transition-colors">
                                                    <td className="px-6 py-3 font-medium text-gray-900">{row.equipment_name}</td>
                                                    <td className="px-6 py-3">
                                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                            {row.equipment_type}
                                                        </span>
                                                    </td>
                                                    <td className="px-6 py-3 text-right font-mono">{row.flowrate}</td>
                                                    <td className="px-6 py-3 text-right font-mono">{row.pressure}</td>
                                                    <td className="px-6 py-3 text-right font-mono">{row.temperature}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    ) : !loading && (
                        /* Empty State */
                        <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
                            <div className="p-4 bg-blue-100 rounded-full">
                                <svg className="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
                                </svg>
                            </div>
                            <h2 className="text-2xl font-bold text-gray-800">Welcome to ChemViz</h2>
                            <p className="text-gray-500 max-w-md">
                                Upload a CSV file containing equipment parameters to generate visualizations and PDF reports.
                            </p>
                            <div className="text-sm text-gray-400 bg-white p-4 rounded-lg border border-gray-200 shadow-sm mt-4">
                                <strong>Required CSV Columns:</strong><br/>
                                Equipment Name, Type, Flowrate, Pressure, Temperature
                            </div>
                        </div>
                    )}
                </main>
            </div>
            
            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 py-3 text-center text-xs text-gray-400">
                <p>&copy; 2026 ChemViz Analytics. Developed for FOSSEE Screening Task.</p>
            </footer>
        </div>
    );
}

// Helper Component
const StatCard = ({ label, value, sub }) => (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
        <p className="text-xs font-bold text-gray-400 uppercase tracking-wide">{label}</p>
        <div className="flex items-baseline mt-2">
            <h3 className="text-3xl font-bold text-slate-800">{value}</h3>
            {sub && <span className="ml-2 text-sm text-gray-500">{sub}</span>}
        </div>
    </div>
);

export default Upload;
