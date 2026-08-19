import React from 'react';
import { PhoneCall, AlertTriangle, X, ShieldAlert, ExternalLink, HeartHandshake } from 'lucide-react';

export default function CrisisModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  const hotlines = [
    {
      country: "India",
      name: "KIRAN Mental Health Helpline",
      number: "1800-599-0019",
      type: "tel:18005990019",
      desc: "24/7 Government Toll-Free Helpline in 13 languages"
    },
    {
      country: "India",
      name: "Tele-MANAS",
      number: "14416 / 1800-891-4416",
      type: "tel:14416",
      desc: "24/7 National Tele-Mental Health Programme"
    },
    {
      country: "India",
      name: "Vandrevala Foundation",
      number: "+91 9999 666 555",
      type: "tel:+919999666555",
      desc: "24/7 Free & Confidential Crisis Counseling"
    },
    {
      country: "United States & Canada",
      name: "Suicide & Crisis Lifeline",
      number: "988",
      type: "tel:988",
      desc: "Free 24/7 Call or Text Support"
    },
    {
      country: "United Kingdom",
      name: "Samaritans",
      number: "116 123",
      type: "tel:116123",
      desc: "Free 24/7 Emotional Support Helpline"
    },
    {
      country: "International / Online",
      name: "Find A Helpline (Global)",
      number: "findahelpline.com",
      type: "https://findahelpline.com",
      desc: "Instant search for crisis support in 130+ countries",
      isWeb: true
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-rose-500/40 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl shadow-rose-950/50 p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-2 rounded-full hover:bg-slate-800 transition"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-rose-500/20 rounded-xl text-rose-400">
            <ShieldAlert className="w-8 h-8 animate-pulse" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              Immediate Crisis Support & Helplines
            </h2>
            <p className="text-rose-300 text-sm">You are never alone. Compassionate, confidential help is available right now.</p>
          </div>
        </div>

        <div className="bg-rose-950/40 border border-rose-800/50 rounded-xl p-4 mb-6 text-slate-200 text-sm leading-relaxed">
          <p className="font-semibold text-rose-200 mb-1 flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            If you or someone you know is in immediate danger:
          </p>
          Please call your local emergency services (e.g. <strong>112 in India/EU</strong>, <strong>911 in the US</strong>, <strong>999 in the UK</strong>) or reach out to the 24/7 helplines below.
        </div>

        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
          <HeartHandshake className="w-4 h-4 text-teal-400" />
          24/7 Verified Helplines
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
          {hotlines.map((h, idx) => (
            <div key={idx} className="bg-slate-800/80 hover:bg-slate-800 border border-slate-700/70 rounded-xl p-3.5 transition flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-700 text-teal-300">
                    {h.country}
                  </span>
                </div>
                <h4 className="font-bold text-white text-base">{h.name}</h4>
                <p className="text-xs text-slate-400 mb-3">{h.desc}</p>
              </div>

              {h.isWeb ? (
                <a
                  href={h.type}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs py-2 px-3 rounded-lg transition"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  Visit Website ({h.number})
                </a>
              ) : (
                <a
                  href={h.type}
                  className="flex items-center justify-center gap-2 bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs py-2 px-3 rounded-lg transition"
                >
                  <PhoneCall className="w-3.5 h-3.5 animate-bounce" />
                  Call: {h.number}
                </a>
              )}
            </div>
          ))}
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium py-2 px-5 rounded-xl border border-slate-700 transition"
          >
            Close Window
          </button>
        </div>
      </div>
    </div>
  );
}
