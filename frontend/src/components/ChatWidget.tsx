import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import './ChatWidget.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  activeTool?: string; // If the assistant is currently running a tool
}

const ChatWidget: React.FC = () => {
  const { token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Connect WebSocket
  useEffect(() => {
    if (!token) return;

    const wsUrl = `ws://localhost:8000/api/v1/ws/chat?token=${token}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        setMessages((prev) => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];

          if (data.type === 'token') {
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.content += data.content;
            } else {
              newMessages.push({ id: Date.now().toString(), role: 'assistant', content: data.content });
            }
          } else if (data.type === 'tool_start') {
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.activeTool = data.name;
            } else {
              newMessages.push({ id: Date.now().toString(), role: 'assistant', content: '', activeTool: data.name });
            }
          } else if (data.type === 'tool_end') {
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.activeTool = undefined; // Tool finished
            }
          } else if (data.type === 'message_end') {
            setIsTyping(false);
            if (lastMessage && lastMessage.role === 'assistant') {
               lastMessage.activeTool = undefined;
            }
          } else if (data.type === 'message') {
             // Fallback for non-streaming strings
             if (lastMessage && lastMessage.role === 'assistant') {
                lastMessage.content = data.content;
             } else {
                newMessages.push({ id: Date.now().toString(), role: 'assistant', content: data.content });
             }
          }
          return newMessages;
        });
      } catch (err) {
        console.error("Failed to parse WS message", err);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      setIsTyping(false);
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [token]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !wsRef.current || !isConnected) return;

    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    
    wsRef.current.send(JSON.stringify({ message: input }));
    setInput('');
    setIsTyping(true);
  };

  return (
    <div className="chat-widget glass-panel">
      <div className="chat-header">
        <h3>AI Assistant</h3>
        <div className="status-indicator">
          <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
          {isConnected ? 'Online' : 'Reconnecting...'}
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-empty-state">
            <p>Ask me about your portfolio or market data!</p>
          </div>
        )}
        
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message ${msg.role}`}>
            <div className="message-content">
              {msg.activeTool && (
                <div className="tool-badge">
                  <span className="spinner"></span>
                  Working on: {msg.activeTool}
                </div>
              )}
              {msg.content && <p>{msg.content}</p>}
            </div>
          </div>
        ))}
        {isTyping && messages.length > 0 && messages[messages.length-1].role === 'user' && (
             <div className="chat-message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                     <span></span><span></span><span></span>
                  </div>
                </div>
             </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-area" onSubmit={sendMessage}>
        <input
          type="text"
          className="input-field"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a command..."
          disabled={!isConnected || isTyping}
        />
        <button type="submit" className="btn-primary" disabled={!isConnected || !input.trim() || isTyping}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatWidget;
