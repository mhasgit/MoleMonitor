import { Loader2 } from 'lucide-react'

type SpinnerProps = {
  className?: string
  size?: number
}

export function Spinner({ className = '', size = 24 }: SpinnerProps) {
  return (
    <Loader2
      className={`animate-spin text-accent ${className}`}
      size={size}
      aria-hidden
    />
  )
}
