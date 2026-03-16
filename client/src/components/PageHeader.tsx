type PageHeaderProps = {
  title: string
  subtitle?: string
}

export function PageHeader({ title, subtitle }: PageHeaderProps) {
  return (
    <header className="mb-6">
      <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">
        {title}
      </h1>
      {subtitle && (
        <p className="text-text-muted text-base">{subtitle}</p>
      )}
    </header>
  )
}
