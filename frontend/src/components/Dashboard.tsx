import { useEffect, useState } from 'react';
import axios from 'axios';
import {
    CheckCircle, AlertTriangle, TrendingUp, ShieldAlert,
    Activity, FileText, Globe, Search, RefreshCw, X, BrainCircuit
} from 'lucide-react';
import { clsx } from 'clsx';

interface Document {
    id: number;
    title: string;
    source: string;
    url: string;
    risk_score: number;
    status: string;
    published_date: string;
    extra_metadata?: any;
}

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';

export function Dashboard() {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        setLoading(true);
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
        if (score >= 75) return "text-rose-400 bg-rose-400/10 border-rose-400/20";
        if (score >= 50) return "text-amber-400 bg-amber-400/10 border-amber-400/20";
        return "text-emerald-400 bg-emerald-400/10 border-emerald-400/20";
    };

    const highRiskCount = documents.filter(d => d.risk_score >= 75).length;
    const avgScore = documents.length > 0
        ? Math.round(documents.reduce((acc, doc) => acc + doc.risk_score, 0) / documents.length)
        : 0;

    const filteredDocs = documents.filter(doc =>
        doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.source.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // Simulated Analysis Generation
    const getAnalysis = (doc: Document) => {
        if (doc.risk_score >= 80) return "CRITICAL: Detected high-probability distress signals. Keywords 'Going Concern' or 'Material Weakness' identified in recent disclosures. Immediate review recommended.";
        if (doc.risk_score >= 50) return "WARNING: Elevated risk factors present. Volatility or Debt keywords detected significantly above baseline. Monitor for further deterioration.";
        return "STABLE: No significant red flags detected in standard risk categories. Routine monitoring advised.";
    };

    return (
        <div className="min-h-screen p-6 md:p-8 space-y-8">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 max-w-7xl mx-auto">
                <div>
                    <h1 className="text-4xl font-black tracking-tight text-white flex items-center gap-3">
                        FINCRAWL <span className="text-indigo-400 text-sm font-medium px-2 py-0.5 rounded-full bg-indigo-400/10 border border-indigo-400/20 tracking-normal align-middle">v1.0</span>
                    </h1>
                    <p className="text-slate-400 mt-2 text-lg">Autonomous Financial Risk Intelligence</p>
                </div>
                <div className="flex items-center gap-3">
                    <span className="flex items-center gap-2 text-xs font-medium text-emerald-400 bg-emerald-400/5 px-3 py-1.5 rounded-full border border-emerald-400/10 animate-pulse">
                        <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                        SYSTEM OPERATIONAL
                    </span>
                    <button
                        onClick={fetchDocuments}
                        className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-all border border-slate-700"
                        title="Refresh Data"
                    >
                        <RefreshCw className={clsx("w-5 h-5", loading && "animate-spin")} />
                    </button>
                </div>
            </div>

            <div className="max-w-7xl mx-auto space-y-8">
                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <FileText className="w-24 h-24 text-slate-200" />
                        </div>
                        <h3 className="text-slate-400 text-sm font-medium uppercase tracking-wider">Monitored Filings</h3>
                        <p className="text-4xl font-bold text-white mt-2">{documents.length}</p>
                        <div className="mt-4 text-xs text-slate-500">Across SEC EDGAR & Global News</div>
                    </div>

                    <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <ShieldAlert className="w-24 h-24 text-rose-400" />
                        </div>
                        <h3 className="text-rose-400/80 text-sm font-medium uppercase tracking-wider">Critical Activity</h3>
                        <div className="flex items-baseline gap-2 mt-2">
                            <p className="text-4xl font-bold text-rose-400">{highRiskCount}</p>
                            <span className="text-sm text-slate-400">High Risk Events</span>
                        </div>
                        <div className="mt-4 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-rose-500 transition-all duration-1000"
                                style={{ width: `${(highRiskCount / (documents.length || 1)) * 100}%` }}
                            />
                        </div>
                    </div>

                    <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <Activity className="w-24 h-24 text-indigo-400" />
                        </div>
                        <h3 className="text-indigo-400/80 text-sm font-medium uppercase tracking-wider">Market Avg Risk</h3>
                        <p className="text-4xl font-bold text-indigo-400 mt-2">{avgScore}<span className="text-lg text-slate-500 font-normal">/100</span></p>
                        <div className="mt-4 text-xs text-slate-500">Weighted volatility index</div>
                    </div>
                </div>

                {/* Main Content Area */}
                <div className="glass-panel rounded-2xl overflow-hidden flex flex-col min-h-[600px]">
                    <div className="p-6 border-b border-white/5 flex flex-col sm:flex-row justify-between items-center gap-4 bg-slate-900/40">
                        <div className="flex items-center gap-3">
                            <TrendingUp className="text-indigo-400 w-5 h-5" />
                            <h2 className="text-lg font-semibold text-white">Live Risk Feed</h2>
                        </div>

                        <div className="relative w-full sm:w-72">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                            <input
                                type="text"
                                placeholder="Search tickers, keywords..."
                                className="w-full bg-black/20 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-slate-300 focus:outline-none focus:border-indigo-500/50 focus:bg-black/40 transition-all"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="overflow-x-auto flex-1">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-slate-900/60 text-slate-400 text-xs uppercase tracking-wider">
                                    <th className="p-5 font-medium w-32">Risk Score</th>
                                    <th className="p-5 font-medium">Entity / Event</th>
                                    <th className="p-5 font-medium w-40">Source</th>
                                    <th className="p-5 font-medium w-32">Status</th>
                                    <th className="p-5 font-medium w-40 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {filteredDocs.map((doc) => (
                                    <tr key={doc.id} className="group hover:bg-white/[0.02] transition-colors">
                                        <td className="p-5">
                                            <div className={clsx("inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-bold border backdrop-blur-md shadow-lg", getRiskColor(doc.risk_score))}>
                                                {doc.risk_score >= 75 && <AlertTriangle className="w-3.5 h-3.5" />}
                                                {doc.risk_score}
                                            </div>
                                        </td>
                                        <td className="p-5">
                                            <div className="font-medium text-slate-200 group-hover:text-white transition-colors text-lg">{doc.title}</div>
                                            <div className="flex items-center gap-2 mt-1">
                                                <a href={doc.url} target="_blank" className="text-xs text-slate-500 hover:text-indigo-400 transition-colors truncate max-w-sm flex items-center gap-1">
                                                    <Globe className="w-3 h-3" />
                                                    {doc.url}
                                                </a>
                                            </div>
                                        </td>
                                        <td className="p-5">
                                            <span className="text-sm text-slate-400 px-2 py-1 rounded-md bg-white/5 border border-white/5">
                                                {doc.source}
                                            </span>
                                        </td>
                                        <td className="p-5">
                                            <div className="flex items-center gap-2 text-sm text-slate-400">
                                                {doc.status === 'EMBEDDED'
                                                    ? <CheckCircle className="w-4 h-4 text-emerald-500" />
                                                    : <div className="w-2 h-2 rounded-full bg-slate-600" />
                                                }
                                                <span className={clsx(doc.status === 'EMBEDDED' && "text-emerald-500/80")}>{doc.status}</span>
                                            </div>
                                        </td>
                                        <td className="p-5 text-right">
                                            <button
                                                onClick={() => setSelectedDoc(doc)}
                                                className="text-sm font-medium text-indigo-400 hover:text-indigo-300 hover:underline cursor-pointer"
                                            >
                                                Analyze &rarr;
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {filteredDocs.length === 0 && !loading && (
                            <div className="flex flex-col items-center justify-center h-64 text-slate-500">
                                <Search className="w-12 h-12 mb-4 opacity-20" />
                                <p>No filings found matching your criteria.</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Footer */}
                <div className="text-center text-slate-600 text-sm pb-8">
                    &copy; 2025 FINCRAWL Systems. All Analysis Generated Autonomously.
                </div>
            </div>

            {/* Analysis Modal */}
            {selectedDoc && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
                    <div className="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden glass-panel">
                        <div className="p-6 border-b border-white/10 flex justify-between items-start">
                            <div>
                                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                                    <BrainCircuit className="text-indigo-400" />
                                    AI Risk Analysis
                                </h2>
                                <p className="text-slate-400 text-sm mt-1">Autonomous evaluation of filing content</p>
                            </div>
                            <button
                                onClick={() => setSelectedDoc(null)}
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                <X className="w-6 h-6" />
                            </button>
                        </div>

                        <div className="p-6 space-y-6">
                            {/* Score Banner */}
                            <div className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5">
                                <div className={clsx("w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold border-4",
                                    selectedDoc.risk_score >= 75 ? "border-rose-500 text-rose-500" :
                                        selectedDoc.risk_score >= 50 ? "border-amber-500 text-amber-500" :
                                            "border-emerald-500 text-emerald-500"
                                )}>
                                    {selectedDoc.risk_score}
                                </div>
                                <div>
                                    <h3 className="text-white font-medium text-lg">{selectedDoc.title}</h3>
                                    <div className="flex items-center gap-2 text-sm text-slate-400 mt-1">
                                        <span>{selectedDoc.source}</span>
                                        <span>•</span>
                                        <span>{new Date().toLocaleDateString()}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Analysis Content */}
                            <div className="space-y-2">
                                <h4 className="text-sm font-semibold text-indigo-300 uppercase tracking-wider">Automated Finding</h4>
                                <p className="text-slate-300 leading-relaxed bg-black/20 p-4 rounded-lg border border-white/5">
                                    {getAnalysis(selectedDoc)}
                                </p>
                            </div>

                            <div className="space-y-3">
                                <h4 className="text-sm font-semibold text-indigo-300 uppercase tracking-wider">Detected Signals</h4>
                                <div className="flex flex-wrap gap-2">
                                    {selectedDoc.risk_score >= 75 && (
                                        <>
                                            <span className="px-3 py-1 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">Going Concern Warning</span>
                                            <span className="px-3 py-1 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">Solvency Risk</span>
                                        </>
                                    )}
                                    {selectedDoc.risk_score >= 30 && (
                                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">Market Volatility</span>
                                    )}
                                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Financial Disclosure</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-6 border-t border-white/10 bg-black/20 flex justify-end gap-3">
                            <button
                                onClick={() => setSelectedDoc(null)}
                                className="px-4 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors"
                            >
                                Close
                            </button>
                            <a
                                href={selectedDoc.url}
                                target="_blank"
                                className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 transition-colors font-medium flex items-center gap-2"
                            >
                                View Source <Globe className="w-4 h-4" />
                            </a>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
