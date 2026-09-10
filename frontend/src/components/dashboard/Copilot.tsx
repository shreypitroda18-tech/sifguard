"use client"

import React, { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BrainCircuit, Send, User, Bot, Sparkles } from "lucide-react"
import axios from "axios"
import { motion } from "framer-motion"

export function Copilot() {
  const [query, setQuery] = useState("")
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am your SIF Copilot. Ask me questions about safety intelligence, current risks, or specific reports. You can also ask me in Hindi, Marathi, or Gujarati." }
  ])
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    const newMessages = [...messages, { role: "user", content: query }]
    setMessages(newMessages)
    setQuery("")
    setLoading(true)

    axios.post(`http://127.0.0.1:8000/api/assistant/query?query=${encodeURIComponent(query)}`)
      .then(res => {
        setMessages([...newMessages, { role: "assistant", content: res.data.answer }])
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setMessages([...newMessages, { role: "assistant", content: "I'm sorry, I'm having trouble connecting to the safety intelligence database right now." }])
        setLoading(false)
      })
  }

  const suggestedQueries = [
    "What are the highest-risk hazards this month?",
    "Which site has the most critical SIF exposure?",
    "मागील ३० दिवसांत सर्वाधिक गंभीर जोखीम कुठे आढळली?",
    "Show overdue corrective actions."
  ]

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="mb-6">
        <h2 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-3">
          <BrainCircuit className="h-8 w-8 text-primary" /> SIF Copilot
        </h2>
        <p className="text-muted-foreground mt-1">Ask questions about your safety intelligence data in multiple languages.</p>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden border-border bg-slate-50">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'assistant' && (
                <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                  <Bot className="h-4 w-4 text-primary" />
                </div>
              )}
              <div className={`p-3 rounded-lg max-w-[80%] ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-white shadow-sm border border-border'}`}>
                {msg.content}
              </div>
              {msg.role === 'user' && (
                <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
                  <User className="h-4 w-4 text-foreground" />
                </div>
              )}
            </motion.div>
          ))}
          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <BrainCircuit className="h-4 w-4 text-primary animate-pulse" />
              </div>
              <div className="p-3 rounded-lg bg-white shadow-sm border border-border flex items-center gap-2">
                <div className="h-2 w-2 bg-primary rounded-full animate-bounce"></div>
                <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="p-4 border-t border-border bg-slate-50">
          <div className="flex gap-2 overflow-x-auto pb-2 mb-2 scrollbar-hide">
            {suggestedQueries.map((sq, idx) => (
              <button 
                key={idx}
                onClick={() => setQuery(sq)}
                className="whitespace-nowrap px-3 py-1.5 text-xs bg-muted hover:bg-muted/80 rounded-full border border-border transition-colors flex items-center gap-1.5"
              >
                <Sparkles className="h-3 w-3 text-primary" /> {sq}
              </button>
            ))}
          </div>
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input 
              value={query} 
              onChange={e => setQuery(e.target.value)} 
              placeholder="Ask SIF Copilot..." 
              className="flex-1"
            />
            <Button type="submit" disabled={loading || !query.trim()} size="icon">
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  )
}
