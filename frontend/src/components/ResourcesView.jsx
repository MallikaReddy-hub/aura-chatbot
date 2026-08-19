import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Globe,
  CheckSquare,
  Sparkles,
  HelpCircle,
  PhoneCall,
  ExternalLink,
  Shield,
  Layers,
  HeartHandshake
} from 'lucide-react';

export default function ResourcesView({ onOpenCrisis }) {
  const [resources, setResources] = useState(null);
  const [groundingChecklist, setGroundingChecklist] = useState({
    see: false,
    touch: false,
    hear: false,
    smell: false,
    taste: false
  });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/resources')
      .then((r) => r.json())
      .then((data) => setResources(data))
      .catch((err) => console.error(err));
  }, []);

  const toggleCheck = (key) => {
    setGroundingChecklist((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const mythsFacts = [
    {
      myth: "Mental health issues are a sign of personal weakness or lack of willpower.",
      fact: "Mental health conditions are complex medical and biological conditions influenced by neurobiology, genetics, trauma, and environment. Seeking support is a sign of strength."
    },
    {
      myth: "Therapy and mental health support are only for people with severe mental disorders.",
      fact: "Anyone can benefit from counseling, active listening, and CBT techniques to navigate stress, burnout, grief, relationships, and self-growth."
    },
    {
      myth: "Children and teenagers do not experience true mental health struggles.",
      fact: "Half of all mental health conditions begin by age 14. Early intervention and supportive environments make a profound lifelong impact."
    }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
          <BookOpen className="w-6 h-6 text-teal-400" />
          SDG 3 Mental Health Resource Hub
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Psychoeducation, evidence-based coping tools, and verified community support centers.
        </p>
      </div>

      {/* UN SDG 3 Showcase Banner */}
      <div className="bg-gradient-to-br from-teal-950/70 via-slate-900 to-indigo-950/70 border border-teal-700/40 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col sm:flex-row items-start gap-4">
          <div className="p-4 bg-teal-500/20 rounded-2xl text-teal-300 border border-teal-500/30">
            <Globe className="w-8 h-8 animate-spin-slow" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-teal-300">
              United Nations Sustainable Development Goal 3
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-white mt-0.5 mb-2">
              Target 3.4: Good Health and Well-being
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed mb-4">
              "By 2030, reduce premature mortality from non-communicable diseases through prevention and treatment, and promote mental health and well-being."
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-3">
                <span className="text-xs font-bold text-teal-300 block mb-1">Accessibility</span>
                <p className="text-[11px] text-slate-400">Democratizing mental health guidance 24/7 at zero cost.</p>
              </div>
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-3">
                <span className="text-xs font-bold text-indigo-300 block mb-1">Stigma Reduction</span>
                <p className="text-[11px] text-slate-400">Providing a safe, private space to build emotional resilience.</p>
              </div>
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-3">
                <span className="text-xs font-bold text-emerald-300 block mb-1">Early Screening</span>
                <p className="text-[11px] text-slate-400">Standardized PHQ-9 & GAD-7 self-screening for timely support.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive 5-4-3-2-1 Grounding Tool */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Layers className="w-4 h-4 text-teal-400" />
          Interactive 5-4-3-2-1 Sensory Grounding Practice
        </h2>
        <p className="text-xs text-slate-400">
          When your mind is racing or trapped in anxiety, ground your awareness in your immediate physical environment. Check off each sensory step as you complete it:
        </p>

        <div className="space-y-2.5">
          {[
            { key: 'see', count: 5, text: 'Look around and name 5 distinct things you can SEE' },
            { key: 'touch', count: 4, text: 'Name 4 things you can physically TOUCH or feel on your skin' },
            { key: 'hear', count: 3, text: 'Listen closely and notice 3 sounds you can HEAR' },
            { key: 'smell', count: 2, text: 'Identify 2 different things you can SMELL in the air' },
            { key: 'taste', count: 1, text: 'Notice 1 thing you can TASTE or one positive attribute about yourself' }
          ].map((step) => {
            const isChecked = groundingChecklist[step.key];
            return (
              <button
                key={step.key}
                type="button"
                onClick={() => toggleCheck(step.key)}
                className={`w-full text-left p-3 rounded-xl border flex items-center gap-3 transition ${
                  isChecked
                    ? 'bg-teal-950/50 border-teal-600 text-teal-200'
                    : 'bg-slate-950/50 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div
                  className={`w-6 h-6 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                    isChecked ? 'bg-teal-600 text-white' : 'bg-slate-800 text-teal-300'
                  }`}
                >
                  {step.count}
                </div>
                <span className="text-xs sm:text-sm font-medium flex-1">{step.text}</span>
                {isChecked && <CheckSquare className="w-4 h-4 text-teal-400 shrink-0" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Mental Health Myths vs Facts */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <HelpCircle className="w-4 h-4 text-indigo-400" />
          Myths vs. Facts in Mental Health
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {mythsFacts.map((item, idx) => (
            <div key={idx} className="bg-slate-950/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
              <div>
                <div className="text-[11px] font-bold text-rose-400 mb-1 flex items-center gap-1">
                  ❌ Myth
                </div>
                <p className="text-xs text-slate-300 font-medium mb-3 italic">"{item.myth}"</p>
              </div>
              <div className="pt-2 border-t border-slate-800">
                <div className="text-[11px] font-bold text-emerald-400 mb-1 flex items-center gap-1">
                  ✅ Reality & Science
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{item.fact}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Emergency Crisis Callout */}
      <div className="bg-rose-950/40 border border-rose-800/60 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-rose-600/20 rounded-xl text-rose-400">
            <HeartHandshake className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-white text-base">In Need of Immediate Human Support?</h3>
            <p className="text-xs text-rose-200">Connect with free, confidential 24/7 hotlines and professional crisis counselors.</p>
          </div>
        </div>

        <button
          onClick={onOpenCrisis}
          className="bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold px-5 py-2.5 rounded-xl shadow-lg transition shrink-0 flex items-center gap-2"
        >
          <PhoneCall className="w-4 h-4" />
          View Verified Helplines
        </button>
      </div>
    </div>
  );
}
