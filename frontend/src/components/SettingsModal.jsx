import React, { useState } from 'react';
import { X, Key, Volume2, Trash2, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function SettingsModal({ isOpen, onClose, apiKey, onSaveApiKey, onClearHistory }) {
  const [keyInput, setKeyInput] = useState(apiKey || '');
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSave = (e) => {
    e.preventDefault();
    onSaveApiKey(keyInput.trim());
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 900);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 relative shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-2 rounded-full hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <h2 className="text-xl font-bold text-white mb-1 flex items-center gap-2">
          Settings & AI Preferences
        </h2>
        <p className="text-xs text-slate-400 mb-5">
          Configure model keys and local privacy settings.
        </p>

        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Key className="w-4 h-4 text-teal-400" />
              Google Gemini API Key (Optional)
            </label>
            <input
              type="password"
              value={keyInput}
              onChange={(e) => setKeyInput(e.target.value)}
              placeholder="Paste your AIzaSy... API key"
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-teal-400 focus:ring-1 focus:ring-teal-400"
            />
            <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
              If left blank, the app runs on the built-in <strong>Offline CBT Empathy Engine</strong> with full sentiment analysis, grounding guides, and cognitive distortion reframing.
            </p>
          </div>

          <div className="pt-2 border-t border-slate-800">
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Privacy & Local Storage
            </h4>
            <p className="text-xs text-slate-400 mb-3">
              Your conversations and mood logs are processed securely in your local environment.
            </p>
            <button
              type="button"
              onClick={() => {
                if (window.confirm("Are you sure you want to reset your local conversation state?")) {
                  onClearHistory();
                  onClose();
                }
              }}
              className="flex items-center gap-2 text-rose-400 hover:text-rose-300 text-xs font-medium bg-rose-950/30 hover:bg-rose-950/60 border border-rose-800/40 px-3 py-2 rounded-lg transition"
            >
              <Trash2 className="w-3.5 h-3.5" />
              Clear Local Session History
            </button>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex items-center gap-2 bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs py-2 px-5 rounded-lg shadow-lg shadow-teal-900/30 transition"
            >
              {savedSuccess ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-300" />
                  Saved!
                </>
              ) : (
                'Save Settings'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
