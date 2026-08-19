import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { API_BASE_URL } from '../config';
import {
  ClipboardList,
  CheckCircle,
  AlertCircle,
  ShieldAlert,
  ArrowRight,
  RotateCcw,
  Sparkles,
  Heart,
  History,
  BookOpen
} from 'lucide-react';

export default function AssessmentView({ sessionId, onOpenCrisis }) {
  const [assessmentType, setAssessmentType] = useState('PHQ-9');
  const [schema, setSchema] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [viewMode, setViewMode] = useState('form'); // 'form' or 'history'

  useEffect(() => {
    fetchSchema(assessmentType);
    fetchHistory();
  }, [assessmentType]);

  const fetchSchema = async (type) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/assessments/schema/${type}`);
      if (res.ok) {
        const data = await res.json();
        setSchema(data);
        setAnswers(new Array(data.questions.length).fill(null));
        setResult(null);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/assessments/${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSelectOption = (qIndex, value) => {
    const newAnswers = [...answers];
    newAnswers[qIndex] = value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {
    if (answers.some((a) => a === null)) {
      alert("Please answer all questions before submitting.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/assessments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          assessment_type: assessmentType,
          answers: answers
        })
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
        fetchHistory();
        // Fire confetti celebration
        confetti({
          particleCount: 75,
          spread: 60,
          origin: { y: 0.6 }
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityBadgeClass = (severity) => {
    if (!severity) return 'bg-slate-700 text-slate-200';
    const s = severity.toLowerCase();
    if (s.includes('minimal') || s.includes('none')) return 'bg-emerald-950 text-emerald-300 border-emerald-700/60';
    if (s.includes('mild')) return 'bg-blue-950 text-blue-300 border-blue-700/60';
    if (s.includes('moderate') && !s.includes('moderately severe')) return 'bg-amber-950 text-amber-300 border-amber-700/60';
    if (s.includes('moderately severe')) return 'bg-orange-950 text-orange-300 border-orange-700/60';
    return 'bg-rose-950 text-rose-300 border-rose-700/60';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      {/* Header & Switchers */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
              <ClipboardList className="w-6 h-6 text-teal-400" />
              Standardized Clinical Self-Screening
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Evidence-based psychological assessment tools validated for mental health tracking (SDG 3).
            </p>
          </div>

          <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-xl border border-slate-800 shrink-0">
            <button
              onClick={() => {
                setAssessmentType('PHQ-9');
                setViewMode('form');
              }}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                assessmentType === 'PHQ-9' && viewMode === 'form'
                  ? 'bg-teal-600 text-white'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              PHQ-9 (Depression)
            </button>
            <button
              onClick={() => {
                setAssessmentType('GAD-7');
                setViewMode('form');
              }}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                assessmentType === 'GAD-7' && viewMode === 'form'
                  ? 'bg-teal-600 text-white'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              GAD-7 (Anxiety)
            </button>
            <button
              onClick={() => setViewMode('history')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 transition ${
                viewMode === 'history'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <History className="w-3.5 h-3.5" />
              History
            </button>
          </div>
        </div>
      </div>

      {/* History View */}
      {viewMode === 'history' ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <History className="w-5 h-5 text-indigo-400" />
            Your Assessment Records
          </h2>
          {history.length === 0 ? (
            <p className="text-sm text-slate-400 py-6 text-center">
              No previous assessment entries recorded yet. Complete a screening to see your history here!
            </p>
          ) : (
            <div className="divide-y divide-slate-800">
              {history.map((rec) => (
                <div key={rec.id} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-white text-sm">{rec.assessment_type}</span>
                      <span className={`px-2 py-0.5 rounded-full border text-[11px] font-semibold ${getSeverityBadgeClass(rec.severity)}`}>
                        {rec.severity}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1">
                      Score: <strong className="text-teal-400">{rec.total_score}</strong> | Completed on {new Date(rec.created_at).toLocaleDateString()} at {new Date(rec.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                  <div className="text-xs text-slate-400">
                    {rec.recommendations?.length || 0} tailored guidance points
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : result ? (
        /* Result Screen */
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-6 animate-fadeIn">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
            <div>
              <span className="text-xs font-semibold text-teal-400 uppercase tracking-wider">
                Screening Completed
              </span>
              <h2 className="text-2xl font-bold text-white mt-0.5">{result.assessment_type}</h2>
            </div>

            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-slate-400 block">Total Score</span>
                <span className="text-2xl font-black text-white">
                  {result.total_score} <span className="text-slate-500 text-sm">/ {result.max_score}</span>
                </span>
              </div>
              <div className={`px-3.5 py-1.5 rounded-xl border text-sm font-bold ${getSeverityBadgeClass(result.severity)}`}>
                {result.severity}
              </div>
            </div>
          </div>

          {/* Self Harm Alert if detected */}
          {result.has_self_harm_risk && (
            <div className="bg-rose-950/70 border border-rose-600 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <div className="flex items-center gap-3 text-rose-200 text-xs sm:text-sm">
                <ShieldAlert className="w-6 h-6 text-rose-400 shrink-0 animate-pulse" />
                <span>
                  You indicated thoughts of self-harm or hurting yourself. Please know you matter and support is right here.
                </span>
              </div>
              <button
                onClick={onOpenCrisis}
                className="bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold px-4 py-2 rounded-xl shrink-0 transition"
              >
                Access Emergency Helplines
              </button>
            </div>
          )}

          {/* Interpretation */}
          <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
              Clinical Interpretation
            </h3>
            <p className="text-sm text-slate-200 leading-relaxed">{result.interpretation}</p>
          </div>

          {/* Tailored Recommendations */}
          <div>
            <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-teal-400" />
              Evidence-Based Recommendations & Coping Steps
            </h3>
            <ul className="space-y-2.5">
              {result.recommendations.map((rec, i) => (
                <li
                  key={i}
                  className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3.5 text-xs sm:text-sm text-slate-200 flex items-start gap-3"
                >
                  <CheckCircle className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Retake Button */}
          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              onClick={() => {
                setResult(null);
                setAnswers(new Array(schema?.questions.length || 9).fill(null));
              }}
              className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-xl text-xs font-semibold transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Retake Screening
            </button>
          </div>
        </div>
      ) : schema ? (
        /* Questions Form */
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
          <div>
            <h2 className="text-lg font-bold text-white">{schema.title}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{schema.subtitle}</p>
          </div>

          {/* Questions List */}
          <div className="space-y-6">
            {schema.questions.map((q, qIdx) => (
              <div
                key={q.id}
                className="bg-slate-950/40 border border-slate-800/80 rounded-xl p-4 space-y-3"
              >
                <div className="flex items-start gap-2">
                  <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-slate-800 text-teal-300">
                    #{q.id}
                  </span>
                  <p className="text-sm font-medium text-slate-100">{q.text}</p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1">
                  {schema.options.map((opt) => {
                    const isSelected = answers[qIdx] === opt.value;
                    return (
                      <button
                        key={opt.value}
                        type="button"
                        onClick={() => handleSelectOption(qIdx, opt.value)}
                        className={`p-2.5 rounded-xl text-xs font-medium border text-center transition-all ${
                          isSelected
                            ? 'bg-teal-600 text-white border-teal-500 shadow-md shadow-teal-950/40 font-bold scale-[1.02]'
                            : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                        }`}
                      >
                        {opt.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <span className="text-xs text-slate-400">
              Answered: {answers.filter((a) => a !== null).length} / {schema.questions.length}
            </span>
            <button
              onClick={handleSubmit}
              disabled={answers.some((a) => a === null) || loading}
              className="flex items-center gap-2 bg-teal-600 hover:bg-teal-500 disabled:opacity-40 disabled:hover:bg-teal-600 text-white text-xs font-bold py-2.5 px-6 rounded-xl shadow-lg shadow-teal-950/40 transition"
            >
              {loading ? 'Analyzing...' : 'Calculate My Score'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
