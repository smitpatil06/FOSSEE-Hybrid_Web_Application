import React, { useState, useEffect } from 'react';
import { Bar, Line, Pie, Doughnut, Radar, PolarArea, Scatter } from 'react-chartjs-2';
import { X, Plus, TrendingUp, BarChart3, PieChart, Activity, Target, Edit3 } from 'lucide-react';

// Professional color palettes
const COLOR_THEMES = {
    ocean: {
        name: 'Ocean',
        colors: ['#0EA5E9', '#0284C7', '#0369A1', '#075985', '#0C4A6E', '#38BDF8'],
        border: '#0C4A6E'
    },
    heatmap: {
        name: 'Heatmap',
        colors: ['#EF4444', '#F97316', '#F59E0B', '#EAB308', '#84CC16', '#22C55E'],
        border: '#DC2626'
    },
    industrial: {
        name: 'Industrial',
        colors: ['#64748B', '#475569', '#334155', '#1E293B', '#0F172A', '#94A3B8'],
        border: '#1E293B'
    },
    emerald: {
        name: 'Emerald',
        colors: ['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#34D399'],
        border: '#064E3B'
    },
    purple: {
        name: 'Purple',
        colors: ['#8B5CF6', '#7C3AED', '#6D28D9', '#5B21B6', '#4C1D95', '#A78BFA'],
        border: '#5B21B6'
    },
    neon: {
        name: 'Neon',
        colors: ['#06B6D4', '#14B8A6', '#10B981', '#84CC16', '#EAB308', '#F59E0B'],
        border: '#0891B2'
    }
};

const CHART_TYPES = [
    { id: 'bar', name: 'Bar Chart', Icon: BarChart3 },
    { id: 'line', name: 'Line Chart', Icon: TrendingUp },
    { id: 'pie', name: 'Pie Chart', Icon: PieChart },
    { id: 'doughnut', name: 'Doughnut', Icon: Target },
    { id: 'radar', name: 'Radar', Icon: Activity },
    { id: 'polar', name: 'Polar Area', Icon: Target },
    { id: 'scatter', name: 'Scatter Plot', Icon: Activity }
];

const CATEGORICAL_METRICS = [
    { id: 'type_distribution', name: 'Equipment Type Count' }
];

const CONTINUOUS_METRICS = [
    { id: 'flowrate', name: 'Flowrate' },
    { id: 'pressure', name: 'Pressure' },
    { id: 'temperature', name: 'Temperature' }
];

const SCATTER_METRICS = [
    { id: 'flowrate_vs_pressure', name: 'Flowrate vs Pressure' },
    { id: 'flowrate_vs_temperature', name: 'Flowrate vs Temperature' },
    { id: 'pressure_vs_temperature', name: 'Pressure vs Temperature' }
];

const DATA_METRICS = [
    ...CATEGORICAL_METRICS,
    ...CONTINUOUS_METRICS,
    ...SCATTER_METRICS
];

const CHART_COMPATIBILITY = {
    pie: CATEGORICAL_METRICS.map(m => m.id),
    doughnut: CATEGORICAL_METRICS.map(m => m.id),
    line: CONTINUOUS_METRICS.map(m => m.id),
    area: CONTINUOUS_METRICS.map(m => m.id),
    scatter: SCATTER_METRICS.map(m => m.id),
    bar: [...CATEGORICAL_METRICS, ...CONTINUOUS_METRICS].map(m => m.id),
    radar: CATEGORICAL_METRICS.map(m => m.id),
    polar: CATEGORICAL_METRICS.map(m => m.id)
};

const getCompatibleMetrics = (type) => {
    const allowed = CHART_COMPATIBILITY[type] || [];
    return DATA_METRICS.filter(metric => allowed.includes(metric.id));
};

const normalizeMetric = (type, metric) => {
    const allowed = CHART_COMPATIBILITY[type] || [];
    if (!allowed.length) return metric;
    if (!allowed.includes(metric)) return allowed[0];
    return metric;
};

const DEFAULT_WIDGETS = [
    { id: 1, title: 'Equipment Type Distribution', metric: 'type_distribution', type: 'bar', theme: 'ocean' },
    { id: 2, title: 'Type Breakdown', metric: 'type_distribution', type: 'doughnut', theme: 'emerald' },
    { id: 3, title: 'Pressure Analysis', metric: 'pressure', type: 'line', theme: 'heatmap' },
    { id: 4, title: 'Multi-Metric Radar', metric: 'type_distribution', type: 'radar', theme: 'purple' }
];

