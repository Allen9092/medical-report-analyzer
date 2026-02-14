import React, { useState } from 'react';
import { Upload, FileText, Activity, Beaker, ClipboardList, Loader2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
    const [inputText, setInputText] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyzeText = async () => {
        if (!inputText) return;
        setLoading(true);
        setError(null);
        try {
            const res = await fetch('http://localhost:8000/analyze/text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: inputText }),
            });
            const data = await res.json();
            if (res.ok && data.status === 'success') {
                setResults(data.data);
            } else {
                let msg = 'Analysis failed';
                if (data.detail) {
                    msg = typeof data.detail === 'string' ? data.detail :
                        Array.isArray(data.detail) ? data.detail.map(d => `${d.loc.join('.')}: ${d.msg}`).join('; ') :
                            JSON.stringify(data.detail);
                }
                setError(msg);
                setResults(null);
            }
        } catch (err) {
            setError('Connection to backend failed');
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        const uploadedFile = e.target.files[0];
        if (!uploadedFile) return;
        setFile(uploadedFile);
        setLoading(true);
        setError(null);
        try {
            const formData = new FormData();
            formData.append('file', uploadedFile);
            const res = await fetch('http://localhost:8000/analyze/file', {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            if (res.ok && data.status === 'success') {
                setResults(data.data);
            } else {
                let msg = 'Analysis failed';
                if (data.detail) {
                    msg = typeof data.detail === 'string' ? data.detail :
                        Array.isArray(data.detail) ? data.detail.map(d => `${d.loc.join('.')}: ${d.msg}`).join('; ') :
                            JSON.stringify(data.detail);
                }
                setError(msg);
                setResults(null);
            }
        } catch (err) {
            setError('Connection to backend failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="header animate-fade-in">
                <h1 className="title">🏥 Medical Pro Analyzer</h1>
                <p className="subtitle">AI-powered medical report extraction and lab value validation</p>
            </header>

            <main className="grid">
                <section className="upload-section animate-fade-in" style={{ animationDelay: '0.1s' }}>
                    <div className="glass-card">
                        <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <FileText size={20} className="text-accent" />
                            Input Report
                        </h3>

                        <textarea
                            className="textarea"
                            placeholder="Paste medical report text here..."
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                        />

                        <div style={{ margin: '1.5rem 0', textAlign: 'center', position: 'relative' }}>
                            <div style={{ borderTop: '1px solid var(--border)', position: 'absolute', width: '100%', top: '50%' }}></div>
                            <span style={{ background: 'var(--bg)', padding: '0 1rem', position: 'relative', color: 'var(--text-muted)', fontSize: '0.875rem' }}>OR</span>
                        </div>

                        <div className="file-input-container">
                            <Upload size={32} style={{ marginBottom: '1rem', color: 'var(--primary)' }} />
                            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                {file ? file.name : 'Upload TXT or PDF report'}
                            </p>
                            <input type="file" className="file-input" onChange={handleFileUpload} accept=".txt,.pdf" />
                        </div>

                        <button
                            className="btn btn-primary"
                            style={{ width: '100%', marginTop: '1.5rem' }}
                            onClick={handleAnalyzeText}
                            disabled={loading || (!inputText && !file)}
                        >
                            {loading ? <Loader2 className="animate-spin" /> : 'Start Analysis'}
                        </button>
                    </div>
                </section>

                <section className="results-section animate-fade-in" style={{ animationDelay: '0.2s' }}>
                    <AnimatePresence mode="wait">
                        {!results && !error && !loading && (
                            <motion.div
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                                className="glass-card" style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', color: 'var(--text-muted)' }}
                            >
                                <Activity size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                                <p>Upload or paste a report to see analysis results here.</p>
                            </motion.div>
                        )}

                        {loading && (
                            <motion.div
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                style={{ textAlign: 'center', padding: '3rem' }}
                            >
                                <Loader2 size={48} className="animate-spin text-primary" style={{ margin: '0 auto' }} />
                                <p style={{ marginTop: '1rem' }}>Analyzing your report...</p>
                            </motion.div>
                        )}

                        {error && (
                            <motion.div
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                className="glass-card" style={{ borderColor: 'var(--error)', background: 'rgba(239, 68, 68, 0.05)' }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--error)' }}>
                                    <AlertCircle size={24} />
                                    <p>{error}</p>
                                </div>
                            </motion.div>
                        )}

                        {results && (
                            <motion.div
                                initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
                                className="upload-section"
                            >
                                <div className="glass-card">
                                    <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <ClipboardList size={20} className="text-accent" />
                                        Diagnoses & Symptoms
                                    </h3>

                                    <div style={{ marginBottom: '1.5rem' }}>
                                        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Possible Diagnoses</p>
                                        {results.diseases.length > 0 ? (
                                            results.diseases.map((d, i) => <span key={i} className="result-tag">{d}</span>)
                                        ) : (
                                            <p style={{ fontSize: '0.875rem' }}>No diseases detected</p>
                                        )}
                                    </div>

                                    <div>
                                        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Symptoms Observed</p>
                                        {results.symptoms.length > 0 ? (
                                            results.symptoms.map((s, i) => <span key={i} className="result-tag" style={{ border: 'none', background: 'rgba(255,255,255,0.05)' }}>{s}</span>)
                                        ) : (
                                            <p style={{ fontSize: '0.875rem' }}>No symptoms detected</p>
                                        )}
                                    </div>
                                </div>

                                <div className="glass-card">
                                    <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <Beaker size={20} className="text-accent" />
                                        Laboratory Values
                                    </h3>

                                    {Object.keys(results.labs).length > 0 ? (
                                        <div>
                                            {Object.entries(results.labs).map(([name, data], i) => (
                                                <div key={i} className="lab-item">
                                                    <div>
                                                        <p style={{ fontWeight: '500' }}>{name}</p>
                                                        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{data.value} {data.unit}</p>
                                                    </div>
                                                    <span className={`status-${data.status.toLowerCase()}`} style={{ fontWeight: '700', fontSize: '0.875rem' }}>
                                                        {data.status.toUpperCase()}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>No lab values detected</p>
                                    )}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </section>
            </main>

            <footer style={{ marginTop: '4rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                <p>© 2026 Medical Pro Analyzer. All processing is local and private.</p>
            </footer>
        </div>
    );
}
