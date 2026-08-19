import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { API_BASE_URL } from '../config';
import {
  SmilePlus,
  TrendingUp,
  Activity,
  Heart,
  Calendar,
  Sparkles,
  Zap,
  CheckCircle2
} from 'lucide-react';

const MOOD_OPTIONS = [
  { score: 1, label: 'Very Low', emoji: '😢', color: 'hover:border-rose-500 hover:text-rose-400' },
  { score: 2, label: 'Low / Down', emoji: '🙁', color: 'hover:border-amber-500 hover:text-amber-400' },
  { score: 3, label: 'Neutral / Okay', emoji: '😐', color: 'hover:border-slate-500 hover:text-slate-300' },
  { score: 4, label: 'Good / Pleased', emoji: '🙂', color: 'hover:border-teal-500 hover:text-teal-400' },
  { score: 5, label: 'Joyful / Great', emoji: '😄', color: 'hover:border-emerald-500 hover:text-emerald-400' }
];

const EMOTION_TAGS = [
  'Anxious', 'Calm', 'Overwhelmed', 'Grateful', 'Tired',
  'Lonely', 'Inspired', 'Hopeful', 'Stressed', 'Peaceful', 'Restless'
];

export default function MoodTrackerView({ sessionId }) {
  const [selectedMood, setSelectedMood] = useState(4);
  const [energyLevel, setEnergyLevel] = useState(3);
  const [selectedTags, setSelectedTags] = useState([]);
  const [notes, setNotes] = useState('');
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({ average_mood: 0, total_entries: 0, average_energy: 0 });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    fetchMoodLogs();
  }, []);

  const fetchMoodLogs = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/moods/${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setLogs(data.logs || []);
        setStats(data.stats || { average_mood: 0, total_entries: 0, average_energy: 0 });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleTagToggle = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  const handleLogMood = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/moods`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          mood_score: selectedMood,
          energy_level: energyLevel,
          emotion_tags: selectedTags.join(', '),
          notes: notes
        })
      });

      if (res.ok) {
        setSavedSuccess(true);
        setNotes('');
        setSelectedTags([]);
        fetchMoodLogs();
        confetti({
          particleCount: 50,
          spread: 45,
          origin: { y: 0.7 }
        });
        setTimeout(() => setSavedSuccess(false), 3000);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getMoodEmoji = (score) => {
    const item = MOOD_OPTIONS.find((m) => m.score === score);
    return item ? item.emoji : '😐';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
          <SmilePlus className="w-6 h-6 text-teal-400" />
          Emotional Well-being & Mood Journal
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Tracking your daily feelings builds self-awareness and emotional regulation (SDG 3).
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Mood Check-In Card */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Heart className="w-4 h-4 text-teal-400" />
            Today's Check-in
          </h2>

          <form onSubmit={handleLogMood} className="space-y-5">
            {/* Mood Scale Selector */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                How are you feeling overall?
              </label>
              <div className="grid grid-cols-5 gap-2">
                {MOOD_OPTIONS.map((item) => {
                  const isSelected = selectedMood === item.score;
                  return (
                    <button
                      key={item.score}
                      type="button"
                      onClick={() => setSelectedMood(item.score)}
                      className={`flex flex-col items-center justify-center p-3 rounded-xl border transition-all ${
                        isSelected
                          ? 'bg-teal-600/30 border-teal-400 scale-105 shadow-md shadow-teal-950/40 text-white'
                          : 'bg-slate-950/50 border-slate-800 text-slate-400 hover:border-slate-700'
                      }`}
                    >
                      <span className="text-2xl mb-1">{item.emoji}</span>
                      <span className="text-[10px] font-medium text-center">{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Energy Slider */}
            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                  <Zap className="w-3.5 h-3.5 text-amber-400" />
                  Energy Level: {energyLevel} / 5
                </label>
              </div>
              <input
                type="range"
                min="1"
                max="5"
                value={energyLevel}
                onChange={(e) => setEnergyLevel(Number(e.target.value))}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-400"
              />
            </div>

            {/* Emotion Chips */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                What emotions are present? (Select all that apply)
              </label>
              <div className="flex flex-wrap gap-1.5">
                {EMOTION_TAGS.map((tag) => {
                  const isSelected = selectedTags.includes(tag);
                  return (
                    <button
                      key={tag}
                      type="button"
                      onClick={() => handleTagToggle(tag)}
                      className={`px-3 py-1 rounded-full text-xs font-medium border transition ${
                        isSelected
                          ? 'bg-teal-600 text-white border-teal-500'
                          : 'bg-slate-950/40 border-slate-800 text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      {tag}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Journal / Thoughts Note */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Journal Reflection / Gratitude (Optional)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="What triggered this mood? What is one thing you appreciate today?"
                rows={3}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-teal-400"
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold py-2.5 rounded-xl shadow-lg shadow-teal-950/40 transition flex items-center justify-center gap-2"
            >
              {savedSuccess ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-300" />
                  Mood Recorded!
                </>
              ) : (
                'Save Today’s Mood'
              )}
            </button>
          </form>
        </div>

        {/* Analytics & Stats Card */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-teal-400" />
              Emotional Analytics
            </h2>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-3.5 text-center">
                <span className="text-[11px] text-slate-400 block mb-1">Average Mood</span>
                <span className="text-2xl font-black text-teal-400">
                  {stats.average_mood ? `${stats.average_mood} / 5` : 'N/A'}
                </span>
              </div>
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-3.5 text-center">
                <span className="text-[11px] text-slate-400 block mb-1">Total Logs</span>
                <span className="text-2xl font-black text-indigo-400">
                  {stats.total_entries}
                </span>
              </div>
            </div>

            {/* Visual Trend Bars */}
            <div className="space-y-2 pt-2">
              <span className="text-xs font-semibold text-slate-400 block">Recent Entries</span>
              {logs.slice(0, 5).map((log) => (
                <div
                  key={log.id}
                  className="bg-slate-950/40 border border-slate-800 rounded-xl p-2.5 flex items-center justify-between"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{getMoodEmoji(log.mood_score)}</span>
                    <div>
                      <div className="flex items-center gap-1.5 flex-wrap">
                        {log.emotion_tags.slice(0, 2).map((t, i) => (
                          <span key={i} className="text-[10px] bg-slate-800 text-teal-300 px-1.5 py-0.5 rounded">
                            {t}
                          </span>
                        ))}
                      </div>
                      <span className="text-[10px] text-slate-500 block">
                        {new Date(log.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <span className="text-xs font-bold text-slate-300">
                    {log.mood_score}/5
                  </span>
                </div>
              ))}

              {logs.length === 0 && (
                <p className="text-xs text-slate-500 text-center py-4">No check-ins yet.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
