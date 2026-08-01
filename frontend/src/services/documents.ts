import type {
  ConversationPublic,
  DocumentCreate,
  DocumentPublic,
  DocumentsPublic,
  ExplanationPublic,
  MessageCreate,
  MessagePublic,
} from "@/types/documents"

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

let mockDocuments: DocumentPublic[] = []
const mockExplanation = ""

export const documentsApi = {
  async listDocuments(): Promise<DocumentsPublic> {
    await delay(400)
    return { data: mockDocuments, count: mockDocuments.length }
  },

  async uploadDocument(_data: DocumentCreate): Promise<DocumentPublic> {
    await delay(1200)
    const document: DocumentPublic = {
      id: crypto.randomUUID(),
      file_url: _data.file_url,
      uploaded_at: new Date().toISOString(),
      extraction_status: "pending",
    }
    mockDocuments = [document, ...mockDocuments]
    return document
  },

  async getDocument(id: string): Promise<DocumentPublic | undefined> {
    await delay(300)
    return mockDocuments.find((document) => document.id === id)
  },

  async getExplanation(_documentId: string): Promise<ExplanationPublic | null> {
    await delay(800)
    if (!mockExplanation) {
      return null
    }
    return {
      id: crypto.randomUUID(),
      summary_text: mockExplanation,
      generated_at: new Date().toISOString(),
    }
  },

  async getConversation(documentId: string): Promise<ConversationPublic> {
    await delay(300)
    return {
      id: crypto.randomUUID(),
      document_id: documentId,
      created_at: new Date().toISOString(),
    }
  },

  async listMessages(): Promise<MessagePublic[]> {
    await delay(300)
    return []
  },

  async sendMessage(_data: MessageCreate): Promise<MessagePublic> {
    await delay(600)
    return {
      id: crypto.randomUUID(),
      role: "assistant",
      content:
        "This is a placeholder reply. Once the document extraction is wired up, I will answer questions about your document in plain language.",
      created_at: new Date().toISOString(),
    }
  },
}
