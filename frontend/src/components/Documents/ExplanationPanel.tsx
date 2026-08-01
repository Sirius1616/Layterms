import { useQuery } from "@tanstack/react-query"
import { Sparkles } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { documentsApi } from "@/services/documents"

interface ExplanationPanelProps {
  documentId: string
}

export function ExplanationPanel({ documentId }: ExplanationPanelProps) {
  const { data: explanation, isLoading } = useQuery({
    queryKey: ["explanation", documentId],
    queryFn: () => documentsApi.getExplanation(documentId),
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="size-4 text-primary" />
          Plain-language summary
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <p className="text-sm text-muted-foreground">
            Reading through your document...
          </p>
        ) : explanation ? (
          <p className="text-sm leading-relaxed">{explanation.summary_text}</p>
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="rounded-full bg-muted p-4 mb-4">
              <Sparkles className="size-8 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold">No explanation yet</h3>
            <p className="text-muted-foreground max-w-sm">
              Once document extraction is wired up, the important details of
              your document will be explained here in simple language.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
