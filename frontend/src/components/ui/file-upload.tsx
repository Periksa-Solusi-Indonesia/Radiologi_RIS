import * as React from "react"
import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, X, FileText, Image } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface FileUploadProps {
  onFilesChange?: (files: File[]) => void
  maxFiles?: number
  maxSize?: number // in bytes
  accept?: Record<string, string[]>
  className?: string
}

export function FileUpload({
  onFilesChange,
  maxFiles = 5,
  maxSize = 10 * 1024 * 1024, // 10MB
  accept = {
    'application/dicom': ['.dcm', '.dicom'],
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
  },
  className,
}: FileUploadProps) {
  const [files, setFiles] = useState<File[]>([])
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(
    (acceptedFiles: File[], fileRejections: any[]) => {
      setError(null)

      if (fileRejections.length > 0) {
        const rejection = fileRejections[0]
        if (rejection.errors.some((e: any) => e.code === 'file-too-large')) {
          setError(`File is larger than ${maxSize / (1024 * 1024)}MB`)
        } else if (rejection.errors.some((e: any) => e.code === 'file-invalid-type')) {
          setError('Invalid file type. Please upload DICOM files or images.')
        } else {
          setError('File upload error')
        }
        return
      }

      const newFiles = [...files, ...acceptedFiles].slice(0, maxFiles)
      setFiles(newFiles)
      onFilesChange?.(newFiles)
    },
    [files, maxFiles, maxSize, onFilesChange]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: maxFiles - files.length,
    maxSize,
    accept,
  })

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index)
    setFiles(newFiles)
    onFilesChange?.(newFiles)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (file: File) => {
    if (file.type.startsWith('image/')) {
      return <Image className="h-4 w-4" />
    }
    return <FileText className="h-4 w-4" />
  }

  return (
    <div className={cn("space-y-2", className)}>
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors",
          isDragActive
            ? "border-primary bg-primary/5"
            : "border-muted-foreground/25 hover:border-primary/50"
        )}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-muted-foreground/50 mb-4" />
        <p className="text-lg font-medium mb-2">
          {isDragActive ? "Drop the files here" : "Drag & drop files here"}
        </p>
        <p className="text-sm text-muted-foreground mb-2">
          or click to browse
        </p>
        <p className="text-xs text-muted-foreground">
          DICOM files (.dcm, .dicom) and images (.jpg, .png) up to {maxSize / (1024 * 1024)}MB
        </p>
      </div>

      {error && (
        <div className="text-sm text-destructive bg-destructive/10 p-2 rounded">
          {error}
        </div>
      )}

      {files.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium">Uploaded Files:</p>
          <div className="space-y-1">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-2 bg-muted rounded-md"
              >
                <div className="flex items-center space-x-2">
                  {getFileIcon(file)}
                  <div className="text-sm">
                    <p className="font-medium truncate max-w-xs">{file.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeFile(index)}
                  className="h-8 w-8 p-0"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}