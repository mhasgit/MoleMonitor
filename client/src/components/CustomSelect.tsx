import { useState, useRef, useEffect } from 'react'
import { ChevronDown } from 'lucide-react'

export type CustomSelectOption = { value: number; label: string }

type CustomSelectProps = {
  value: number
  onChange: (value: number) => void
  options: CustomSelectOption[]
  placeholder?: string
  className?: string
  triggerClassName?: string
}

export function CustomSelect({ value, onChange, options, placeholder = '— Select —', className = '', triggerClassName = '' }: CustomSelectProps) {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    if (open) document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [open])

  const selected = options.find((o) => o.value === value)
  const displayLabel = selected ? selected.label : placeholder

  return (
    <div ref={ref} className={`relative ${className}`}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className={`select-input w-full flex items-center justify-between gap-2 text-left ${triggerClassName}`}
      >
        <span className={value === 0 ? 'text-text-muted' : 'text-text-primary'}>{displayLabel}</span>
        <ChevronDown className={`w-4 h-4 shrink-0 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <ul
          className="absolute z-50 mt-1 w-full rounded-card border border-border bg-card shadow-card-hover py-1 max-h-48 overflow-auto"
          role="listbox"
        >
          {options.map((opt) => (
            <li
              key={opt.value}
              role="option"
              aria-selected={opt.value === value}
              onClick={() => {
                onChange(opt.value)
                setOpen(false)
              }}
              className={`px-3 py-2 cursor-pointer text-sm transition-colors text-text-primary ${
                opt.value === value
                  ? 'bg-accent/20 text-accent font-medium'
                  : 'hover:bg-hover-surface'
              }`}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
