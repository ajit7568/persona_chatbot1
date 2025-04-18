import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Chat from './components/Chat';
import Auth from './components/Auth';
import { getToken } from './services/auth';
import './index.css';

// Protected Route wrapper component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const token = getToken();
    if (!token) {
        return <Navigate to="/login" replace />;
    }
    return <>{children}</>;
};

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <div className="min-h-screen bg-gray-900">
                <Routes>
                    <Route path="/login" element={<Auth mode="login" />} />
                    <Route path="/register" element={<Auth mode="register" />} />
                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <Chat />
                            </ProtectedRoute>
                        }
                    />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </div>
        </BrowserRouter>
    );
};

export default App;