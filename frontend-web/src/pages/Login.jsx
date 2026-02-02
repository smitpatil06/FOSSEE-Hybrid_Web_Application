import React, { useState } from 'react';
import { auth } from '../api';

function Login({ onLoginSuccess }) {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                const response = await auth.login(formData.username, formData.password);
                onLoginSuccess(response.user);
            } else {
                const response = await auth.register(formData);
                onLoginSuccess(response.user);
            }
        } catch (err) {
            setError(err.response?.data?.error || err.response?.data?.username || 'Authentication failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-slate-100 flex items-center justify-center p-4">
            <div className="max-w-md w-full">
                {/* Logo and Title */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
                        <span className="text-white text-2xl font-bold">C</span>
                    </div>
                    <h1 className="text-3xl font-bold text-slate-800">ChemViz</h1>
                    <p className="text-slate-600 mt-2">Chemical Equipment Analytics</p>
                    <p className="text-sm text-slate-500 mt-1">FOSSEE Project</p>
                </div>

                {/* Login/Register Form */}
                <div className="bg-white rounded-xl shadow-lg p-8">
                    <div className="flex mb-6 border-b">
                        <button
                            className={`flex-1 pb-3 text-center font-medium transition-colors ${
                                isLogin 
                                ? 'text-blue-600 border-b-2 border-blue-600' 
                                : 'text-slate-400 hover:text-slate-600'
                            }`}
                            onClick={() => setIsLogin(true)}
                        >
                            Login
                        </button>
                        <button
                            className={`flex-1 pb-3 text-center font-medium transition-colors ${
                                !isLogin 
                                ? 'text-blue-600 border-b-2 border-blue-600' 
                                : 'text-slate-400 hover:text-slate-600'
                            }`}
                            onClick={() => setIsLogin(false)}
                        >
                            Register
                        </button>
                    </div>

                    {error && (
                        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                Username
                            </label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Enter username"
                            />
                        </div>

                        {!isLogin && (
                            <>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="Enter email"
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-1">
                                            First Name
                                        </label>
                                        <input
                                            type="text"
                                            name="first_name"
                                            value={formData.first_name}
                                            onChange={handleChange}
                                            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-1">
                                            Last Name
                                        </label>
                                        <input
                                            type="text"
                                            name="last_name"
                                            value={formData.last_name}
                                            onChange={handleChange}
                                            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        />
                                    </div>
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                Password
                            </label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                                minLength={6}
                                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Enter password"
                            />
                            {!isLogin && (
                                <p className="mt-1 text-xs text-slate-500">Minimum 6 characters</p>
                            )}
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Please wait...' : isLogin ? 'Login' : 'Register'}
                        </button>
                    </form>

                    <div className="mt-6 text-center text-sm text-slate-500">
                        {isLogin ? "Don't have an account? " : "Already have an account? "}
                        <button
                            onClick={() => setIsLogin(!isLogin)}
                            className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                            {isLogin ? 'Register here' : 'Login here'}
                        </button>
                    </div>
                </div>

                {/* Demo Credentials */}
                <div className="mt-4 p-4 bg-slate-100 rounded-lg text-center text-sm text-slate-600">
                    <p className="font-medium mb-1">Demo Credentials (if available):</p>
                    <p>Username: demo | Password: demo123</p>
                </div>
            </div>
        </div>
    );
}

export default Login;
