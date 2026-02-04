import { Outlet } from '@tanstack/react-router'
import SideNavBar from './sideNavBar'

const SideBarLayout = () => {
  return (
    <div className="flex h-full w-full max-w-360 mx-auto">
      <SideNavBar />
      <main className="flex-1 overflow-y-auto p-8 scrollbar-hide">
        <Outlet />
      </main>
    </div>
  )
}

export default SideBarLayout
