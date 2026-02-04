import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/f')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div className="text-9xl text-stone-950">Hello "/settings/f"!</div>
}
