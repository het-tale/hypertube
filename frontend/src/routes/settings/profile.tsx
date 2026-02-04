import ProfileSettings from '@/features/settings/profile/components/profile'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/profile')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <main className="flex-1  overflow-y-auto">
      <ProfileSettings />
    </main>
  )
}
