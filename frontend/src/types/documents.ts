export type ExtractionStatus = "pending" | "success" | "failed"

export type MessageRole = "user" | "assistant"

export type DocumentPublic = {
  file_url: string
  id: string
  uploaded_at: string
  extraction_status: ExtractionStatus
}

export type DocumentsPublic = {
  data: DocumentPublic[]
  count: number
}

export type DocumentCreate = {
  file_url: string
}

export type ExplanationPublic = {
  id: string
  summary_text: string
  generated_at: string
}

export type ConversationPublic = {
  id: string
  document_id: string
  created_at: string
}

export type MessagePublic = {
  id: string
  role: MessageRole
  content: string
  created_at: string
}

export type MessageCreate = {
  content: string
}
