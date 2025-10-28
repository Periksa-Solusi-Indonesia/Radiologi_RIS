import { PatientFormWrapper } from "@/components/forms/PatientFormWrapper"

export default function NewPatientPage() {
  return (
    <div className="container mx-auto py-10">
      <div className="mx-auto max-w-2xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">New Patient</h1>
          <p className="text-muted-foreground mt-2">
            Enter patient information and upload DICOM files for a new radiology study.
          </p>
        </div>
        <PatientFormWrapper />
      </div>
    </div>
  )
}