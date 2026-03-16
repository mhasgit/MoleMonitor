import { useRef, useState } from 'react'
import { Upload } from 'lucide-react'
import { Button } from './Button'
import { Label } from './Label'
import { Card } from './Card'

type ImageUploaderProps = {
  label: string
  file: File | null
  previewUrl: string | null
  onFileChange: (file: File | null) => void
  accept?: string
  disabled?: boolean
}

export function ImageUploader({
  label,
  file,
  previewUrl,
  onFileChange,
  accept = '.jpg,.jpeg,.png,.webp,.bmp',
  disabled = false,
}: ImageUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [isDragOver, setIsDragOver] = useState(false)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) onFileChange(f)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    if (disabled) return
    const f = e.dataTransfer.files?.[0]
    if (f && /^image\//.test(f.type)) onFileChange(f)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    if (disabled) return
    e.dataTransfer.dropEffect = 'copy'
    setIsDragOver(true)
  }

  const handleDragLeave = () => {
    setIsDragOver(false)
  }

  const handleClear = () => {
    onFileChange(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <Card className="flex flex-col">
      <Label>{label}</Label>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleInputChange}
        className="hidden"
        disabled={disabled}
      />
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`min-h-[180px] border-2 border-dashed rounded-card flex flex-col items-center justify-center gap-3 p-4 transition-colors duration-200 ${
          disabled ? 'opacity-50 cursor-not-allowed pointer-events-none border-border' : isDragOver ? 'border-accent bg-accent/10' : 'border-border hover:border-accent/50'
        }`}
      >
        {previewUrl ? (
          <>
            <img
              src={previewUrl}
              alt="Preview"
              className="max-h-40 max-w-full object-contain rounded-lg"
            />
            <p className="text-sm text-text-muted truncate max-w-full px-2">
              {file?.name ?? 'Preview'}
            </p>
            <div className="flex gap-2">
              <Button
                variant="secondary"
                onClick={() => inputRef.current?.click()}
                disabled={disabled}
              >
                <Upload className="w-4 h-4" />
                Change
              </Button>
              <Button variant="ghost" onClick={handleClear} disabled={disabled}>
                Clear
              </Button>
            </div>
          </>
        ) : (
          <>
            <Upload className="w-10 h-10 text-text-muted" />
            <p className="text-sm text-text-muted text-center">
              Drag and drop or click to upload
            </p>
            <Button
              variant="secondary"
              onClick={() => inputRef.current?.click()}
              disabled={disabled}
            >
              Choose file
            </Button>
          </>
        )}
      </div>
    </Card>
  )
}
