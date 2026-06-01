import { type LabelHTMLAttributes } from 'react'

type LabelProps = LabelHTMLAttributes<HTMLLabelElement>

export function Label({ className = '', children, ...props }: LabelProps) {
  // Shared form label component for consistent spacing and typography.
  return (
    <label
      className={`block text-sm font-medium text-text-primary mb-1.5 ${className}`}
      {...props}
    >
      {children}
    </label>
  )
}
