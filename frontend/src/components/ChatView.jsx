import React, { useState, useEffect, useRef } from 'react';
import { API_BASE_URL } from '../config';
import {
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Sparkles,
  AlertTriangle,
  Heart,
  Bot,
  User,
  Lightbulb,
  ShieldCheck,
  RefreshCw,
  PhoneCall
} from 'lucide-react';

const QUICK_PROMPTS = [
  "I'm feeling overwhelmed with work and responsibilities.",
  "I have a lot of anxiety and my mind is racing.",
  "I'm feeling really lonely and sad today.",
  "Can you guide me through a quick grounding exercise?",
  "I'm having trouble falling asleep due to stress.",
  "I want to celebrate a small win from my day!"
];

export default function ChatView({ apiKey, onOpenCrisis, sessionId }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [activeDistortion, setActiveDistortion] = useState(null);
  
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Initial welcome message
  useEffect(() => {
    fetchHistory();
    // Check Speech Recognition support
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputText((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setIsListening(false);
      };

      recognitionRef.current.onerror = () => {
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };

      setSpeechSupported(true);
    }
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/chat/history/${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        if (data.length > 0) {
          setMessages(data);
          return;
        }
      }
    } catch (e) {
      console.log('No previous history found or server starting up');
    }

    // Default welcoming message
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content:
          "Hello, I'm **Aura**, your compassionate mental health & well-being companion. 🌿\n\nI am here to listen without judgment, help you explore anxious or overwhelming thoughts through gentle CBT reflections, and guide you through calming grounding routines.\n\n*How are you feeling right in this moment?*",
        sentiment: 'Supportive',
        emotion: 'calm',
        is_crisis: false
      }
    ]);
  };

  const handleSendMessage = async (textToSend = null) => {
    const text = textToSend || inputText;
    if (!text.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      created_at: new Date().toISOString()
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!textToSend) setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId,
          api_key: apiKey || null
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const botMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.reply,
        sentiment: data.nlp?.sentiment_label,
        emotion: data.nlp?.primary_emotion,
        is_crisis: data.is_crisis,
        hotlines: data.hotlines,
        cognitive_distortions: data.nlp?.cognitive_distortions,
        created_at: new Date().toISOString()
      };

      setMessages((prev) => [...prev, botMessage]);

      if (data.nlp?.cognitive_distortions?.length > 0) {
        setActiveDistortion(data.nlp.cognitive_distortions[0]);
      } else {
        setActiveDistortion(null);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content:
            "I'm here with you. It seems there was a temporary connection hiccup, but please take a slow, gentle breath. I'm ready whenever you'd like to try again.",
          sentiment: 'Neutral',
          emotion: 'calm',
          is_crisis: false
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) return;
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (e) {
        console.error(e);
      }
    }
  };

  const speakText = (text) => {
    if (!('speechSynthesis' in window)) return;
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    // Clean markdown stars/bullets for clean audio
    const cleanText = text.replace(/[*#•_]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const getEmotionBadge = (emotion) => {
    if (!emotion) return null;
    const map = {
      anxiety: { label: 'Anxiety Detected', bg: 'bg-amber-950/70 text-amber-300 border-amber-800/60' },
      sadness: { label: 'Low Mood / Sadness', bg: 'bg-indigo-950/70 text-indigo-300 border-indigo-800/60' },
      overwhelm: { label: 'Overwhelmed', bg: 'bg-purple-950/70 text-purple-300 border-purple-800/60' },
      anger: { label: 'Frustration / Anger', bg: 'bg-rose-950/70 text-rose-300 border-rose-800/60' },
      joy: { label: 'Positive & Joyful', bg: 'bg-emerald-950/70 text-emerald-300 border-emerald-800/60' },
      calm: { label: 'Calm & Centered', bg: 'bg-teal-950/70 text-teal-300 border-teal-800/60' }
    };
    return map[emotion.toLowerCase()] || null;
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-5rem)] pb-4">
      {/* Medical Safety Disclaimer Strip */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl px-4 py-2 mb-3 flex items-center justify-between text-[11px] text-slate-400">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-teal-400 shrink-0" />
          <span>
            <strong>Wellness & SDG 3 Support:</strong> Aura provides empathetic guidance and CBT coping tools. Not a substitute for medical diagnosis or emergency care.
          </span>
        </div>
        <button
          onClick={onOpenCrisis}
          className="text-rose-400 hover:text-rose-300 font-semibold underline shrink-0 ml-2"
        >
          Emergency Help
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 bg-slate-950/50 border border-slate-800/80 rounded-2xl p-4 sm:p-6 overflow-y-auto space-y-4 shadow-inner">
        {messages.map((msg, index) => {
          const isUser = msg.role === 'user';
          const emotionInfo = getEmotionBadge(msg.emotion);

          return (
            <div
              key={msg.id || index}
              className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-1`}
            >
              {/* Sender & Emotion Label */}
              <div className="flex items-center gap-2 px-1 text-[11px] text-slate-400">
                <span className="font-semibold">{isUser ? 'You' : 'Aura AI'}</span>
                {!isUser && emotionInfo && (
                  <span className={`px-2 py-0.5 rounded-full border text-[10px] font-medium ${emotionInfo.bg}`}>
                    {emotionInfo.label}
                  </span>
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  isUser
                    ? 'bg-teal-600 text-white rounded-br-none shadow-md shadow-teal-950/40'
                    : msg.is_crisis
                    ? 'bg-rose-950/80 border border-rose-600 text-rose-100 rounded-bl-none shadow-lg shadow-rose-950/50'
                    : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none shadow-md'
                }`}
              >
                {/* Crisis Warning Banner Inside Bot Message */}
                {msg.is_crisis && (
                  <div className="mb-3 p-3 bg-rose-900/60 border border-rose-500/50 rounded-xl flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 text-xs font-bold text-rose-200">
                      <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
                      <span>Crisis Safety Interception Activated</span>
                    </div>
                    <button
                      onClick={onOpenCrisis}
                      className="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3 py-1 rounded-lg font-bold flex items-center gap-1 shadow"
                    >
                      <PhoneCall className="w-3 h-3" />
                      View Helplines
                    </button>
                  </div>
                )}

                {/* Formatted Markdown Content */}
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Actions on Assistant Message */}
                {!isUser && (
                  <div className="mt-2 pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <span className="text-[10px] opacity-70">Empathetic CBT Nudge</span>
                    <button
                      onClick={() => speakText(msg.content)}
                      className="flex items-center gap-1 hover:text-teal-300 p-1 rounded transition"
                      title="Read aloud"
                    >
                      {isSpeaking ? (
                        <VolumeX className="w-3.5 h-3.5 text-rose-400" />
                      ) : (
                        <Volume2 className="w-3.5 h-3.5" />
                      )}
                      <span className="text-[10px]">Audio</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-center gap-3 p-3 text-sm text-slate-400 bg-slate-900/50 rounded-2xl w-fit border border-slate-800">
            <Sparkles className="w-4 h-4 text-teal-400 animate-spin" />
            <span>Aura is reflecting on your thoughts...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Prompts */}
      <div className="mt-2.5 flex items-center gap-2 overflow-x-auto py-1 no-scrollbar">
        <span className="text-[11px] text-slate-400 font-medium whitespace-nowrap flex items-center gap-1">
          <Lightbulb className="w-3.5 h-3.5 text-teal-400" />
          Suggestions:
        </span>
        {QUICK_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(prompt)}
            className="text-xs bg-slate-800/70 hover:bg-slate-800 text-slate-300 hover:text-white px-3 py-1.5 rounded-full border border-slate-700/60 whitespace-nowrap transition"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="mt-2 flex items-center gap-2 bg-slate-900 border border-slate-700/80 rounded-2xl p-2 shadow-lg"
      >
        {speechSupported && (
          <button
            type="button"
            onClick={toggleVoiceInput}
            className={`p-2.5 rounded-xl transition ${
              isListening
                ? 'bg-rose-600 text-white animate-pulse'
                : 'text-slate-400 hover:text-teal-400 hover:bg-slate-800'
            }`}
            title={isListening ? 'Stop listening' : 'Speak your thoughts'}
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </button>
        )}

        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Share what is on your mind... (e.g. feeling anxious, stressed, or happy)"
          className="flex-1 bg-transparent px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
        />

        <button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          className="bg-teal-600 hover:bg-teal-500 disabled:opacity-40 disabled:hover:bg-teal-600 text-white p-2.5 rounded-xl shadow-md shadow-teal-950/40 transition"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
