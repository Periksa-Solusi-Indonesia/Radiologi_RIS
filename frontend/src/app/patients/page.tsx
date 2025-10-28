'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Search, Plus, Eye, Edit, Trash2 } from 'lucide-react'
import Link from 'next/link'
import { format } from 'date-fns'

// Mock data for demonstration - in a real app, this would come from an API
const mockPatients = [
  {
    id: '1',
    patientId: 'P001',
    name: 'John Doe',
    dateOfBirth: new Date('1980-05-15'),
    gender: 'MALE',
    phoneNumber: '+1234567890',
    email: 'john.doe@example.com',
    address: '123 Main St, City, State',
    emergencyContact: 'Jane Doe',
    emergencyPhone: '+0987654321',
    createdAt: new Date('2023-01-15'),
  },
  {
    id: '2',
    patientId: 'P002',
    name: 'Jane Smith',
    dateOfBirth: new Date('1992-08-22'),
    gender: 'FEMALE',
    phoneNumber: '+1234567891',
    email: 'jane.smith@example.com',
    address: '456 Oak Ave, City, State',
    emergencyContact: 'Bob Smith',
    emergencyPhone: '+0987654322',
    createdAt: new Date('2023-02-20'),
  },
  {
    id: '3',
    patientId: 'P003',
    name: 'Robert Johnson',
    dateOfBirth: new Date('1975-12-03'),
    gender: 'MALE',
    phoneNumber: '+1234567892',
    email: 'robert.johnson@example.com',
    address: '789 Pine Rd, City, State',
    emergencyContact: 'Mary Johnson',
    emergencyPhone: '+0987654323',
    createdAt: new Date('2023-03-10'),
  },
]

export default function PatientsPage() {
  const [patients, setPatients] = useState(mockPatients)
  const [searchTerm, setSearchTerm] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // In a real app, you would fetch patients from your API
  useEffect(() => {
    const fetchPatients = async () => {
      setIsLoading(true)
      try {
        // const response = await fetch('/api/patients')
        // const data = await response.json()
        // setPatients(data)
        
        // For now, using mock data
        setTimeout(() => {
          setIsLoading(false)
        }, 500)
      } catch (error) {
        console.error('Error fetching patients:', error)
        setIsLoading(false)
      }
    }

    fetchPatients()
  }, [])

  const filteredPatients = patients.filter(
    patient =>
      patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.patientId.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (patient.email && patient.email.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const getGenderBadgeVariant = (gender: string) => {
    switch (gender) {
      case 'MALE':
        return 'default'
      case 'FEMALE':
        return 'secondary'
      default:
        return 'outline'
    }
  }

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Patients</h1>
          <p className="text-muted-foreground mt-2">
            Manage and view all patient records
          </p>
        </div>
        <Link href="/patients/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            New Patient
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Patient List</CardTitle>
          <CardDescription>
            A list of all patients in the system
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2 mb-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search patients..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>

          {isLoading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Patient ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Date of Birth</TableHead>
                  <TableHead>Gender</TableHead>
                  <TableHead>Phone</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPatients.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center py-8">
                      No patients found
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredPatients.map((patient) => (
                    <TableRow key={patient.id}>
                      <TableCell className="font-medium">{patient.patientId}</TableCell>
                      <TableCell>{patient.name}</TableCell>
                      <TableCell>{format(patient.dateOfBirth, 'MMM dd, yyyy')}</TableCell>
                      <TableCell>
                        <Badge variant={getGenderBadgeVariant(patient.gender)}>
                          {patient.gender}
                        </Badge>
                      </TableCell>
                      <TableCell>{patient.phoneNumber}</TableCell>
                      <TableCell>{format(patient.createdAt, 'MMM dd, yyyy')}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end space-x-2">
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}