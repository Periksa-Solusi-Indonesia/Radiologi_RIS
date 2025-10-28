"use client"

import { PatientForm } from "@/components/forms/PatientForm"
import { useToast } from "@/components/ui/use-toast"

export function PatientFormWrapper() {
  const { toast } = useToast()
  
  const handlePatientSubmit = async (data: any, files: File[]) => {
    try {
      // In a real application, you would send this data to your API
      console.log('Patient data:', data)
      console.log('Uploaded files:', files)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "Success",
        description: "Patient registered successfully!",
      })
    } catch (error) {
      console.error('Error registering patient:', error)
      toast({
        title: "Error",
        description: "Failed to register patient. Please try again.",
        variant: "destructive",
      })
    }
  }

  return <PatientForm onSubmit={handlePatientSubmit} />
}