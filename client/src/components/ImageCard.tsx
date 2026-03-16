type ImageCardProps = {
  src: string
  alt: string
  caption?: string
}

export function ImageCard({ src, alt, caption }: ImageCardProps) {
  return (
    <div className="space-y-1.5">
      <div className="overflow-hidden rounded-card shadow-card bg-card">
        <img
          src={src}
          alt={alt}
          className="w-full h-auto block object-contain max-h-[400px] hover:scale-[1.02] transition-transform duration-200"
        />
      </div>
      {caption && (
        <p className="text-sm text-text-muted">{caption}</p>
      )}
    </div>
  )
}
