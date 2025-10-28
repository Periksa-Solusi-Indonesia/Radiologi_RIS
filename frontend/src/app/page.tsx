import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Radiology Information System</h1>
            </div>
            <nav className="flex items-center space-x-4">
              <Link href="/patients">
                <Button variant="outline">Patient List</Button>
              </Link>
              <Link href="/patients/new">
                <Button>New Patient</Button>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>Patient List</CardTitle>
                <CardDescription>
                  View and manage all registered patients
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/patients">
                  <Button className="w-full">View Patients</Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>Patient Registration</CardTitle>
                <CardDescription>
                  Register new patients and upload DICOM files
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/patients/new">
                  <Button className="w-full">Register Patient</Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>Study Management</CardTitle>
                <CardDescription>
                  View and manage radiology studies
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" disabled>
                  Coming Soon
                </Button>
              </CardContent>
            </Card>

            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>DICOM Viewer</CardTitle>
                <CardDescription>
                  View and analyze medical images
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" disabled>
                  Coming Soon
                </Button>
              </CardContent>
            </Card>

            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>Reporting</CardTitle>
                <CardDescription>
                  Create and manage radiology reports
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" disabled>
                  Coming Soon
                </Button>
              </CardContent>
            </Card>

            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>Worklist</CardTitle>
                <CardDescription>
                  Manage radiology worklists
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" disabled>
                  Coming Soon
                </Button>
              </CardContent>
            </Card>

            <Card className="transition-all duration-300 hover:shadow-lg">
              <CardHeader>
                <CardTitle>Analytics</CardTitle>
                <CardDescription>
                  View system analytics and statistics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" disabled>
                  Coming Soon
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
