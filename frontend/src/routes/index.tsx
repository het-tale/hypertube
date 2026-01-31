import { createFileRoute } from '@tanstack/react-router'

import LandingPage from '@/features/landing/'

export const Route = createFileRoute('/')({
  component: App,
})

function App() {
  return (
    <div className="text-center">
      <LandingPage />
    </div>
  )
}
