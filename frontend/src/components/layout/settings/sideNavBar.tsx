import { Button } from '@/components/ui/button'
import { useLogout } from '@/features/auth/hooks/useAuthQueries'
import { Link } from '@tanstack/react-router'

const SideNavBar = () => {
  const { mutate } = useLogout()
  //   const
  return (
    <aside className="hidden lg:flex w-64 flex-col border-r border-gray-200 dark:border-border-dark p-6 gap-8 h-full overflow-hidden">
      <div className="flex flex-col gap-2">
        <h3 className="px-3 text-xs font-bold uppercase tracking-widest text-text-muted mb-2">
          Settings
        </h3>
        <Link
          to="/settings/profile"
          activeProps={{
            className: 'bg-primary text-white shadow-lg shadow-primary/20',
          }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:bg-card-dark hover:text-white transition-all group "
        >
          <span className="material-symbols-outlined fill-icon">person</span>
          <span className="text-sm font-semibold">Profile</span>
        </Link>
        <Link
          to="/settings/account"
          activeProps={{
            className: 'bg-primary text-white shadow-lg shadow-primary/20',
          }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:bg-card-dark hover:text-white transition-all group"
        >
          <span className="material-symbols-outlined group-hover:text-white">
            settings
          </span>
          <span className="text-sm font-medium">Account</span>
        </Link>
        <Link
          to="/settings/security"
          activeProps={{
            className: 'bg-primary text-white shadow-lg shadow-primary/20',
          }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:bg-card-dark hover:text-white transition-all group"
        >
          <span className="material-symbols-outlined group-hover:text-white">
            security
          </span>
          <span className="text-sm font-medium">Security</span>
        </Link>
        <Link
          to="/settings/notifications"
          activeProps={{
            className: 'bg-primary text-white shadow-lg shadow-primary/20',
          }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:bg-card-dark hover:text-white transition-all group"
        >
          <span className="material-symbols-outlined group-hover:text-white">
            notifications
          </span>
          <span className="text-sm font-medium">Notifications</span>
        </Link>
        <Link
          to="/settings/billing"
          activeProps={{
            className: 'bg-primary text-white shadow-lg shadow-primary/20',
          }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:bg-card-dark hover:text-white transition-all group"
        >
          <span className="material-symbols-outlined group-hover:text-white">
            payments
          </span>
          <span className="text-sm font-medium">Billing</span>
        </Link>
      </div>
      <div className="mt-auto border-t border-gray-200 dark:border-border-dark pt-6">
        <Button
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-primary hover:bg-primary/10 transition-all"
          onClick={() => mutate()}
        >
          <span className="material-symbols-outlined">logout</span>
          <span className="text-sm font-semibold">Sign Out</span>
        </Button>
      </div>
    </aside>
  )
}

export default SideNavBar
