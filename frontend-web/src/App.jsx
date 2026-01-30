import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const API_URL = 'http://127.0.0.1:8000/api';

function App() {
    const [history, setHistory] = useState([]);
    const [selectedData, setSelectedData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => { fetchHistory(); }, []);

    const fetchHistory = async () => {
        try {
            const res = await axios.get(`${API_URL}/history/`);
            setHistory(res.data);
            if (res.data.length > 0) handleLoadBatch(res.data[0].id);
        } catch (err) { console.error(err); }
    };

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        setLoading(true);
        try {
            await axios.post(`${API_URL}/upload/`, formData);
            alert("Upload Successful!");
            fetchHistory();
        } catch (error) { alert("Upload Failed"); }
        setLoading(false);
    };

    const handleLoadBatch = async (id) => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_URL}/summary/${id}/`);
            setSelectedData(res.data);
        } catch (error) { console.error(error); }
        setLoading(false);
    };

    return (
        <div className="flex h-screen bg-gray-50 font-sans">
            {/* Sidebar */}
            <div className="w-64 bg-white shadow-lg p-5 flex flex-col">
                <h2 className="text-xl font-bold text-blue-600 mb-6">⚗️ ChemViz</h2>
                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Upload CSV</label>
                    <input type="file" onChange={handleUpload} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"/>
                </div>
                <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">History</h3>
                <ul className="flex-1 overflow-y-auto space-y-2">
                    {history.map((batch) => (
                        <li key={batch.id} onClick={() => handleLoadBatch(batch.id)} 
                            className={`p-3 rounded cursor-pointer transition-colors ${selectedData?.filename === batch.filename ? 'bg-blue-50 text-blue-700 border-l-4 border-blue-500' : 'hover:bg-gray-100'}`}>
                            <div className="font-medium truncate">{batch.filename}</div>
                            <div className="text-xs text-gray-500">{new Date(batch.uploaded_at).toLocaleDateString()}</div>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Main Content */}
            <div className="flex-1 p-8 overflow-y-auto">
                {selectedData && !loading ? (
                    <div className="max-w-6xl mx-auto space-y-6">
                      <header className="flex justify-between items-center">
    <h1 className="text-2xl font-bold text-gray-800">{selectedData.filename}</h1>
    
    {/* PDF Download Button */}
    <a 
        href={`${API_URL}/report/${selectedData.id}/`}
        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg shadow-md text-sm font-bold transition-colors flex items-center gap-2"
        download
    >
        <span>📄</span> Download Report
    </a>
</header> 

                        {/* Stats Cards */}
                        <div className="grid grid-cols-3 gap-6">
                            <Card title="Total Count" value={selectedData.summary.total_count} color="text-blue-600" />
                            <Card title="Avg Flowrate" value={selectedData.summary.avg_flow?.toFixed(1)} color="text-emerald-600" />
                            <Card title="Avg Pressure" value={selectedData.summary.avg_press?.toFixed(1)} color="text-amber-600" />
                        </div>

                        {/* Charts */}
                        <div className="grid grid-cols-2 gap-6">
                            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80">
                                <h3 className="font-semibold text-gray-700 mb-4">Equipment Distribution</h3>
                                <Bar data={{
                                    labels: Object.keys(selectedData.type_distribution),
                                    datasets: [{ label: 'Count', data: Object.values(selectedData.type_distribution), backgroundColor: '#3B82F6' }]
                                }} options={{ maintainAspectRatio: false }} />
                            </div>
                            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80 flex justify-center">
                                <Pie data={{
                                    labels: Object.keys(selectedData.type_distribution),
                                    datasets: [{ data: Object.values(selectedData.type_distribution), backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'] }]
                                }} options={{ maintainAspectRatio: false }} />
                            </div>
                        </div>

                        {/* Table */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                             <table className="w-full text-sm text-left text-gray-500">
                                <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3">Name</th>
                                        <th className="px-6 py-3">Type</th>
                                        <th className="px-6 py-3">Flowrate</th>
                                        <th className="px-6 py-3">Pressure</th>
                                        <th className="px-6 py-3">Temp</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {selectedData.data.map((row, idx) => (
                                        <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                            <td className="px-6 py-4 font-medium text-gray-900">{row.equipment_name}</td>
                                            <td className="px-6 py-4">{row.equipment_type}</td>
                                            <td className="px-6 py-4">{row.flowrate}</td>
                                            <td className="px-6 py-4">{row.pressure}</td>
                                            <td className="px-6 py-4">{row.temperature}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) : (
                    <div className="h-full flex items-center justify-center text-gray-400">Select a file to view data</div>
                )}
            </div>
        </div>
    );
}

const Card = ({ title, value, color }) => (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p className="text-gray-500 text-sm font-medium uppercase">{title}</p>
        <h3 className={`text-3xl font-bold mt-2 ${color}`}>{value}</h3>
    </div>
);

export default App;