const STORAGE_KEY = 'clw_widget_config';

function Charts({ data, onConfigChange }) {
    const [widgets, setWidgets] = useState(DEFAULT_WIDGETS);
    const [nextId, setNextId] = useState(5);
    const [showAddModal, setShowAddModal] = useState(false);
    const [editingWidget, setEditingWidget] = useState(null);

    useEffect(() => {
        try {
            const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
            if (Array.isArray(saved) && saved.length) {
                setWidgets(saved);
                const maxId = saved.reduce((acc, item) => Math.max(acc, item.id || 0), 0);
                setNextId(maxId + 1);
            }
        } catch (error) {
            console.warn('Failed to restore widget config:', error);
        }
    }, []);

    useEffect(() => {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(widgets));
        } catch (error) {
            console.warn('Failed to persist widget config:', error);
        }
    }, [widgets]);

    useEffect(() => {
        if (!onConfigChange) return;
        const normalized = widgets.map(widget => {
            const theme = COLOR_THEMES[widget.theme];
            const type = widget.type;
            const color = ['pie', 'doughnut'].includes(type) ? 'multi' : (theme?.colors?.[0] || '#3B82F6');
            return {
                type,
                metric: widget.metric,
                title: widget.title,
                color
            };
        });
        onConfigChange(normalized);
    }, [widgets, onConfigChange]);


    if (!data || !data.type_distribution) {
        return (
            <div className="text-center py-10 text-slate-500 bg-white rounded-lg border border-gray-200">
                <Activity className="w-16 h-16 text-gray-300 mx-auto mb-3" />
                <p className="font-medium text-sm">No data available for visualization</p>
            </div>
        );
    }

    const addWidget = (config) => {
        const newWidget = {
            id: nextId,
            ...config
        };
        setWidgets([...widgets, newWidget]);
        setNextId(nextId + 1);
        setShowAddModal(false);
    };

    const updateWidget = (id, updates) => {
        setWidgets(widgets.map(widget => 
            widget.id === id ? { ...widget, ...updates } : widget
        ));
        setEditingWidget(null);
    };

    const removeWidget = (id) => {
        if (widgets.length <= 1) {
            alert('You must keep at least one widget');
            return;
        }
        setWidgets(widgets.filter(widget => widget.id !== id));
    };

    return (
        <div className="space-y-3">
            {/* Control Panel */}
            <div className="bg-linear-to-r from-slate-900 to-slate-800 text-white rounded-lg p-3 flex items-center justify-between shadow-xl border border-slate-700">
                <div className="flex items-center gap-3">
                    <div className="bg-blue-600 p-2 rounded-lg">
                        <BarChart3 className="w-5 h-5" />
                    </div>
                    <div>
                        <h2 className="font-bold text-base">Analytics Dashboard</h2>
                        <p className="text-xs text-slate-300">{widgets.length} Active Widget{widgets.length !== 1 ? 's' : ''} • Real-time Data</p>
                    </div>
                </div>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium text-sm transition-all shadow-lg hover:shadow-xl"
                >
                    <Plus className="w-4 h-4" />
                    Add Widget
                </button>
            </div>

            {/* Widgets Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                {widgets.map(widget => (
                    <WidgetCard
                        key={widget.id}
                        widget={widget}
                        data={data}
                        onUpdate={(updates) => updateWidget(widget.id, updates)}
                        onRemove={() => removeWidget(widget.id)}
                        onEdit={() => setEditingWidget(widget)}
                    />
                ))}
            </div>

            {/* Add Widget Modal */}
            {showAddModal && (
                <AddWidgetModal
                    onClose={() => setShowAddModal(false)}
                    onAdd={addWidget}
                />
            )}

            {/* Edit Widget Modal */}
            {editingWidget && (
                <EditWidgetModal
                    widget={editingWidget}
                    onClose={() => setEditingWidget(null)}
                    onSave={(updates) => updateWidget(editingWidget.id, updates)}
                />
            )}
        </div>
    );
}

