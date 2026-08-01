import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Bot, Send } from "lucide-react"
import { useEffect, useRef, useState } from "react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { documentsApi } from "@/services/documents"
import type { MessageCreate, MessagePublic } from "@/types/documents"
import { formatTime } from "@/utils/format"

interface DocumentChatProps {
  documentId: string
}

function ChatMessage({ message }: { message: MessagePublic }) {
  const isUser = message.role === "user"

  return (
    <div className={cn("flex gap-3", isUser && "justify-end")}>
      {!isUser && (
        <div className="rounded-md bg-primary/10 p-2 self-start">
          <Bot className="size-4 text-primary" />
        </div>
      )}
      <div
        className={cn(
          "max-w-[80%] rounded-lg px-4 py-2 text-sm",
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-muted text-foreground",
        )}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>
        <p
          className={cn(
            "mt-1 text-xs",
            isUser ? "text-primary-foreground/70" : "text-muted-foreground",
          )}
        >
          {formatTime(message.created_at)}
        </p>
      </div>
    </div>
  )
}

export function DocumentChat({ documentId }: DocumentChatProps) {
  const [messages, setMessages] = useState<MessagePublic[]>([])
  const [input, setInput] = useState("")
  const scrollRef = useRef<HTMLDivElement>(null)
  const queryClient = useQueryClient()

  useQuery({
    queryKey: ["conversation", documentId],
    queryFn: async () => {
      const conversation = await documentsApi.getConversation(documentId)
      const history = await documentsApi.listMessages()
      setMessages(history)
      return conversation
    },
  })

  const sendMutation = useMutation({
    mutationFn: (data: MessageCreate) => documentsApi.sendMessage(data),
    onSuccess: (reply) => {
      setMessages((prev) => [...prev, reply])
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["conversation", documentId] })
    },
  })

  useEffect(() => {
    if (messages.length === 0) return
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    })
  }, [messages])

  const onSend = () => {
    const content = input.trim()
    if (!content) return
    const userMessage: MessagePublic = {
      id: crypto.randomUUID(),
      role: "user",
      content,
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    sendMutation.mutate({ content })
  }

  return (
    <Card className="flex h-full flex-col gap-0">
      <CardHeader className="border-b">
        <CardTitle>Ask about this document</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-1 flex-col gap-4 p-4">
        <div
          ref={scrollRef}
          className="flex flex-1 flex-col gap-4 overflow-y-auto pr-1"
        >
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="rounded-full bg-muted p-4 mb-4">
                <Bot className="size-8 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-semibold">
                Got a question about this document?
              </h3>
              <p className="text-muted-foreground max-w-sm">
                Ask me to explain any part in plain language, like "What does
                this charge mean?"
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))
          )}
        </div>
        <div className="flex gap-2 border-t pt-4">
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault()
                onSend()
              }
            }}
            placeholder="Ask about your document in plain language..."
            className="flex min-h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm outline-none placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50"
            rows={1}
          />
          <Button
            size="icon"
            onClick={onSend}
            disabled={!input.trim() || sendMutation.isPending}
            aria-label="Send"
          >
            <Send className="size-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
