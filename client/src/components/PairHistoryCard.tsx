import { formatPairTimestamp, uploadsUrl, type Pair } from '../api'
import { Card } from './Card'
import { Button } from './Button'
import { FileText, Trash2 } from 'lucide-react'

type PairHistoryCardProps = {
  pair: Pair
  onViewReport: () => void
  onDelete: () => void
}

export function PairHistoryCard({ pair, onViewReport, onDelete }: PairHistoryCardProps) {
  const name = pair.pair_name || `Pair ${pair.id}`
  return (
    <Card className="flex flex-row flex-wrap items-center gap-4 p-4">
      <div className="flex shrink-0 gap-2">
        <div className="w-16 h-16 rounded-lg overflow-hidden bg-hover-surface border border-border shrink-0">
          <img
            src={uploadsUrl(pair.path_a)}
            alt="Old image"
            className="w-full h-full object-cover"
          />
        </div>
        <div className="w-16 h-16 rounded-lg overflow-hidden bg-hover-surface border border-border shrink-0">
          <img
            src={uploadsUrl(pair.path_b)}
            alt="New image"
            className="w-full h-full object-cover"
          />
        </div>
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-base font-bold text-text-primary m-0">{name}</p>
        <p className="text-sm text-text-muted mt-0.5 m-0">
          {formatPairTimestamp(pair.created_at)}
        </p>
      </div>
      <div className="flex shrink-0 gap-2">
        <Button variant="primary" onClick={onViewReport}>
          <FileText className="w-4 h-4" />
          View Report
        </Button>
        <Button variant="destructive" onClick={onDelete}>
          <Trash2 className="w-4 h-4" />
          Delete
        </Button>
      </div>
    </Card>
  )
}