// Helper function to prepare chart data based on metric
function prepareChartData(data, metric, theme) {
    const themeColors = COLOR_THEMES[theme];

    if (metric.includes('_vs_')) {
        const [xMetric, yMetric] = metric.split('_vs_');
        const scatterData = data.data.slice(0, 50).map(item => ({
            x: parseFloat(item[xMetric]) || 0,
            y: parseFloat(item[yMetric]) || 0
        }));
        return {
            labels: [`${xMetric} vs ${yMetric}`],
            datasets: [{
                label: `${xMetric} vs ${yMetric}`,
                data: scatterData,
                backgroundColor: themeColors.colors[0] + 'cc',
                borderColor: themeColors.border,
                borderWidth: 1,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        };
    }
    
    switch (metric) {
        case 'type_distribution':
            return {
                labels: Object.keys(data.type_distribution),
                datasets: [{
                    label: 'Equipment Count',
                    data: Object.values(data.type_distribution),
                    backgroundColor: themeColors.colors,
                    borderColor: themeColors.border,
                    borderWidth: 2
                }]
            };
        
        case 'flowrate':
        case 'pressure':
        case 'temperature':
            const values = data.data.map(item => item[metric]);
            const labels = data.data.map((_, idx) => `Unit ${idx + 1}`);
            return {
                labels: labels.slice(0, 20), // Limit to 20 for readability
                datasets: [{
                    label: metric.charAt(0).toUpperCase() + metric.slice(1),
                    data: values.slice(0, 20),
                    backgroundColor: themeColors.colors[0] + '80',
                    borderColor: themeColors.border,
                    borderWidth: 2,
                    fill: true
                }]
            };
        
        default:
            return { labels: [], datasets: [] };
    }
}

// Widget Card Component
function WidgetCard({ widget, data, onUpdate, onRemove, onEdit }) {
    try {
        const theme = COLOR_THEMES[widget.theme];
        const chartData = prepareChartData(data, widget.metric, widget.theme);

        if (!chartData || !chartData.datasets) {
            return (
                <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
                    <p className="text-gray-500 text-sm">Unable to prepare data for this chart</p>
                </div>
            );
        }

    const chartOptions = {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
            legend: {
                display: ['pie', 'doughnut', 'polar', 'radar'].includes(widget.type),
                position: 'bottom',
                labels: {
                    boxWidth: 10,
                    padding: 6,
                    font: { size: 9 }
                }
            },
            tooltip: {
                titleFont: { size: 11 },
                bodyFont: { size: 10 }
            }
        },
        scales: ['bar', 'line', 'radar'].includes(widget.type) ? {
            y: {
                beginAtZero: true,
                ticks: { font: { size: 9 } }
            },
            x: {
                ticks: { font: { size: 9 }, maxRotation: 45 }
            }
        } : (widget.type === 'scatter' ? (() => {
            const [xMetric, yMetric] = widget.metric.split('_vs_');
            return {
                x: {
                    title: { display: true, text: xMetric || 'X', font: { size: 10 } },
                    ticks: { font: { size: 9 } }
                },
                y: {
                    title: { display: true, text: yMetric || 'Y', font: { size: 10 } },
                    ticks: { font: { size: 9 } }
                }
            };
        })() : {})
    };

    const renderChart = () => {
        switch (widget.type) {
            case 'bar':
                return <Bar data={chartData} options={chartOptions} />;
            case 'line':
                return <Line data={chartData} options={chartOptions} />;
            case 'pie':
                return <Pie data={chartData} options={chartOptions} />;
            case 'doughnut':
                return <Doughnut data={chartData} options={chartOptions} />;
            case 'radar':
                return <Radar data={chartData} options={chartOptions} />;
            case 'polar':
                return <PolarArea data={chartData} options={chartOptions} />;
            case 'scatter':
                return <Scatter data={chartData} options={chartOptions} />;
            default:
                return null;
        }
    };

    return (
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-lg transition-shadow">
            {/* Widget Header */}
            <div className="px-3 py-2 border-b border-gray-100 flex items-center justify-between bg-linear-to-r from-slate-50 to-gray-50">
                <h3 className="text-xs font-semibold text-slate-700 truncate flex-1">{widget.title}</h3>
                <div className="flex items-center gap-1">
                    <button
                        onClick={onEdit}
                        className="p-1 hover:bg-blue-100 text-blue-600 rounded transition-colors"
                        title="Edit Widget"
                    >
                        <Edit3 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={onRemove}
                        className="p-1 hover:bg-red-100 text-red-600 rounded transition-colors"
                        title="Remove Widget"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Chart Canvas */}
            <div className="p-3" style={{ height: '220px' }}>
                {renderChart()}
            </div>

            {/* Widget Footer */}
            <div className="px-3 py-1.5 bg-slate-50 border-t border-gray-100 flex items-center justify-between text-xs">
                <span className="text-slate-500 font-medium">{DATA_METRICS.find(m => m.id === widget.metric)?.name}</span>
                <span className="text-slate-400">{COLOR_THEMES[widget.theme].name}</span>
            </div>
        </div>
    );
    } catch (error) {
        console.error('Error rendering widget:', error);
        return (
            <div className="bg-white rounded-lg border border-red-200 shadow-sm p-6">
                <p className="text-red-600 text-sm font-medium">Chart rendering error</p>
                <p className="text-red-500 text-xs mt-1">{error.message}</p>
            </div>
        );
    }
}

