import SideBarLayout from '@/components/layout/settings/layout'
import ProtectedRoute from '@/features/auth/components/ProtectedRoute'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <ProtectedRoute>
      <div className="bg-background-dark dark:bg-background-dark  text-gray-900 dark:text-white h-full">
        <div className="layout-container flex flex-col h-full">
          <SideBarLayout />
        </div>
      </div>
    </ProtectedRoute>
  )
}
