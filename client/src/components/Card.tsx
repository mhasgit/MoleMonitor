import { type HTMLAttributes } from 'react'

type CardProps = HTMLAttributes<HTMLDivElement>

export function Card({ className = '', children, ...props }: CardProps) {
  // Consistent card container used across pages for grouped content blocks.
  return (
    <div
      className={`bg-card border border-border rounded-card p-5 shadow-card hover:shadow-card-hover transition-all duration-200 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