// Add Widget Modal
function AddWidgetModal({ onClose, onAdd }) {
    const [config, setConfig] = useState({
        title: '',
        metric: 'type_distribution',
        type: 'bar',
        theme: 'ocean',
        xMetric: 'flowrate',
        yMetric: 'pressure'
    });

    const compatibleMetrics = getCompatibleMetrics(config.type);

    const handleTypeChange = (type) => {
        if (type === 'scatter') {
            const scatterMetric = `${config.xMetric}_vs_${config.yMetric}`;
            setConfig({ ...config, type, metric: scatterMetric });
            return;
        }
        const normalizedMetric = normalizeMetric(type, config.metric);
        setConfig({ ...config, type, metric: normalizedMetric });
    };

    const handleScatterMetricChange = (axis, value) => {
        const next = { ...config, [axis]: value };
        next.metric = `${next.xMetric}_vs_${next.yMetric}`;
        setConfig(next);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!config.title.trim()) {
            alert('Please enter a widget title');
            return;
        }
        onAdd(config);
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full">
                <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-linear-to-r from-blue-600 to-blue-700 text-white rounded-t-xl">
                    <h2 className="text-lg font-bold">Add New Widget</h2>
                    <button onClick={onClose} className="p-1 hover:bg-white hover:bg-opacity-20 rounded">
                        <X className="w-5 h-5" />
                    </button>
                </div>
                
                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {/* Title */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Widget Title</label>
                        <input
                            type="text"
                            value={config.title}
                            onChange={(e) => setConfig({ ...config, title: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                            placeholder="Enter widget title..."
                            required
                        />
                    </div>

                    {/* Data Metric */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Data Metric</label>
                        {config.type === 'scatter' ? (
                            <div className="grid grid-cols-2 gap-2">
                                <select
                                    value={config.xMetric}
                                    onChange={(e) => handleScatterMetricChange('xMetric', e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                                >
                                    {CONTINUOUS_METRICS.map(metric => (
                                        <option key={metric.id} value={metric.id}>{metric.name}</option>
                                    ))}
                                </select>
                                <select
                                    value={config.yMetric}
                                    onChange={(e) => handleScatterMetricChange('yMetric', e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                                >
                                    {CONTINUOUS_METRICS.map(metric => (
                                        <option key={metric.id} value={metric.id}>{metric.name}</option>
                                    ))}
                                </select>
                            </div>
                        ) : (
                            <select
                                value={config.metric}
                                onChange={(e) => setConfig({ ...config, metric: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                            >
                                {compatibleMetrics.map(metric => (
                                    <option key={metric.id} value={metric.id}>{metric.name}</option>
                                ))}
                            </select>
                        )}
                    </div>

                    {/* Chart Type */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Chart Type</label>
                        <div className="grid grid-cols-4 gap-2">
                            {CHART_TYPES.map(({ id, name, Icon }) => (
                                <button
                                    key={id}
                                    type="button"
                                    onClick={() => handleTypeChange(id)}
                                    className={`p-2 rounded-lg border-2 transition-all flex flex-col items-center gap-1 ${
                                        config.type === id
                                            ? 'border-blue-600 bg-blue-50'
                                            : 'border-gray-200 hover:border-blue-300'
                                    }`}
                                >
                                    <Icon className="w-5 h-5" />
                                    <span className="text-xs font-medium">{id}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Color Theme */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Color Theme</label>
                        <div className="grid grid-cols-3 gap-2">
                            {Object.entries(COLOR_THEMES).map(([key, theme]) => (
                                <button
                                    key={key}
                                    type="button"
                                    onClick={() => setConfig({ ...config, theme: key })}
                                    className={`px-3 py-2 rounded-lg border-2 transition-all text-xs font-medium ${
                                        config.theme === key
                                            ? 'border-slate-800 bg-slate-100'
                                            : 'border-gray-200 hover:border-slate-400'
                                    }`}
                                    style={{ 
                                        backgroundColor: config.theme === key ? theme.colors[0] + '20' : undefined,
                                        borderColor: config.theme === key ? theme.border : undefined
                                    }}
                                >
                                    {theme.name}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium text-sm"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm"
                        >
                            Add Widget
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

// Edit Widget Modal
function EditWidgetModal({ widget, onClose, onSave }) {
    const [xDefault, yDefault] = widget.metric.includes('_vs_')
        ? widget.metric.split('_vs_')
        : ['flowrate', 'pressure'];
    const [config, setConfig] = useState({
        title: widget.title,
        metric: widget.metric,
        type: widget.type,
        theme: widget.theme,
        xMetric: xDefault,
        yMetric: yDefault
    });

    const compatibleMetrics = getCompatibleMetrics(config.type);

    const handleTypeChange = (type) => {
        if (type === 'scatter') {
            const scatterMetric = `${config.xMetric}_vs_${config.yMetric}`;
            setConfig({ ...config, type, metric: scatterMetric });
            return;
        }
        const normalizedMetric = normalizeMetric(type, config.metric);
        setConfig({ ...config, type, metric: normalizedMetric });
    };

    const handleScatterMetricChange = (axis, value) => {
        const next = { ...config, [axis]: value };
        next.metric = `${next.xMetric}_vs_${next.yMetric}`;
        setConfig(next);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!config.title.trim()) {
            alert('Please enter a widget title');
            return;
        }
        onSave(config);
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full">
                <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-linear-to-r from-slate-700 to-slate-800 text-white rounded-t-xl">
                    <h2 className="text-lg font-bold">Edit Widget</h2>
                    <button onClick={onClose} className="p-1 hover:bg-white hover:bg-opacity-20 rounded">
                        <X className="w-5 h-5" />
                    </button>
                </div>
                
                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {/* Title */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Widget Title</label>
                        <input
                            type="text"
                            value={config.title}
                            onChange={(e) => setConfig({ ...config, title: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                            required
                        />
                    </div>

                    {/* Data Metric */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Data Metric</label>
                        {config.type === 'scatter' ? (
                            <div className="grid grid-cols-2 gap-2">
                                <select
                                    value={config.xMetric}
                                    onChange={(e) => handleScatterMetricChange('xMetric', e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                                >
                                    {CONTINUOUS_METRICS.map(metric => (
                                        <option key={metric.id} value={metric.id}>{metric.name}</option>
                                    ))}
                                </select>
                                <select
                                    value={config.yMetric}
                                    onChange={(e) => handleScatterMetricChange('yMetric', e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                                >
                                    {CONTINUOUS_METRICS.map(metric => (
                                        <option key={metric.id} value={metric.id}>{metric.name}</option>
                                    ))}
                                </select>
                            </div>
                        ) : (
                            <select
                                value={config.metric}
                                onChange={(e) => setConfig({ ...config, metric: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                            >
                                {compatibleMetrics.map(metric => (
                                    <option key={metric.id} value={metric.id}>{metric.name}</option>
                                ))}
                            </select>
                        )}
                    </div>

                    {/* Chart Type */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Chart Type</label>
                        <div className="grid grid-cols-4 gap-2">
                            {CHART_TYPES.map(({ id, name, Icon }) => (
                                <button
                                    key={id}
                                    type="button"
                                    onClick={() => handleTypeChange(id)}
                                    className={`p-2 rounded-lg border-2 transition-all flex flex-col items-center gap-1 ${
                                        config.type === id
                                            ? 'border-blue-600 bg-blue-50'
                                            : 'border-gray-200 hover:border-blue-300'
                                    }`}
                                >
                                    <Icon className="w-5 h-5" />
                                    <span className="text-xs font-medium">{id}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Color Theme */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Color Theme</label>
                        <div className="grid grid-cols-3 gap-2">
                            {Object.entries(COLOR_THEMES).map(([key, theme]) => (
                                <button
                                    key={key}
                                    type="button"
                                    onClick={() => setConfig({ ...config, theme: key })}
                                    className={`px-3 py-2 rounded-lg border-2 transition-all text-xs font-medium ${
                                        config.theme === key
                                            ? 'border-slate-800 bg-slate-100'
                                            : 'border-gray-200 hover:border-slate-400'
                                    }`}
                                    style={{ 
                                        backgroundColor: config.theme === key ? theme.colors[0] + '20' : undefined,
                                        borderColor: config.theme === key ? theme.border : undefined
                                    }}
                                >
                                    {theme.name}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium text-sm"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="flex-1 px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-800 font-medium text-sm"
                        >
                            Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Charts;
