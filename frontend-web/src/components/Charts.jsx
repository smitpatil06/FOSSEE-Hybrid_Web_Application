import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';

function Charts({ data }) {
    if (!data || !data.type_distribution) {
        return (
            <div className="text-center py-10 text-slate-500">
                No data available for visualization
            </div>
        );
    }

    const chartData = {
        labels: Object.keys(data.type_distribution),
        datasets: [{
            label: 'Count',
            data: Object.values(data.type_distribution),
            backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'],
            borderWidth: 1
        }]
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="font-bold text-gray-700 mb-4 border-l-4 border-blue-500 pl-3">
                    Equipment Distribution
                </h3>
                <div className="h-64">
                    <Bar 
                        data={chartData} 
                        options={{ 
                            maintainAspectRatio: false,
                            responsive: true,
                            plugins: {
                                legend: {
                                    display: false
                                }
                            }
                        }} 
                    />
                </div>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="font-bold text-gray-700 mb-4 border-l-4 border-purple-500 pl-3">
                    Type Distribution
                </h3>
                <div className="h-64 flex justify-center">
                    <Pie 
                        data={chartData} 
                        options={{ 
                            maintainAspectRatio: false,
                            responsive: true
                        }} 
                    />
                </div>
            </div>
        </div>
    );
}

export default Charts;
