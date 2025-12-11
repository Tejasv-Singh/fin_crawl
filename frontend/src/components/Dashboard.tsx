import { useEffect, useState } from 'react';
import axios from 'axios';
import { AlertCircle, FileText, CheckCircle, Search } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface Document {
    id: number;
    title: string;
    source: string;
    url: string;
    risk_score: number;
    status: string;
    published_date: string;
}

const BASE_URL = 'http://localhost:8001/api/v1';

export function Dashboard() {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const res = await axios.get(`${BASE_URL}/documents`);
            setDocuments(res.data);
        } catch (error) {
            console.error("Failed to fetch documents", error);
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (score: number) => {
        if (score >= 75) return "text-red-600 bg-red-50";
        if (score >= 50) return "text-orange-600 bg-orange-50";
        return "text-green-600 bg-green-50";
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-7xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 tracking-tight">FINCRAWL <span className="text-blue-600 text-lg align-top">Early-Warning System</span></h1>
                    <p className="text-gray-500 mt-2">Autonomous Risk Monitoring & Signal Detection</p>
                </header>

                {/* Stats Row */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <h3 className="text-gray-500 text-sm font-medium">Total Documents</h3>
                        <p className="text-3xl font-bold text-gray-900 mt-2">{documents.length}</p>
                    </div>
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <h3 className="text-gray-500 text-sm font-medium">High Risk Flags</h3>
                        <p className="text-3xl font-bold text-red-600 mt-2">
                            {documents.filter(d => d.risk_score >= 75).length}
                        </p>
                    </div>
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <h3 className="text-gray-500 text-sm font-medium">Recent Activity</h3>
                        <p className="text-3xl font-bold text-blue-600 mt-2">24h</p>
                    </div>
                </div>

                {/* Main Table */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                        <h2 className="text-lg font-semibold text-gray-900">Risk Feed</h2>
                        <button onClick={fetchDocuments} className="text-sm text-blue-600 hover:text-blue-700 font-medium">Refresh</button>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="bg-gray-50 border-b border-gray-100">
                                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase">Risk Score</th>
                                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase">Document</th>
                                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase">Source</th>
                                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase">Status</th>
                                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase">Date</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-100">
                                {documents.map((doc) => (
                                    <tr key={doc.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="p-4">
                                            <span className={clsx("px-3 py-1 rounded-full text-sm font-bold", getRiskColor(doc.risk_score))}>
                                                {doc.risk_score}
                                            </span>
                                        </td>
                                        <td className="p-4">
                                            <div className="font-medium text-gray-900">{doc.title}</div>
                                            <a href={doc.url} target="_blank" className="text-xs text-blue-500 hover:underline truncate block max-w-xs">{doc.url}</a>
                                        </td>
                                        <td className="p-4 text-sm text-gray-600">{doc.source}</td>
                                        <td className="p-4">
                                            <span className={clsx("flex items-center gap-1.5 text-xs font-medium",
                                                doc.status === 'EMBEDDED' ? 'text-green-600' : 'text-gray-400')}>
                                                {doc.status === 'EMBEDDED' ? <CheckCircle className="w-4 h-4" /> : <div className="w-2 h-2 rounded-full bg-gray-300" />}
                                                {doc.status}
                                            </span>
                                        </td>
                                        <td className="p-4 text-sm text-gray-500">
                                            {new Date().toLocaleDateString()} {/* Mock date for MVP */}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    {documents.length === 0 && !loading && (
                        <div className="p-12 text-center text-gray-400">No documents found. Trigger ingestion to start.</div>
                    )}
                </div>
            </div>
        </div>
    );
}
